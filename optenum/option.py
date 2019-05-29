"""
Option class represents a single option in a list of options/enum
"""
import six
from .mysix import is_identifier

NUMBER_TYPES = six.integer_types + (float,)
DATE_TYPES = ()  # (datetime, date, time)

AVAILABLE_CODE_TYPES = six.string_types + NUMBER_TYPES + DATE_TYPES
AVAILABLE_CODE_TYPES_STR = ', '.join(t.__name__ for t in AVAILABLE_CODE_TYPES)


class OptionPseudo(object):
    pass


class OptionMeta(type):

    def __new__(mcs, name, bases, namespace):
        cls_instance = super(OptionMeta, mcs).__new__(mcs, name, bases, namespace)

        cls_instance.NOT_DEFINED = None
        """Not defined option."""

        cls_instance.NUMBER_TYPES = six.integer_types + (float,)
        cls_instance.DATE_TYPES = ()  # (datetime, date, time)

        cls_instance.AVAILABLE_CODE_TYPES = six.string_types + NUMBER_TYPES + DATE_TYPES
        cls_instance.AVAILABLE_CODE_TYPES_STR = ', '.join(t.__name__ for t in AVAILABLE_CODE_TYPES)

        return cls_instance

    def __call__(cls, code, name, text=None):

        if code is None or name is None:
            raise ValueError('code or name can not be None')

        if not (code is None or isinstance(code, Option.AVAILABLE_CODE_TYPES)):
            raise TypeError('Option code must be one of %s' % AVAILABLE_CODE_TYPES_STR)

        if name is not None:
            if not isinstance(name, six.string_types):
                raise ValueError('Option name must be string type.')

            if not (name[0].isalpha() and is_identifier(name) and name.isupper()):
                raise ValueError('Option name must be alphanumeric or "_"  in uppercase and start with alphabet.')

        if not ((code is None and name is None and text is None) or (code is not None and name is not None)):
            raise ValueError('Option code and name must be not None unless code, name and text are all None.')

        cls_code = type(code)
        cls_option = type('Option(%s)' % cls_code.__name__, (cls_code, OptionPseudo), {})
        obj_option = cls_option(code)
        obj_option.code = code
        obj_option.name = name
        obj_option.text = text

        return obj_option

    def __subclasscheck__(cls, subclass):
        if issubclass(subclass, OptionPseudo):
            return True
        else:
            return super(OptionMeta, cls).__subclasscheck__(subclass)

    def __instancecheck__(cls, instance):
        if isinstance(instance, OptionPseudo):
            return True
        else:
            return super(OptionMeta, cls).__instancecheck__(instance)


@six.add_metaclass(OptionMeta)     # py2,3 compatibility
class Option(object):
    pass


__all__ = ('Option', )


