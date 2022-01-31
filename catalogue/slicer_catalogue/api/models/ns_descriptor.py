from mongoengine import DynamicDocument

from api.queries.utils import get_or_error


class Nsd(DynamicDocument):

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()
