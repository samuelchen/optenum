# Grouping `Option`s with `tags`

        supported from v1.1.2
        
Sometimes, we want to group some options together. Somehow we could do it as this:

```python
from optenum import Options

class MyFavorites(Options):
  APPLE = 1, 'APPLE'
  BANANA = 2, 'BANANA'
  FOOTBALL = 'F', 'FOOTBALL'
  BASKETBALL = 'B', 'BASKETBALL'

  __IGNORE_INVALID_NAME__ = True
  FRUITS = (APPLE, BANANA)
  SPORTS = (FOOTBALL, BASKETBALL)
  All = FRUITS + SPORTS
```

But it's not convenience because:

* Need specify `__IGNORE_INVALID_NAME__`
* The grouped values are built-in types not Option objects.
* Group name can not be full uppercase.

So `tags` is introduced to archive this.

## Tags

An Option object can be initialized with `tags` argument. It accept list or tuple of string tags.

So your above Options can be declared as below:

```python
from optenum import Options, Option
from gettext import gettext as _


class MyFavorites(Options):
    APPLE = Option(1, 'APPLE', _('Apple'), tags=['FRUITS', 'RED'])
    BANANA = 2, _('Banana'), ('FRUITS', 'YELLOW')
    FOOTBALL = 'F', _('Football'), ('SPORTS', 'WHITE')
    BASKETBALL = 'B', _('Basketball'), ('SPORTS', 'RED')


# now try get tags
print(MyFavorites.APPLE.tags)  # ('FRUITS', 'RED')

# add new tag
MyFavorites.APPLE.add_tag('BAD')
print(MyFavorites.APPLE.tags)  # ('FRUITS', 'RED', 'BAD')

# remove a tag
MyFavorites.APPLE.remove_tag('BAD')
print(MyFavorites.APPLE.tags)  # ('FRUITS', 'RED')
```

        Note: add/remove tag will cause re-grouping options.

## Group

And you may also access grouped options by using tag name:

```python

# MyFavorites declaration as above

print(MyFavorites.FRUITS)        # (1, 2)
print(MyFavorites.WHITE)         # ('F', )
print(MyFavorites.RED)         # (1, 'B')

# add new tag and group
MyFavorites.APPLE.add_tag('GOOD')
print(MyFavorites.GOOD)         # (1, )
MyFavorites.FOOTBALL.add_tag('GOOD')
print(MyFavorites.GOOD)         # (1, 'F')

# remove a tag
MyFavorites.APPLE.remove_tag('RED')
print(MyFavorites.RED)         # ('B', )

```

We could also define *tags* and *group* options as the following annotation.

```python
from optenum import Options, Option, OptionGroup as G
from gettext import gettext as _


class MyFavorites(Options):
    APPLE = Option(1, 'APPLE', _('Apple'), tags=['FRUITS', 'RED'])
    BANANA = 2, _('Banana')
    FOOTBALL = 'F', _('Football')
    BASKETBALL = 'B', _('Basketball')
    
    FRUITS = G(APPLE, BANANA)
    SPORTS = G(FOOTBALL, BASKETBALL)


# now try get tags
print(MyFavorites.BANANA.tags)  # ('FRUITS',)

# access group
print(MyFavorites.FRUITS)  # (APPLE, BANANA) -> (1, 2)

```