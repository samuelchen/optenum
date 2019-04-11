# Supported Operators of `Option`

  `Option.code` is the real value of the enum/option item. Somehow we need to use codes 
  like `if active_state == MyOption.RUNNING ...` to check the status. For convenience using it, some of the operators
  are override. 
  
  To give example for operators, the following options (Fruit and Balls) will be used.
  
  ```python

# Here it inherits from "object" for simple example. 
# Better to use "Options" as parent class to leverage the features.

class Fruit(object):
    APPLE = Option(1, 'APPLE', 'Apple')
    ORANGE = Option(2, 'ORANGE', 'Orange')
    BANANA = Option(3, 'BANANA', 'Banana')
    PEAR = Option(-1, 'PEAR', 'Pear')
    MONGO = Option(-2.1, 'MONGO', 'Mongo')
    WATERMELON = Option(0, 'WATERMELON', 'Watermelon')
    
    
class Ball(object):
    FOOTBALL = Option('F', 'FOOTBALL')
    BASKETBALL = Option('B', 'BASKETBALL')
    PING_PONG = Option('P', 'PING_PONG')
    TENNIS = Option('10', 'TENNIS')
    
class CellPhone(object):
    APPLE = Option(1, 'APPLE', 'iPhone')
    HUAWEI = Option(2, 'HUAWEI', 'Honer')
    SAMSUNG = Option(3, 'SAMSUNG', 'Galaxy')

  ```

## Math operators

  * Negative -
  
  Available when `Option.code` is **number** type.
  
  ```python
>>> - Fruit.APPLE
-1

>>> - Fruit.PEAR
1

>>> - Ball.BASKETBALL
Traceback (most recent call last):
  ...
TypeError: '-(negative)' not supported on instances of 'Option(str)'

  ```
  
  * Positive +
  
  Available when `Option.code` is **number** type.
  
  ```python
>>> + Fruit.APPLE
1

>>> + Fruit.PEAR
-1

>>> + Ball.BASKETBALL
Traceback (most recent call last):
    ...
TypeError: '+(positive)' not supported on instances of 'Option(str)'

  ```
  
  * Add +
  
    Available when `Option.code` is **number** type and the `other` variable is also **number** type.
    Or both are **string** types. Explicit use `str()`, `float()`, `int()` or other functions to convert 
    the variables first if you want number type to add string type. 
  
  ```python
>>> Fruit.PEAR + 1
0

>>> Fruit.APPLE + 1
2

>>> 2 + Fruit.BANANA
5

>>> Fruit.ORANGE + Fruit.BANANA
5

>>> Fruit.APPLE + '1'
Traceback (most recent call last):
    ...
TypeError: '+' not supported between instances of 'Option(int)' and 'str'

>>> Ball.BASKETBALL + 1
Traceback (most recent call last):
    ...
TypeError: '+' not supported between instances of 'Option(str)' and 'int'

>>> Ball.BASKETBALL + ' is basket ball.'
'B is basket ball.'

>>> Ball.BASKETBALL + Ball.FOOTBALL
'BF'

>>> Fruit.APPLE + int('1')
2

>>> Fruit.APPLE + float('1')
2.0

>>> str(Fruit.APPLE) + Ball.FOOTBALL
'F1'

  ```
  
  * Sub -
  
    Available when `Option.code` is **number** type and the `other` variable is also **number** type.
    Or both are **string** types. Explicit use `str()`, `float()`, `int()` or other functions to convert 
    the variables first if you want number type to add string type.
  
  ```python
>>> Fruit.PEAR - 1
-1

>>> Fruit.APPLE - 1
0

>>> 2 - Fruit.BANANA
-1

>>> Fruit.ORANGE - Fruit.BANANA
-1

>>> Fruit.APPLE - '1'
Traceback (most recent call last):
    ...
TypeError: '-' not supported between instances of 'Option(int)' and 'str'

>>> Ball.BASKETBALL - 1
Traceback (most recent call last):
    ...
TypeError: '-' not supported between instances of 'Option(str)' and 'int'

>>> Ball.BASKETBALL - ' is basket ball.'
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for -: 'str' and 'str'

>>> Ball.BASKETBALL - Ball.FOOTBALL
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for -: 'str' and 'str'

>>> Fruit.APPLE - int('1')
0

>>> Fruit.APPLE - float('1')
0.0

>>> int(Ball.TENNIS) - Fruit.APPLE
9

>>> int(Ball.FOOTBALL) - 1
Traceback (most recent call last):
    ...
ValueError: invalid literal for int() with base 10: 'F'

  ```

  
  * Multiple *
  
    Available when `Option.code` is **number** type and the `other` variable is also **number** type.
    Or `Option.code` is **string** type and the `other` variable is **integer** type.
  
  ```python
>>> Fruit.PEAR * 2
-2

>>> 2 * Fruit.BANANA
6

>>> Fruit.ORANGE - Fruit.BANANA
-1

>>> Fruit.APPLE * '1'
Traceback (most recent call last):
    ...
TypeError: '*' not supported on instances of 'str'

>>> Ball.BASKETBALL * 3
'BBB'
>>> Ball.BASKETBALL * Fruit.ORANGE
'BB'
  ```

  * Division / and Floor Division //
  
    Available when `Option.code` is **number** type and the `other` variable is also **number** type.
    
    Note:

        In Python 2, the division will behave like floor division (e.g. `5 / 2 = 2`). 
        Only when you `from __future__ import division`, it will behaves as true division (e.g. `5 / 2 = 2.5`). 
        In python 3, it behaves as second one. 
  
  Python 2.7 examples
  
  ```python
>>> Fruit.PEAR / 2
-1

>>> 2 / Fruit.BANANA
0

>>> from __future__ import division

>>> Fruit.PEAR / 2
-0.5

>>> 2 / Fruit.BANANA
0.6666666666666666

>>> Fruit.BANANA / 0
Traceback (most recent call last):
    ...
ZeroDivisionError: division by zero

>>> Ball.TENNIS / 2
Traceback (most recent call last):
    ...
TypeError: '/' not supported on instances of 'Option(str)'

>>> int(Ball.TENNIS) / 2
5.0
  ```    
  Python 3 examples
    
```python

>>> Fruit.PEAR / 2
-0.5
>>> 2 / Fruit.BANANA
0.6666666666666666

>>> Fruit.BANANA / 0
Traceback (most recent call last):
    ...
ZeroDivisionError: division by zero

>>> Ball.TENNIS / 2
Traceback (most recent call last):
    ...
TypeError: '/' not supported on instances of 'Option(str)'

>>> int(Ball.TENNIS) / 2
5.0
```

  Floor Division examples
  

```python
>>> Fruit.BANANA // 2
1

>>> 5 // Fruit.ORANGE
2

>>> int(Ball.TENNIS) // 3
3

>>> 4 / Fruit.WATERMELON
Traceback (most recent call last):
    ...
ZeroDivisionError: division by zero
```


  * Mod %
  
    Available when `Option.code` is **integer** type and the `other` variable is also **integer** type.
  
  ```python
>>> Fruit.PEAR % 2
1

>>> 5 % Fruit.BANANA
2

>>> Fruit.ORANGE % 1.5
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for %: 'Option' and 'float'

>>> 3.5 % Fruit.BANANA
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for %: 'float' and 'Option'

>>> Ball.BASKETBALL % 2
Traceback (most recent call last):
    ...
TypeError: '%' not supported on instances of 'Option(str)'

  ```
  
  * divmod
  
    Available when `Option.code` is **integer** type and the `other` variable is also **integer** type.
  
  ```python
>>> divmod(Fruit.ORANGE,  3)
(0, 2)

>>> divmod(5, Fruit.BANANA)
(1, 2)

>>> divmod(5.5, Fruit.BANANA)
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for divmod(): 'float' and 'Option'

>>> divmod(Fruit.ORANGE,  3.5)
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for divmod(): 'Option' and 'float'

>>> divmod(Ball.BASKETBALL,  3)
Traceback (most recent call last):
    ...
TypeError: '%' not supported on instances of 'Option(str)'

  ```
  
  
  * abs
  
    Available when `Option.code` is **number** type and the `other` variable is also **number** type.
  
  ```python
>>> abs(Fruit.ORANGE)
2

>>> abs(Fruit.PEAR)
1

>>> Fruit.PEAR
<Option code=-1 name=PEAR text=Pear>

>>> abs(Fruit.MONGO)
2.1

>>> abs(Ball.FOOTBALL)
Traceback (most recent call last):
    ...
TypeError: 'abs' not supported on instances of 'Option(str)'

  ```    
  

## Logic Operators

Logic operators are not override. They will perform as the object logic operators. 

  * equal == (and !=)
    
  When comparing between 2 `Option` objects, it will compare `code`, `name` and `text`.
  Only if 3 fields are all same, it will returns `True`, otherwise returns `False`.
  
  Here I add a new class for example
    
  ```python
    class Favorite(object):
        APPLE = Option(1, 'APPLE', 'Apple')
        BANANA = Option(2, 'BANANA', 'Banana')
  ```

  You will see the difference.
    
  ```python
    >>> Fruit.APPLE == Favorite.APPLE
    True
    >>> Fruit.APPLE is Favorite.APPLE
    False
    >>> Fruit.BANANA == Favorite.BANANA
    False
    >>> Fruit.BANANA != Favorite.BANANA
    True
  ```

  * is
  
  No special implementation for `is`. It behaves as `object`.  

  * Greater(Equal), Less(Equal), >, >=, <, <=
  
  Comparing 2 `Option` objects means to compares their `code`.
  Comparing an `Option` objects with another type object means to compare the `Option.code` to the other object.

  * and, or
  
  No special implementation for `and` and `or` operators. It behaves as its.
  
  ```python
    >>> Fruit.APPLE and Favorite.BANANA
    <Option code=2 name=BANANA text=Banana>
    >>> Fruit.APPLE or Favorite.BANANA
    <Option code=1 name=APPLE text=Apple>
  ```

## Bit Operators

  * invert ~

    Available when `Option.code` is **integer** type .
  
```python
  
>>> ~ Fruit.APPLE
-2

>>> ~ Fruit.MONGO
Traceback (most recent call last):
    ...
TypeError: '~' not supported on instances of 'Option(float)'

>>> ~ Fruit.PEAR
0

>>> ~ Ball.FOOTBALl
Traceback (most recent call last):
    ...
AttributeError: type object 'Ball' has no attribute 'FOOTBALl'

```

  * left shift <<

    Available when `Option.code` is **integer** type and the `other` variable is also **integer** type.
  
```python
  
>>> Fruit.APPLE << 2
4

>>> 3 << Fruit.ORANGE
12

>>> Fruit.MONGO << 2
Traceback (most recent call last):
    ...
TypeError: '<<' not supported on instances of 'Option(float)'

>>> Fruit.PEAR << 1
-2

>>> Ball.FOOTBAL << 2
Traceback (most recent call last):
    ...
AttributeError: type object 'Ball' has no attribute 'FOOTBAL'


```


  * right shift >>

    Available when `Option.code` is **integer** type and the `other` variable is also **integer** type.
  
```python

>>> Fruit.APPLE >> 2
0

>>> 32 >> Fruit.ORANGE
8

>>> Fruit.MONGO >> 1
Traceback (most recent call last):
    ...
TypeError: '>>' not supported on instances of 'Option(float)'

>>> Ball.FOOTBALL >> 1
Traceback (most recent call last):
    ...
TypeError: '>>' not supported on instances of 'Option(str)'

```