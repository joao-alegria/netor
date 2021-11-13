from enum import Enum


class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def get_values(cls):
        return tuple([e.value for e in cls])
