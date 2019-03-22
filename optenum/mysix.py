"""
My py2 & py3 compilable module.
"""

import six

if six.PY2:
    import re
    regx_identifier = re.compile('^[a-z][a-z0-9_]*$', re.IGNORECASE)


def is_identifier(s):
    if six.PY2:
        m = regx_identifier.match(s)
        return bool(m)
    else:
        return s.isidentifier()
