from mongoengine import Document, DynamicDocument
from mongoengine.fields import StringField, MapField
from api.queries.utils import get_or_error


class OnBoardVnfPackageRequest(Document):
    name = StringField()
    version = StringField()
    provider = StringField()
    checksum = StringField()
    user_defined_data = MapField(StringField())
    vnf_package_path = StringField()

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()


class Vnfd(DynamicDocument):

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()
