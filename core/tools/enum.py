class _EnumMeta(type):
    def __init__(cls, name, bases, dct):
        super(_EnumMeta, cls).__init__(name, bases, dct)
        cls._choices_keys = dict(cls.__dict__['_choices']) \
            if '_choices' in cls.__dict__ else dict()
        cls._choices_values = dict(
            ((v, k) for k, v in cls.__dict__['_choices'])
        ) if '_choices' in cls.__dict__ else dict()

    def __call__(cls, key=None):
        if key is None:
            return cls._choices
        return cls._to_str(key)

    def get_key(cls, value):
        try:
            return cls._choices_values[value]
        except KeyError:
            return None


class Enum(object):
    __metaclass__ = _EnumMeta

    @classmethod
    def _to_str(cls, key):
        try:
            key = int(key)
        except (ValueError, TypeError):
            return None
        return cls._choices_keys.get(key, None)
