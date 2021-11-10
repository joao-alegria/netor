from pyangbind.lib.serialise import pybindJSONDecoder
from api.exceptions.exceptions import InvalidEntity
import pyangbind.lib.pybindJSON as pybindJSON
import yaml


def pyangbind_load(obj, data, error_message, force=False):
    try:
        pybindJSONDecoder.load_ietf_json(data, None, None, obj=obj,
                                         path_helper=True, skip_unknown=force)
        out = pybindJSON.dumps(obj, mode="ietf")
        desc_out = yaml.safe_load(out)
        return desc_out
    except Exception as e:
        raise InvalidEntity(error_message)
