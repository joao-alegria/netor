from marshmallow import Schema, ValidationError
from marshmallow.fields import String, List, Nested
from api.serializers.ns_descriptor import etsi_nfv_nsd
from api.serializers.ns_template import NstSerializer
from api.serializers.utils import pyangbind_load
from api.serializers.vs_blueprint import VsdNsdTranslationRuleSerializer, VsBlueprintSerializer, VsbActionsSerializer
from api.serializers.vnf import OnBoardVnfPackageRequestSerializer


class VsBlueprintRequestSerializer(Schema):
    nsds = etsi_nfv_nsd()
    translation_rules = List(Nested(VsdNsdTranslationRuleSerializer))
    available_actions = List(Nested(VsbActionsSerializer))
    nsts = List(Nested(NstSerializer))
    owner = String()
    vs_blueprint = Nested(VsBlueprintSerializer, required=True,
                          error_messages={"required": "Onboard VS blueprint request without VS blueprint"})
    vnf_packages = List(Nested(OnBoardVnfPackageRequestSerializer))

    def load(self, data, *, many=None, partial=None, unknown=None):
        if data.get('vs_blueprint', {}).pop('translation_rules', None) is not None:
            raise ValidationError({'vs_blueprint': {'translation_rules': ['Unknown field.']}}, "translation_rules")

        nsds = {'nsd': {'nsd': data.pop('nsds', None)}}

        if nsds is not None:
            nsds = pyangbind_load(etsi_nfv_nsd(), nsds, "Invalid content for Nsd object").get('etsi-nfv-nsd:nsd',
                                                                                              {}).get('nsd')

        validated_data = super().load(data)
        if nsds is not None:
            validated_data.update({'nsds': nsds})
        return validated_data
