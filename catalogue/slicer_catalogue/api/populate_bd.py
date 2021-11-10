import os

from mongoengine import connect
from mixer.backend.mongoengine import TypeMixer, Mixer

from api.models.ns_template import Nst
from api.models.ns_descriptor import Nsd
from api.models.vs_blueprint import VsdNsdTranslationRule, VsBlueprint, VsBlueprintInfo, VsComponent
from api.models.vnf import OnBoardVnfPackageRequest
from api.models.vs_descriptor import VsDescriptor

connection_data = {
    # 'username': os.environ.get('MONGO_USERNAME', 'root'),
    # 'password': os.environ.get('MONGO_PASSWORD', 'root'),
    'host': os.environ.get('MONGO_URL', 'localhost'),
    'port': 27017,
    'db': os.environ.get('MONGO_DB', 'catalogues'),
    # 'authentication_source': 'admin',
    # 'replicaSet': 'rs0'
}

connect(**connection_data)


class MyTypeMixer(TypeMixer):
    def __init__(self, cls, **params):
        super(MyTypeMixer, self).__init__(cls, **params)

    @staticmethod
    def is_required(field):
        # Avoid MapFields due to mixer's errors
        return field.scheme.__class__.__name__ != 'MapField'


class MyMixer(Mixer):
    def __init__(self, **params):
        self.type_mixer_cls = MyTypeMixer
        super(MyMixer, self).__init__(**params)


mixer = MyMixer()

if __name__ == '__main__':
    for i in range(5):
        nsd = mixer.blend(Nsd)
        vsd_nsd_translation_rule = mixer.blend(VsdNsdTranslationRule, blueprint_id=str(i))
        on_board_vnf_package_request = mixer.blend(OnBoardVnfPackageRequest)
        args = dict(blueprint_id=f'{i}', version=f'version_{i}', name=f'name_{i}')
        if i == 1:
            args['atomic_components'] = [mixer.blend(VsComponent, compatible_site=None)]
        vs_blueprint = mixer.blend(VsBlueprint, **args)
        vs_blueprint_info = mixer.blend(VsBlueprintInfo, vs_blueprint_id=f'{i}', vs_blueprint_version=f'version_{i}',
                                        name=f'name_{i}', active_vsd_id=[f"{j}" for j in range(5)])
        vs_descriptor = mixer.blend(VsDescriptor, descriptor_id=f"{i}", vs_blueprint_id=f'{i}', tenant_id='tenant')
        nst = mixer.blend(Nst, nsst=None, geographical_area_info_list=[])
