# optenum
A missing python Option/Enum libary which supports enum code, name, text, even (code, name) tuple list and so on.


# Quick start

``` To be written
```

# Background
Ofen we need to define some enums or options. But looks python missing this class.
Sometimes we uses class, tuples or dict as the replacement. But they are not convenience.

For example, we use class as enum. We can use `MyOption.foo` to get the enum value `1`.
```
Class MyOption(object):
    foo = 1
    bar = 2
```
But how can we get the enum name foo ? How can we get the list of all enums ? Even list of tuples `[ (1, 'foo'), (2, 'bar')]` (useful in Django model)

Although Python 3.7 comes with data classes[https://docs.python.org/3/whatsnew/3.7.html#whatsnew37-pep557]. So far it looks like a piece of syntax sugar for me and it can not solve these problems.

# Features

  * Code - Enumration/option by different types - e.g. 0, 1, -1 (or 'new', 'running', 'stopped')
  * Name - Name of an enum/option - e.g.  'NEW', 'RUNNING', 'STOPPED'. Support dot access. 
  * Text - Meaning or description of the enum/option. support i18n - e.g. _('new'), _('running'), _('stopped') (translated to '新建', '运行中', ‘停止中’)
  * List - Retrieve list of code, name or text `[0, 1, -1]`
  * Dict - Retrieve dict of `{code: name}` mapping. even `{code: text}`, `{name: text}` mapping if required.
  * List of tuples - Retrieve list of `[(code, name), ...]` tuples. Useful in **Django** model.
  * Grouping - Group a set of enums/options. e.g. IN_PROGERSS_STATE = ['STARTING', 'STOPPING'], but 'STARTED' and 'STOPPED' are not belongs to it.
  * Access **name**, **text** by **code**
  * Lookup enum/option by **name**, **code**
  
# Guide / Tutor
