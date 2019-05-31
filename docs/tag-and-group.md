# Grouping `Option`s with `tags`

        supported from v1.1.2
        
Sometimes, we want to group some options together. Somehow we ccould do it as this:

```python
from optenum import Options

class MyFavorites(Options):
  APPLE = 1, 'APPLE'
  BANANA = 2, 'BANANA'
  FOOTBALL = 'F', 'FOOTBALL'
  BASKETBALL = 'B', 'BASKETBALL'

  __IGNORE_INVALID_NAME__ = True
  Fruits = (APPLE, BANANA)
  Sports = (FOOTBALL, BASKETBALL)
  All = Fruits + Sports
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
    APPLE = Option(1, 'APPLE', _('Apple'), tags=['fruit', 'red'])
    BANANA = 2, _('Banana'), ('fruit', 'yellow')
    FOOTBALL = 'F', _('Football'), ('sport', 'white')
    BASKETBALL = 'B', _('Basketball'), ('sport', 'red')


# now try get tags
print(MyFavorites.APPLE.tags)  # ('fruit', 'red')

# add new tag
MyFavorites.APPLE.add_tag('bad')
print(MyFavorites.APPLE.tags)  # ('fruit', 'red', 'good')

# remove a tag
MyFavorites.APPLE.remove_tag('bad')
print(MyFavorites.APPLE.tags)  # ('fruit', 'good')
```

        Note: add/remove tag will cause re-group options.

## Group

And you may also access grouped options by using tag name:

```python

# MyFavorites declaration as above

print(MyFavorites.fruit)        # (1, 2)
print(MyFavorites.white)         # ('F', )
print(MyFavorites.red)         # (1, 'B')

# add new tag and group
MyFavorites.APPLE.add_tag('GOOD')
print(MyFavorites.GOOD)         # (1, )
MyFavorites.FOOTBALL.add_tag('GOOD')
print(MyFavorites.GOOD)         # (1, 'F')

# remove a tag
MyFavorites.APPLE.remove_tag('red')
print(MyFavorites.red)         # ('B', )

```