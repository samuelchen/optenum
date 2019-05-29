"""
Options represents an set of option items (enumerations). It is a list of options/enum entries.
"""

import six
from .option import Option
import logging

log = logging.getLogger(__name__)


class OptionsMeta(type):

    def __new__(cls, name, bases, namespace):
        instance = super(OptionsMeta, cls).__new__(cls, name, bases, namespace)
        name_options_mapping = {}
        code_options_mapping = {}

        ignore_invalid_name = namespace.get('__IGNORE_INVALID_NAME__', False)
        order_by = namespace.get('__ORDER_BY__', None)

        if not isinstance(ignore_invalid_name, bool):
            raise ValueError("'__IGNORE_INVALID_NAME__' must be bool type True or False.")

        if order_by not in ['code', 'name', None]:
            raise ValueError("'__ORDER_BY__' only supported on `code` and `name` field")

        if name != 'Options':
            for attr, val in namespace.items():
                if attr.startswith('_'):
                    continue
                elif not attr.isupper():
                    if callable(val) or isinstance(val, (staticmethod, classmethod, property)):
                        pass    # function
                    else:
                        if not ignore_invalid_name:
                            raise AttributeError('Option name must be uppercase. Attribute "%s" is not.' % attr)
                else:
                    if attr in name_options_mapping.keys() or hasattr(cls, attr):
                        raise AttributeError('Duplicated attribute "%s" found' % attr)

                    if isinstance(val, Option):
                        if val.name != attr:
                            raise ValueError('Option name of option %s must be same as attribute "%s"' % (val, attr))
                        else:
                            opt = val
                    elif isinstance(val, (list, tuple)):
                        if len(val) == 0:
                            raise ValueError('Option code can not be empty list or tuple')
                        elif len(val) == 1:
                            opt = Option(code=val[0], name=attr)
                        elif len(val) == 2:
                            opt = Option(code=val[0], name=attr, text=str(val[1]))
                        else:
                            raise ValueError('Option code can only be (code, text) tuple or list. name is not needed.')
                    elif isinstance(val, Option.AVAILABLE_CODE_TYPES):
                        opt = Option(code=val, name=attr)
                    else:
                        raise AttributeError('"%s" is uppercase attribute but its value can not be converted to Option.'
                                             % attr)

                    if opt.code in code_options_mapping.keys():
                        raise ValueError('Duplicated code "%s" found' % opt.code)

                    setattr(instance, attr, opt)
                    name_options_mapping[attr] = opt
                    code_options_mapping[opt.code] = opt

        instance.__name_options_mapping__ = name_options_mapping
        instance.__code_options_mapping__ = code_options_mapping

        return instance

    # Options class methods or properties
    def __get_name_options_mapping(cls):
        """
        Dict of {'name': option} mapping.
        DO NOT change this dict. TODO: make it immutable.

        :return: dict {"name": option}
        """
        return cls.__name_options_mapping__

    def __get_code_options_mapping(cls):
        """
        Dict of {'code': option} mapping
        DO NOT change this dict. TODO: make it immutable.
        :return: dict {"name": option}
        """
        return cls.__code_options_mapping__

    def __getitem__(cls, item):
        return cls.__get_name_options_mapping()[item]

    def __setitem__(cls, key, value):
        raise TypeError("'%s' class does not support item assignment" % cls.__name__)

    def __delitem__(cls, key):
        raise TypeError("'%s' class does not support item deletion" % cls.__name__)

    def __contains__(cls, item):
        if isinstance(item, Option):
            return item in cls.__get_name_options_mapping().values()
        else:
            return item in cls.__get_code_options_mapping().keys()

    def get(cls, key, default=None):
        return cls.__get_name_options_mapping().get(key, default)

    @property
    def codes(cls):
        """List of `code`s"""
        return list(cls.__get_code_options_mapping().keys())

    @property
    def names(cls):
        """List of `name`s"""
        return list(cls.__get_name_options_mapping().keys())

    @property
    def all(cls):
        """List of `Option` objects"""
        return list(cls.__get_name_options_mapping().values())

    @property
    def tuples(cls):
        """List of (`name`, `code`, `text`) tuples"""
        return [(o.name, o.code, o.text) for o in cls.__get_name_options_mapping().values()]

    @property
    def items(cls):
        """Dict of {`name`: Option} mapping"""
        return {o.name: o for o in cls.__get_name_options_mapping().values()}

    def get_list(cls, *fields):
        """
        List of *fields.
        :param fields: Field name of `Option`. Such as `code`, (`name`, `code`), [`code`, `name`, `text`] or etc.
        :return: List of *fields tuple or single value.
        """

        if len(fields) == 0:
            raise ValueError("No fields argument found.")

        found_fields = set()
        for f in fields:
            if f not in ['code', 'name', 'text']:
                raise NameError(
                    "'%s' is incorrect Option field. Only 'code', 'name' and 'text' are available." % str(f))
            if f in found_fields:
                raise ValueError("Duplicated fields '%s' found." % str(f))
            found_fields.add(f)

        lst = []
        for o in cls.__get_name_options_mapping().values():
            value = []
            for f in fields:
                value.append(getattr(o, f))
            lst.append(value[0] if len(value) == 1 else tuple(value))
        return lst

    def get_dict(cls, key_field, *fields):
        """
        Retrieve as dict of {key_field: *fields} mapping. If `fields` is single value, returns `{key:value}` mapping.
                If `fields` is **tuple**, returns `{key: (tuple of fields value)}` mapping.
        :param key_field: name of Option field for dict key. Only `code` and `name` are available.
        :param fields: Names of Option field for values. Can be tuple or single value. Impact value part of return dict.
        :return: dict of {key_field: *fields} mapping.
        """
        if key_field not in ['code', 'name']:
            raise NameError("'%s' is not correct key field. Only 'code' and 'name' can be key field." % str(key_field))

        if len(fields) == 0:
            raise ValueError("No fields argument found.")

        found_fields = set()
        for f in fields:
            if f not in ['code', 'name', 'text']:
                raise NameError(
                    "'%s' is incorrect Option field. Only 'code', 'name' and 'text' are available." % str(f))
            if f in found_fields:
                raise ValueError("Duplicated fields '%s' found." % str(f))
            found_fields.add(f)

        items = {}
        for o in cls.__get_name_options_mapping().values():
            key = getattr(o, key_field)
            value = []
            for f in fields:
                value.append(getattr(o, f))
            items[key] = value[0] if len(value) == 1 else tuple(value)

        return items


@six.add_metaclass(OptionsMeta)     # py2,3 compatibility
class Options(object):
    """
    Derive class `Options` to implement your enum/options.
    e.g
    ```
        # simple way
        class Fruit(Options):
            APPLE = 1
            ORANGE = 2
            BANANA = 3

        # option `code` + `text` description in tuple
        class DoorState(Options):
            OPEN = 'O', 'Door is opened'
            CLOSED = ('C', 'Door is closed')
            IN_OPENING = 'IO'
            IN_CLOSING = 'IC'
    ```
    """

    pass


__all__ = ('Options', )

