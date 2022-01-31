import logging
import api.queries.vs_descriptor as vs_descriptor_queries
import uuid
from bson import ObjectId
from mongoengine.queryset.visitor import Q

from api.models.ns_descriptor import Nsd
from api.models.vnf import Vnfd
from api.models.vs_blueprint import VsBlueprintInfo, VsBlueprint, VsdNsdTranslationRule, VsbActions
from api.models.ns_template import Nst
from api.exceptions.exceptions import MalFormedException, FailedOperationException, AlreadyExistingEntityException, \
    NotExistingEntityException
from api.exceptions.utils import exception_message_elements
from api.queries.utils import transaction, extract_file, download_file, get_json_in_folder, file_exists, move_file, \
    remove_file_and_folder, convert_all_fields_to_snake, aggregate_transactions
from copy import deepcopy
from api.serializers.utils import pyangbind_load
from api.serializers.vnf import etsi_nfv_vnfd
from api.serializers.ns_descriptor import etsi_nfv_nsd


# noinspection PyBroadException
def _post_process_vsb(original_vs_blueprint_info, tenant_id):
    target_vs_blueprint_info = deepcopy(original_vs_blueprint_info)
    target_vs_blueprint_info.vs_blueprint = original_vs_blueprint_info.vs_blueprint
    target_vs_blueprint_info.active_vsd_id = []

    for id_ in original_vs_blueprint_info.active_vsd_id:
        try:
            target_vs_blueprint_info.active_vsd_id.append(vs_descriptor_queries.get_vs_descriptors(tenant_id, id_)[0])
        except Exception:
            continue

    return target_vs_blueprint_info


# noinspection PyTypeChecker
def get_vs_blueprints(vsb_id=None, vsb_name=None, vsb_version=None, tenant_id=None, with_translation_rules=False):
    arguments = locals()
    arguments.pop('with_translation_rules', None)
    parameters_size = len(dict(filter(lambda a: a[-1] is not None, arguments.items())))

    if parameters_size == 1 and (vsb_id is not None):
        vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vsb_id)
        if with_translation_rules:
            vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vsb_id)

        return [vsbi]

    elif parameters_size == 1 and (tenant_id is not None):
        vsbi_list = []

        for vsbi in VsBlueprintInfo.objects.all():
            vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsbi.name, version=vsbi.vs_blueprint_version)
            if with_translation_rules:
                vs_blueprint_id = vsbi.vs_blueprint.blueprint_id
                vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vs_blueprint_id)
            vsbi_list.append(_post_process_vsb(vsbi, tenant_id))

        return vsbi_list

    elif parameters_size == 2 and (vsb_name is not None) and (vsb_version is not None):
        vsbi = VsBlueprintInfo.get_or_404(name=vsb_name, vs_blueprint_version=vsb_version)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsb_name, version=vsb_version)
        if with_translation_rules:
            vs_blueprint_id = vsbi.vs_blueprint.blueprint_id
            vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vs_blueprint_id)

        return [vsbi]

    elif parameters_size == 2 and (vsb_id is not None) and (tenant_id is not None):
        vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vsb_id)
        if with_translation_rules:
            vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vsb_id)

        return [_post_process_vsb(vsbi, tenant_id)]

    elif parameters_size == 0:
        all_vsbi = VsBlueprintInfo.objects.all()
        for vsbi in all_vsbi:
            vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsbi.name, version=vsbi.vs_blueprint_version)
            if with_translation_rules:
                vs_blueprint_id = vsbi.vs_blueprint.blueprint_id
                vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vs_blueprint_id)

        return all_vsbi

    raise MalFormedException()


def delete_vs_blueprint(vsb_id):
    vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
    if len(vsbi.active_vsd_id) > 0:
        raise FailedOperationException("There are some VSDs associated to the VS Blueprint. Impossible to remove it.")

    def delete_callback(session):
        VsBlueprintInfo.get_collection().delete_one({
            "vs_blueprint_id": vsb_id
        }, session=session)

        VsBlueprint.get_collection().delete_one({
            "blueprint_id": vsb_id
        }, session=session)

    transaction(delete_callback)


def _store_vnfd(vnf, vnfd):
    vnfd_id, vnfd_version = vnfd.pop('id', None), vnf.get('version')

    if Vnfd.objects.filter((Q(vnfd_id=vnfd) & Q(version=vnfd_version)) |
                           (Q(name=vnf.get('name')) & Q(provider=vnf.get('provider')) &
                            Q(version=vnf.get('version')))).count() > 0:
        raise AlreadyExistingEntityException(f"Vnfd with vnfdId: {vnfd.vndf_id} already present in DB")

    vnfd['vnfd_id'] = vnfd_id

    return vnfd


def _onboard_vnf_package(vnf):
    downloaded_file = download_file(vnf.get('vnf_package_path'), str(uuid.uuid4()))
    folder = extract_file(downloaded_file)
    json_content = get_json_in_folder(folder)

    if file_exists(f'{folder}/cloud-config.txt'):
        # need to not delete cloud init
        move_file(f'{folder}/cloud-config.txt')

    remove_file_and_folder(downloaded_file, folder)

    vnfd = pyangbind_load(etsi_nfv_vnfd(), json_content, "Invalid content for Vnfd object").get('etsi-nfv-vnfd:vnfd')

    if vnfd is None:
        raise MalFormedException('VNFD for onboarding is empty')

    return _store_vnfd(vnf, convert_all_fields_to_snake(vnfd))


def _on_board_ns_template(nst, nsds, vnf_packages):
    nsds = [] if nsds is None else nsds
    vnf_packages = [] if vnf_packages is None else vnf_packages

    # Vnf Packages
    all_vnfd_data = []
    for vnf in vnf_packages:
        try:
            vnfd_data = _onboard_vnf_package(vnf)
            all_vnfd_data.append(vnfd_data)
        except AlreadyExistingEntityException:
            continue

    transaction_data = []
    if len(all_vnfd_data) > 0:
        transaction_data += [
            {
                'collection': Vnfd.get_collection(),
                'operation': 'insert_many',
                'args': (all_vnfd_data,)
            }
        ]

    # Nsds
    all_nsd_data = []
    for nsd in nsds:
        try:
            nsd_data = convert_all_fields_to_snake(nsd)
            all_nsd_data.append(nsd_data)
        except AlreadyExistingEntityException:
            continue

    if len(all_nsd_data) > 0:
        transaction_data += [
            {
                'collection': Nsd.get_collection(),
                'operation': 'insert_many',
                'args': (all_nsd_data,)
            }
        ]
    nst_name, nst_version, nst_id = nst.get('nst_name'), nst.get('nst_version'), nst.get('nst_id')
    if Nst.objects.filter((Q(nst_name=nst_name) & Q(nst_version=nst_version)) | Q(nst_id=nst_id)).count() > 0:
        raise AlreadyExistingEntityException(
            f"NsTemplate with name {nst_name} and version {nst_version} or ID {nst_id} exists")

    if len(nst) > 0:
        transaction_data += [
            {
                'collection': Nst.get_collection(),
                'operation': 'insert_one',
                'args': (nst,)
            }
        ]
    return transaction_data


def _process_ns_descriptor_onboarding(data):
    nsts, nsds, vnf_packages = data.get('nsts', []), data.get('nsds', []), data.get('vnf_packages', [])

    if len(nsts) == 0 and len(nsds) == 0 and len(vnf_packages) == 0:
        return

    transaction_data = []
    if len(nsts) > 0:
        transaction_data += _on_board_ns_template(nsts[0], nsds, vnf_packages)
        for nst in nsts[1:]:
            transaction_data += _on_board_ns_template(nst, None, None)

    return transaction_data


def _create_vs_blueprint(data):
    transaction_data = _process_ns_descriptor_onboarding(data)
    if transaction_data is None:
        transaction_data = []

    vs_blueprint = data.get('vs_blueprint', {})

    name, version, owner = vs_blueprint.get('name'), vs_blueprint.get('version'), data.get('owner')

    blueprints = VsBlueprint.objects.filter(name=name, version=version)

    if VsBlueprintInfo.objects.filter(name=name, vs_blueprint_version=version).count() > 0 or \
           blueprints.count() > 0:
        blueprint_id =blueprints.first().blueprint_id
        class_name, args = exception_message_elements(VsBlueprint, name=name, blueprint_id=blueprint_id,\
            version=version)
        raise AlreadyExistingEntityException(f"{class_name} with {args} already present in DB")

    _id = ObjectId()
    data['_id'] = _id
    vs_blueprint_id = vs_blueprint['blueprint_id'] = str(_id)

    translation_rules = data.get('translation_rules', [])
    for translation_rule in translation_rules:
        translation_rule['blueprint_id'] = vs_blueprint_id

    transaction_data += [
        {
            'collection': VsBlueprint.get_collection(),
            'operation': 'insert_one',
            'args': (data.get('vs_blueprint'),)
        },
        {
            'collection': VsBlueprintInfo.get_collection(),
            'operation': 'insert_one',
            'args': ({
                         'vs_blueprint_id': vs_blueprint_id,
                         'vs_blueprint_version': version,
                         'name': name,
                         'owner': owner
                     },)
        }
    ]
    if len(translation_rules) > 0:
        transaction_data += [{
            'collection': VsdNsdTranslationRule.get_collection(),
            'operation': 'insert_many',
            'args': (translation_rules,)
        }]

    available_actions = data.get('available_actions', [])
    for available_action in available_actions:
        available_action['blueprint_id'] = vs_blueprint_id
    if len(available_actions) > 0:
        transaction_data += [{
            'collection': VsbActions.get_collection(),
            'operation': 'insert_many',
            'args': (available_actions,)
        }]

    return vs_blueprint_id, transaction_data


def create_vs_blueprint(data):
    vs_blueprint_id, transaction_data = _create_vs_blueprint(data)
    transaction(aggregate_transactions(transaction_data))

    return vs_blueprint_id


def get_nst():
    return Nst.objects.all()


def delete_nst(nst_id):
    Nst.get_or_404(nst_id=nst_id)

    def delete_callback(session):
        Nst.get_collection().delete_one({
            "nst_id": nst_id
        }, session=session)

    transaction(delete_callback)
