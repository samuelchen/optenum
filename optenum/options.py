"""
Options represents an set of option items (enumerations). It is a list of options/enum entries.
"""

import six
from .option import Option


class OptionGroup(object):

    def __init__(self, *options):
        group = []
        for opt in options:
            group.append(opt)

        self._group = group

    def get_option_list(self):
        return self._group


class OptionsMeta(type):

    def __new__(cls, name, bases, namespace):
        instance = super(OptionsMeta, cls).__new__(cls, name, bases, namespace)
        name_options_mapping = {}
        code_options_mapping = {}
        groups_mapping = {}

        if name != 'Options':
            for attr, val in namespace.items():
                if attr.startswith('_'):
                    continue
                elif not attr.isupper():
                    raise AttributeError('Option name must be uppercase. "%s" is not uppercase.' % attr)
                else:
                    if attr in name_options_mapping.keys():
                        raise AttributeError('Duplicate option "%s" found' % attr)

                    if isinstance(val, OptionGroup):
                        groups_mapping[attr] = val
                        setattr(cls, attr, val.get_option_list())
                        continue

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
                    else:
                        opt = Option(code=val, name=attr)

                    if opt.code in code_options_mapping:
                        raise ValueError('Duplicate code "%s" found' % opt.code)

                    setattr(instance, attr, opt)
                    name_options_mapping[attr] = opt
                    code_options_mapping[opt.code] = opt

        instance.__name_options_mapping__ = name_options_mapping
        instance.__code_options_mapping__ = code_options_mapping

        return instance


@six.add_metaclass(OptionsMeta)     # py2,3 compatibility
class Options(object):
    """
    Derive class `Options` to implement your enum/options.
    e.g
    ```
        # simple way
        class EnumFruits(Options):
            APPLE = 1
            ORANGE = 2
            BANANA = 3

        # option `code` + `text` description in tuple
        class DoorStates(Options):
            OPEN = 'O', 'Door is opened'
            CLOSED = ('C', 'Door is closed')
            IN_OPENING = 'IO'
            IN_CLOSING = 'IC'
    ```
    """

    __order_by_code = 'code'
    __order_by_name = 'name'

    _G = OptionGroup

    @classmethod
    def __get_name_options_mapping(cls):
        """
        Dict of {'name': option} mapping.
        DO NOT change this dict. TODO: make it immutable.

        :return: dict {"name": option}
        """
        return cls.__name_options_mapping__

    @classmethod
    def __get_code_options_mapping(cls):
        """
        Dict of {'code': option} mapping
        DO NOT change this dict. TODO: make it immutable.
        :return: dict {"name": option}
        """
        return cls.__code_options_mapping__

    @classmethod
    def lookup_by_code(cls, option_code):
        assert isinstance(option_code, Option.AVAILABLE_CODE_TYPES)

        return cls.__get_code_options_mapping().get(option_code, Option.NOT_DEFINED)

    @classmethod
    def lookup_by_name(cls, option_name):
        assert isinstance(option_name, six.string_types)

        return cls.__get_name_options_mapping().get(option_name, Option.NOT_DEFINED)

    @classmethod
    def get_order_by_kw_code(cls):
        """
        Get the keyword to order by "code"
        :return:
        """
        return cls.__order_by_code

    @classmethod
    def get_order_by_kw_name(cls):
        """
        Get the keyword to order by "name"
        :return:
        """
        return cls.__order_by_name

    @classmethod
    def get_option_list(cls, order_by=None, reverse=False):
        """
        Get all options as a list
        :param order_by: Sort order. by 'name' or 'code' (use get_order_by_kw_xxx() to get).
        :param reverse: Whether sort is reversed. Only available when `order_by` is not set correctly.
        :return: List of `Option` object.
        """
        assert order_by in [None, cls.get_order_by_kw_code(), cls.get_order_by_kw_name()], \
            'Incorrect order_by'

        options = cls.__get_name_options_mapping()

        if order_by == cls.get_order_by_kw_code():
            lst = sorted(options.values(), key=lambda o: o.code, reverse=reverse)
        elif order_by == cls.get_order_by_kw_name():
            lst = sorted(options.values(), key=lambda o: o.name, reverse=reverse)
        else:
            lst = options.values()

        return lst

    @classmethod
    def get_code_list(cls, order_by=None, reverse=False):
        """
        Get all option codes as a list
        :param order_by: Sort order. by 'name' or 'code' (use get_keyword_order_by_xx() to get).
        :param reverse: Whether sort is reversed. Only available when `order_by` is not set correctly.
        :return: List of codes.
        """
        options = cls.get_option_list(order_by=order_by, reverse=reverse)
        codes = [o.code for o in options]
        return codes

    @classmethod
    def get_name_list(cls, order_by=None, reverse=False):
        """
        Get all option names as a list
        :param order_by: Sort order. by 'name' or 'code' (use get_keyword_order_by_xx() to get).
        :param reverse: Whether sort is reversed. Only available when `order_by` is not set correctly.
        :return: List of names.
        """
        options = cls.get_option_list(order_by=order_by, reverse=reverse)
        names = [o.name for o in options]
        return names

    @classmethod
    def get_code_name_list(cls, order_by=None, reverse=False, code_first=True):
        """
        Get all option tuple (name, code) or (code, name) as a list
        :param order_by: Sort order. by 'name' or 'code' (use get_keyword_order_by_xx() to get).
        :param reverse: Whether sort is reversed. Only available when `order_by` is not set correctly.
        :param code_first: Bool. If true, `code` will be at first (code, name). Otherwise, `name` first (name, code).
        :return: List of (code, name) or (name, code) tuples.
        """
        options = cls.get_option_list(order_by=order_by, reverse=reverse)

        if code_first:
            lst = [(o.code, o.name) for o in options]
        else:
            lst = [(o.name, o.code) for o in options]

        return lst

    @classmethod
    def get_code_text_list(cls, order_by=None, reverse=False, code_first=True):
        """
        Get all option tuple (code, text) or (text, code) as a list
        :param order_by: Sort order. by 'name' or 'code' (use get_keyword_order_by_xx() to get).
        :param reverse: Whether sort is reversed. Only available when `order_by` is not set correctly.
        :param code_first: Bool. If true, `code` will be at first (code, name). Otherwise, `name` first (name, code).
        :return: List of (code, text) or (text, code) tuples.
        """

        options = cls.get_option_list(order_by=order_by, reverse=reverse)

        if code_first:
            lst = [(o.code, o.text) for o in options]
        else:
            lst = [(o.text, o.code) for o in options]

        return lst


__all__ = ('Options', )
