# Optenum

[![Travis](https://img.shields.io/github/languages/top/samuelchen/optenum.svg?style=flat-square)](https://pypi.org/project/optenum/)
[![Travis](https://img.shields.io/travis/samuelchen/optenum.svg?branch=master?style=flat-square)](https://travis-ci.org/samuelchen/optenum)
[![Travis](https://img.shields.io/pypi/pyversions/optenum.svg?style=flat-square)](https://pypi.org/project/optenum/)
[![Travis](https://img.shields.io/pypi/v/optenum.svg?style=flat-square)](https://pypi.org/project/optenum/)
[![Travis](https://img.shields.io/pypi/status/optenum.svg?style=flat-square)](https://pypi.org/project/optenum/)
[![Travis](https://img.shields.io/pypi/format/optenum.svg?style=flat-square)](https://pypi.org/project/optenum/)


	
A missing Python Option/Enum library which supports enum code, name, text, even (code, name) tuple list and so on.

Name "**optenum**" comes from '**opt**ion' + '**enum**eration'.

Compatible with `Python 2.7+` and `Python 3.0+`.

# Install

Python 3.x, 2.7

```bash
pip install optenum
```

For those probably missing `six` module:

```bash
pip install six optenum
```

# Quick start

1. Simple as Enum type

    Says we define a simple enum:
    
    ```python
    from optenum import Options
 
    class Fruit(Options):
        APPLE = 1
        ORANGE = 2
        BANANA = 3 
    ```
    
    Try the following in Python command line:
    
    ```
    >>> from optenum import Option, Options
    >>> class Fruit(Options):
    ...     APPLE = 1
    ...     ORANGE = 2
    ...     BANANA = 3
    >>> 
    >>> Fruit.APPLE
    <Option code=1 name=APPLE text=None>
    >>> print(Fruit.APPLE)
    1
    >>> Fruit.APPLE.code
    1
    >>> Fruit.APPLE.name
    'APPLE'
    >>> Fruit.APPLE.text
    >>> print(Fruit.APPLE.text)
    None
    >>> Fruit.APPLE.get_text()
    'apple'
    
    ```

2. Complex declaration

    You may declare your Options (Enums) in many annotations.

    ```python
    from optenum import Option, Options
 
    class EnumCellPhone(Options):
        APPLE = 1
        SAMSUNG = Option(2, name='SAMSUNG')
        HUAWEI = 3, 'Huawei cellphone'     # tuple annotation. name = code, text
    
    
    class DoorState(Options):
        OPEN = 'O', 'Door is opened'       # tuple annotation. name = code, text
        CLOSED = ('C', 'Door is closed')   # tuple annotation, too.
        IN_OPENING = 'IO'
        IN_CLOSING = 'IC'
    
        _FLAG = False           # underscore leading name is not an option
        x = lambda y: y         # function/callable is not an option
    ```

3. Operators

    `Option` support some operators. See more in [operators.md](https://github.com/samuelchen/optenum/blob/master/docs/operators.md).
    
    ```
    >>> class Favorite(Options):
    ...     APPLE = 1
    ...     BANANA = 3, 'Banana hot'
    ... 
    >>> 
    >>> Fruit.APPLE == Favorite.APPLE
    True
    >>> Fruit.BANANA == Favorite.BANANA
    False
    >>> Fruit.APPLE + 1 == Fruit.ORANGE
    True>>> Fruit.BANANA >> 2
    0
    >>> Fruit.BANANA << 2
    12>>> Fruit.BANANA > Favorite.APPLE
    True
    ```

4. Collections

    `Options` provides some collections for accessing option and it's fields.
    See section "Collections for Options" below for more information.
    
    ```
    >>> Fruit.codes
    [1, 2, 3]
    >>> Fruit.names
    ['ORANGE', 'APPLE', 'BANANA']
    >>> Fruit.all
    [<Option code=2 name=ORANGE text=None>, <Option code=1 name=APPLE text=None>, <Option code=3 name=BANANA text=None>]
    >>> Fruit.tuples
    [('ORANGE', 2, None), ('APPLE', 1, None), ('BANANA', 3, None)]
    >>> Favorite.items
    {'APPLE': <Option code=1 name=APPLE text=None>, 'BANANA': <Option code=3 name=BANANA text=Banana hot>}
    >>> Favorite.get_list('code','text')
    [(1, None), (3, 'Banana hot')]
    >>> Favorite.get_dict('name','text')
    {'APPLE': None, 'BANANA': 'Banana hot'}
    
    ```

5. Django model choices

        To be written

# Background

Often we need to define some enums or options. But looks python missing this class.
Sometimes we uses class, tuples or dict as the replacement. But they are not convenience.

For example, we could define a class as enumeration. We can use `MyOption.foo` to get the enum value `1`.

```python
class MyOption(object):
    foo = 1
    bar = 2
```
But how can we get the enum name foo ? How can we get the list of all enums ? Even list of tuples `[ (1, 'foo'), (2, 'bar')]` (useful in Django model)

Although Python 3.7 comes with [data classes](https://docs.python.org/3/whatsnew/3.7.html#whatsnew37-pep557). So far it looks like a piece of syntax sugar for me and it can not solve these problems.

# Features

  * Code - Enumeration/options by different types - e.g. 0, 1, -1 (or 'new', 'running', 'stopped')
  * Name - Name of an enum/option - e.g.  'NEW', 'RUNNING', 'STOPPED'. Support dot access. 
  * Text - Meaning or description of the enum/option. support i18n - e.g. _('new'), _('running'), _('stopped') (translated to '新建', '运行中', ‘停止中’)
  * List - Retrieve list of code, name or text `[0, 1, -1]`
  * Dict - Retrieve dict of `{code: name}` mapping. even `{code: text}`, `{name: text}` mapping if required.
  * List of tuples - Retrieve list of `[(code, name), ...]` tuples. Useful in **Django** model.
  * Operators support - e.g. `Fruit.APPLE == 1`, `Fruit.BANANA > Fruit.APPLE`
  * Grouping - Group a set of enums/options. e.g. IN_PROGRESS_STATE = ['STARTING', 'STOPPING'], but 'STARTED' and 'STOPPED' are not belongs to it.
  * Access **name**, **text** by **code**
  * Lookup enum/option by **name**, **code**
  
# Guide / Tutor

# Type converting for `Option`

    since v1.1.1

An `Option` instance will be constructed dynamically. Optenum will construct a new sub type 
`Option(?)` class based on your option value(`code`) to initialize the new instance object.  

For example, `Option(code=1, name='APPLE', text='an apple')` will construct a class `Option(int)`.
The `int` is your `code`'s type. If your option is for a string, e.g. `Option('A', 'ADMIN', 'Administration user')`,
an `Option(str)` class will be constructed internally.

The internal `Option(?)` class is derived from either `Option` and `?` (e.g. `int`). That means you can use 
`isinstance` to check your object. For example, says we have `apple = Option(1, 'APPLE', 'an apple')`. Then
 `isinstance(apple, int)` is `True`. And `isinstance(apple, Option)` is `True`, too. So that you can use
 your option as its value(`code`) is such in `dict` as key and so on.
 

    Deprecated since v1.1.0
    
    `str()` or implicit string converting will convert `Option.code` to string type and returns. ~
    
    `repr()` will returns the object as string format of `<Option code=??? name=??? text=???>`.
    
    `int`, `float` will be performed on `Option.code` and returns the value or raises corresponding exception.

# Boolean for `Option`

    Deprecated since v1.1.0
    No special implementation. It behaves as `object` is.

# Group and tags 

See [this doc](https://github.com/samuelchen/optenum/blob/master/docs/tag-and-group.md).

# Operators for `Option`

Since v1.1.1, an `Option` behaves as its value(`code`) is. So it will support all operators its `code` supports.

    Deprecated since v1.1.0
    
    `Option.code` is the real value of the enum/option item. Somehow we need to use codes 
    like `if active_state == MyOption.RUNNING.code:  # Do something ...` to check the status. For convenience using it, some of the operators
    are override. Then we could use `if active_state == MyOption.RUNNING:`, `x = MyOption.RUNNING + 1` and so on to
    directly reference to its real value.
    
    See doc [operators.md](https://github.com/samuelchen/optenum/blob/master/docs/operators.md) for override operators.

# Collections for `Options`

Option can be accessed directly as subscribe annotation. For example `Option['FOO']`
equals to `Option.FOO`.

We could also access the following collections from within an Options class. 

  * `Options.codes` - list of codes
    
  * `Options.names` - list of names
  
  * `Options.all` - list of options

  * `Options.tuples` - list of (`name`, `code`, `text`) tuple

  * `Options.items` - dict of {`name`: `Option`} mapping

  * `Options.get_list(*fields)` - list of *files tuple. *fields are names of Option filed 
  such as `code`, *(`name`, `code`) or *(`code`, `name`, `text`)
  
  * `Options.get_dict(key_field, *fields)` - dict of `{key_filed: (*fields)}` (`{str: tuple}`) mapping.
  `key_field` specify which Option field is key such as `name`, `code`. 
  `fields` specify the value tuple combined of which Option fields such as (`name`, `text`) or `name`.
  if fields is tuple, the value is tuple. if fields is single filed, value is single field.

    Deprecated since v1.1.0
    
    `in` operator could check if a `code` in `Options`. e.g. `if Fruit.APPLE in Fruit`.
    The `Option.name` will not work. e.g. `if 'APPLE' in Fruit` will got `False`. 
    If you want to check if name in `Options`), use collection instead. 
    e.g. `if 'APPLE' in Fruit.names`.


# Configuration

Some flags can be used to make some simple configuration to your Options.

  * `__IGNORE_INVALID_NAME__` - Ignore invalid `Option` name so that you may add your own attribute/function to class.
  
    Underscore `_` leading attributes and any functions will be ignored so that you can add your own attributes and 
    functions. The following example is valid definition.
    
    ```python
    from optenum import Options

    class MyEnum(Options):
        FOO = 1
        BAR = 2
        
        _flag = False
        
        def switch(self):
            pass
    ```
    
    But if an attributes is not uppercase (all characters), it will be treat as invalid `Option` and cause exception.
    
    ```python
    from optenum import Options

    class MyEnum(Options):
        FOO = 1
        BAR = 2
        
        Baz = 3     # <- Invalid Option name. Exception raised.
    ```
    
    If you want this available, add `__IGNORE_INVALID_NAME__` to your class like below. The exception will ignored.
    But to be noticed, it still not an `Option`.
  
    ```python
    from optenum import Options

    class MyEnum(Options):
        __IGNORE_INVALID_NAME__ = True
        
        FOO = 1
        BAR = 2
        
        Baz = 3     # <- Exception ignored. But still not an Option.
    ```
  
  * `__ORDER_BY__`
  
        Not supported yet

# FAQ

* Why not use *namedtuple* ?

*namedtuple* is also a good way to define enum/options. But it has not enough features
you may required such as *collection*, *operator*, *compare*, *text* and so on.

* Why only uppercase allowed for Option name ?

Because you can define other none-option attributes if sets `__IGNORE_INVALID_NAME__` to `True`.
And enumerations commonly are defined with uppercase identifier.

# Contributors

List of contributors:

* Samuel Chen - The project owner and maintainer.