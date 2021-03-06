# from __future__ import division
import unittest
import six
from optenum import Option


class Fruit(object):
    APPLE = Option(1, 'APPLE', 'Apple')
    ORANGE = Option(2, 'ORANGE', 'Orange')
    BANANA = Option(3, 'BANANA', 'Banana')
    PEAR = Option(-1, 'PEAR', 'Pear')
    MONGO = Option(-2.1, 'MONGO', 'Mongo')
    WATERMELON = Option(0, 'WATERMELON', 'Watermelon')


class CellPhone(object):
    APPLE = Option(1, 'APPLE', 'Apple iPhone')
    HUAWEI = Option(2, 'HUWEI', 'Huawei Hornor')
    SAMSUNG = Option(3, 'SAMSUNG', 'Samsung Galaxy')


class Ball(object):
    FOOTBALL = Option('F', 'FOOTBALL')
    BASKETBALL = Option('B', 'BASKETBALL')
    PING_PONG = Option('P', 'PING_PONG')


class Favorite(object):
    APPLE = Option(1, 'APPLE', 'Apple')
    BANANA = Option(2, 'BANANA', 'Banana')


store = {
    1: '10 Apples',         # Apple = 1
    2: '20 Bananas',        # Banana = 2 
    'F': '4 Footballs',     # Football = 'F'
    'B': '3 Basketballs',   # Basketball = 'B'
    Ball.PING_PONG: '1 PingPong',    # PingPong Option object (hash is 'P')
    'P': 'PPP'
}


class TestOption(unittest.TestCase):

    def raiseAssert(self, e):
        raise AssertionError('Should raise %s' % e)

    # def test_not_defined(self):
    #     self.assertIsInstance(Option.NOT_DEFINED, Option)
    #     self.assertIs(Option.NOT_DEFINED.code, None)

    def test_option(self):
        opt = Option(1, 'FOO')
        self.assertIs(opt.code, 1)
        self.assertEqual(str(opt), '1')
        self.assertIsInstance(opt, Option)
        self.assertTrue(issubclass(type(opt), Option))

    def test_option_tags(self):
        opt = Option(1, 'FOO', tags=['FOO', 'BAR_1', 'BA1Z', 'QUX'])
        self.assertIn('FOO', opt.tags)
        self.assertIn('BAR_1', opt.tags)
        self.assertIn('BA1Z', opt.tags)
        self.assertIn('QUX', opt.tags)

    def test_get_text(self):
        opt = Option(code=1, name='OPT')
        self.assertEqual(opt.get_text(), 'OPT')
        opt = Option(code=1, name='OPT', text='')
        self.assertEqual(opt.get_text(), '')
        opt.text = 'An Option'
        self.assertEqual(opt.get_text(), 'An Option')

    def test_option_invalid_code_type(self):
        self.assertRaises(TypeError, Option, *([1, 2, 3], ))
        self.assertRaises(TypeError, Option, *({'foo': 'bar'}, ''))

    def test_option_code_name(self):
        self.assertRaises(ValueError, Option, *(None, 'FOO'))
        self.assertRaises(ValueError, Option, *(1, None))
        self.assertRaises(ValueError, Option, *(None, None, 'bar'))

    def test_option_name_text(self):
        opt = Option('O', 'OPEN', 'Opened')
        self.assertIs(opt.code, 'O')
        self.assertIs(opt.name, 'OPEN')
        self.assertIs(opt.text, 'Opened')
        self.assertEqual(str(opt), 'O')

    def test_invalid_name(self):
        self.assertRaises(ValueError, Option, *(1, '_FOO'))
        self.assertRaises(ValueError, Option, *(1, 'Foo'))
        self.assertRaises(ValueError, Option, *(1, 'Fo.o'))
        self.assertRaises(ValueError, Option, *(1, '1Foo'))
        self.assertRaises(ValueError, Option, *(1, 'FOO_1a'))

    def test_op_is(self):
        self.assertIsNot(Fruit.APPLE, CellPhone.APPLE)

    # compare op

    def test_op_cmp(self):
        options = [Fruit.BANANA, Fruit.APPLE, Fruit.ORANGE]
        options = sorted(options)
        self.assertIs(options[0], Fruit.APPLE)
        #
        # if six.PY2:
        #     self.assertEqual(Fruit.BANANA.__cmp__(Fruit.ORANGE), 1)
        #     self.assertEqual(Fruit.APPLE.__cmp__(CellPhone.APPLE), 0)
        #     self.assertEqual(Fruit.BANANA.__cmp__(Favorite.APPLE), -1)

    def test_op_eq(self):
        self.assertEqual(Fruit.APPLE, 1)
        self.assertEqual(CellPhone.APPLE, 1)
        self.assertEqual(Fruit.APPLE, Favorite.APPLE)
        # self.assertNotEqual(Fruit.BANANA, Favorite.BANANA)
        self.assertNotEqual(Fruit.BANANA, Favorite.BANANA)
        self.assertEqual(Fruit.APPLE, CellPhone.APPLE)
        self.assertEqual(Fruit.APPLE.code, CellPhone.APPLE.code)

    def test_op_lt(self):
        self.assertLess(Fruit.APPLE, 2)
        self.assertLess(Fruit.ORANGE, Fruit.BANANA)
        self.assertLess(1.5, Fruit.ORANGE)
        self.assertLess(Fruit.APPLE, CellPhone.SAMSUNG)
        self.assertLess(Ball.BASKETBALL, 'T')
        try:
            self.assertLess(Ball.FOOTBALL, Fruit.BANANA)
            self.raiseAssert((TypeError, AssertionError))
        except Exception as e:
            self.assertIsInstance(e, (TypeError, AssertionError))
        try:
            self.assertLess(Ball.FOOTBALL, 2)
            self.raiseAssert((TypeError, AssertionError))
        except Exception as e:
            self.assertIsInstance(e, (TypeError, AssertionError))
        # self.assertRaises(TypeError, Ball.FOOTBALL.__lt__, Fruit.BANANA)
        # self.assertRaises(TypeError, Ball.FOOTBALL.__lt__, 2)

    def test_op_le(self):
        self.assertLessEqual(Fruit.APPLE, 2)
        self.assertLessEqual(Fruit.ORANGE, Fruit.BANANA)
        self.assertLessEqual(2, Fruit.ORANGE)
        self.assertLessEqual(Fruit.APPLE, CellPhone.APPLE)
        self.assertLessEqual(Ball.BASKETBALL, 'B')

        try:
            self.assertLessEqual(Ball.FOOTBALL, Fruit.BANANA)
            self.raiseAssert((TypeError, AssertionError))
        except Exception as e:
            self.assertIsInstance(e, (TypeError, AssertionError))
        try:
            self.assertLessEqual(Ball.FOOTBALL, 2)
            self.raiseAssert((TypeError, AssertionError))
        except Exception as e:
            self.assertIsInstance(e, (TypeError, AssertionError))

        # self.assertRaises(TypeError, Ball.FOOTBALL.__le__, Fruit.BANANA)
        # self.assertRaises(TypeError, Ball.FOOTBALL.__le__, 2)

    def test_op_gt(self):
        self.assertGreater(Fruit.APPLE, 0)
        self.assertGreater(Fruit.ORANGE, Fruit.APPLE)
        self.assertGreater(3.5, Fruit.ORANGE)
        self.assertGreater(Fruit.BANANA, CellPhone.APPLE)
        self.assertGreater(Ball.BASKETBALL, '1')

        try:
            self.assertGreater(Ball.FOOTBALL, Fruit.BANANA)
            if six.PY3:
                # Only for PY3. Because comparision between str and int is available in Python 2.7
                self.raiseAssert(TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)

        try:
            self.assertGreater(Ball.FOOTBALL, 2)
            if six.PY3:
                # Only for PY3. Because comparision between str and int is available in Python 2.7
                self.raiseAssert(TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)

        # self.assertRaises(TypeError, Ball.FOOTBALL.__gt__, Fruit.BANANA)
        # self.assertRaises(TypeError, Ball.FOOTBALL.__gt__, 2)

    def test_op_ge(self):
        self.assertGreaterEqual(Fruit.APPLE, -1.5)
        self.assertGreaterEqual(Fruit.ORANGE, Fruit.APPLE)
        self.assertGreaterEqual(2, Fruit.ORANGE)
        self.assertGreaterEqual(Fruit.BANANA, CellPhone.APPLE)
        self.assertGreaterEqual(Ball.PING_PONG, 'Jump')

        try:
            self.assertGreaterEqual(Ball.FOOTBALL, Fruit.BANANA)
            self.raiseAssert((TypeError, AssertionError))
        except Exception as e:
            self.assertIsInstance(e, (TypeError, AssertionError))

        try:
            self.assertGreaterEqual(Ball.FOOTBALL, 2.1)
            self.raiseAssert((TypeError, AssertionError))
        except Exception as e:
            self.assertIsInstance(e, (TypeError, AssertionError))

        # self.assertRaises(TypeError, Ball.FOOTBALL.__ge__, Fruit.BANANA)
        # self.assertRaises(TypeError, Ball.FOOTBALL.__ge__, 2.1)

    # math op

    def test_op_neg(self):
        self.assertEqual(- Fruit.APPLE, -1)
        self.assertEqual(- Fruit.PEAR, 1)
        try:
            -Ball.BASKETBALL
            self.assertIsInstance(e, TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)
        # self.assertRaises(TypeError, Ball.BASKETBALL.__neg__)

    def test_op_pos(self):
        self.assertEqual(+ Fruit.APPLE, 1)
        self.assertEqual(+ Fruit.PEAR, -1)
        self.assertEqual(+ Fruit.APPLE, Fruit.APPLE)
        try:
            +Ball.BASKETBALL
            self.assertIsInstance(e, TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)
        # self.assertRaises(TypeError, Ball.BASKETBALL.__pos__)

    def test_op_abs(self):
        self.assertEqual(abs(Fruit.APPLE), 1)
        self.assertEqual(abs(Fruit.PEAR), 1)
        self.assertEqual(abs(Fruit.APPLE), Fruit.APPLE)
        self.assertRaises(TypeError, abs, Ball.BASKETBALL)

    def test_op_int(self):
        self.assertEqual(int(Fruit.APPLE), 1)
        self.assertEqual(int(Fruit.MONGO), -2)
        self.assertEqual(int(Fruit.APPLE), Fruit.APPLE)
        self.assertRaises(ValueError, int, Ball.BASKETBALL)

    def test_op_float(self):
        self.assertEqual(float(Fruit.APPLE), 1.0)
        self.assertEqual(float(Fruit.MONGO), -2.1)
        self.assertEqual(float(Fruit.APPLE), Fruit.APPLE)
        self.assertRaises(ValueError, float, Ball.BASKETBALL)

    def test_op_invert(self):
        self.assertEqual(~ Fruit.APPLE, -2)
        self.assertEqual(~ Fruit.PEAR, 0)
        try:
            ~ Fruit.MONGO
            self.assertIsInstance(e, TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)
        self.assertRaises(ValueError, float, Ball.BASKETBALL)

    def test_op_add(self):
        self.assertEqual(Fruit.APPLE + 1, Fruit.ORANGE)
        self.assertEqual(1 + Fruit.ORANGE, Fruit.BANANA)
        self.assertEqual(Fruit.BANANA + 1.5, 4.5)
        self.assertEqual(1.2 + Fruit.APPLE, 2.2)

    def test_op_sub(self):
        self.assertEqual(Fruit.BANANA - 1, Fruit.ORANGE)
        self.assertEqual(3 - Fruit.ORANGE, Fruit.APPLE)
        self.assertEqual(Fruit.BANANA - 1.2, 1.8)
        self.assertEqual(4.2 - Fruit.ORANGE, 2.2)

    def test_op_mul(self):
        self.assertEqual(Fruit.APPLE * 2, 2)
        self.assertEqual(Fruit.MONGO * 2, -4.2)
        self.assertEqual(2 * Fruit.APPLE * 1.5, Fruit.BANANA)
        self.assertEqual(Ball.BASKETBALL * 2, 'BB')
        self.assertEqual(2 * Ball.BASKETBALL, 'BB')
        # self.assertRaises(TypeError, Fruit.APPLE.__mul__, *('1',))
        # self.assertRaises(TypeError, Ball.BASKETBALL.__mul__, *('1', ))

    def test_op_div(self):
        if 1 == 3 / 2:
            division_loaded = False
        else:
            division_loaded = True

        if six.PY2 and not division_loaded:
            self.assertEqual(Fruit.APPLE / 2, 0)
            self.assertEqual(Fruit.BANANA / 2, 1)
            self.assertEqual(3 / Fruit.ORANGE, 1)
            # self.assertRaises(TypeError, Ball.BASKETBALL.__div__, *(2,))
            # self.assertRaises(ZeroDivisionError, Fruit.APPLE.__div__, *(0,))
            # self.assertRaises(ZeroDivisionError, Fruit.WATERMELON.__rdiv__, *(3,))
        else:
            self.assertEqual(Fruit.APPLE / 2, 0.5)
            self.assertEqual(Fruit.BANANA / 2, 1.5)
            self.assertEqual(3 / Fruit.ORANGE, 1.5)

            # self.assertRaises(TypeError, Ball.BASKETBALL.__truediv__, *(2, ))
            # self.assertRaises(ZeroDivisionError, Fruit.APPLE.__truediv__, *(0,))
            # self.assertRaises(ZeroDivisionError, Fruit.WATERMELON.__rtruediv__, *(3,))

        try:
            Ball.BASKETBALL / 2
            self.assertIsInstance(e, TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)
        try:
            Fruit.APPLE / 0
            self.assertIsInstance(e, ZeroDivisionError)
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)

        self.assertEqual(2 / Fruit.APPLE, 2)
        self.assertEqual(Fruit.MONGO / 2, -1.05)
        self.assertEqual(Fruit.ORANGE / 2, Fruit.APPLE)
        self.assertEqual(6 / Fruit.BANANA / 2, Fruit.APPLE)
        self.assertEqual(2 / Fruit.ORANGE, Fruit.APPLE)

        self.assertEqual(2 // Fruit.APPLE, 2)
        self.assertEqual(Fruit.MONGO // 2, -2)
        self.assertEqual(Fruit.ORANGE // 2, Fruit.APPLE)
        self.assertEqual(6 // Fruit.BANANA // 2, Fruit.APPLE)
        self.assertEqual(2 // Fruit.ORANGE, 1)

        try:
            Ball.BASKETBALL // 2
            self.assertIsInstance(e, TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)
        try:
            Fruit.APPLE // 0
            self.assertIsInstance(e, ZeroDivisionError)
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)
        try:
            3 // Fruit.WATERMELON
            self.assertIsInstance(e, ZeroDivisionError)
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)
        # self.assertRaises(TypeError, Ball.BASKETBALL.__floordiv__, *(2, ))
        # self.assertRaises(ZeroDivisionError, Fruit.APPLE.__floordiv__, *(0,))
        # self.assertRaises(ZeroDivisionError, Fruit.WATERMELON.__rfloordiv__, *(3,))

    def test_op_mod(self):
        self.assertEqual(Fruit.MONGO % 2, 1.9)
        self.assertEqual(2 % Fruit.APPLE, 0)
        self.assertEqual(Fruit.BANANA % 2, Fruit.APPLE)
        self.assertEqual(8 % Fruit.BANANA % 3, Fruit.ORANGE)
        self.assertRaises(ZeroDivisionError, Fruit.APPLE.__mod__, *(0,))
        self.assertRaises(ZeroDivisionError, Fruit.WATERMELON.__rmod__, *(3,))

    def test_op_divmod(self):
        self.assertEqual(divmod(Fruit.APPLE, 3), (0, 1))
        self.assertEqual(divmod(3, Fruit.ORANGE), (1, 1))
        self.assertEqual(divmod(Fruit.BANANA, 0.5), (6.0, 0.0))
        try:
            divmod(Fruit.BANANA, '2')
            self.assertIsInstance(e, TypeError)
        except Exception as e:
            self.assertIsInstance(e, TypeError)
        try:
            divmod(Fruit.APPLE, 0)
            self.assertIsInstance(e, ZeroDivisionError)
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)
        try:
            divmod(3, Fruit.WATERMELON)
            self.assertIsInstance(e, ZeroDivisionError)
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)
        # self.assertRaises(TypeError, divmod, *(Fruit.BANANA, 0.5))
        # self.assertRaises(ZeroDivisionError, divmod, *(Fruit.APPLE, 0))
        # self.assertRaises(ZeroDivisionError, divmod, *(3, Fruit.WATERMELON))

    def test_hash(self):
        self.assertEqual(store.get(Fruit.APPLE), '10 Apples')       # Fruit.APPLE hash is 1
        self.assertEqual(store.get(Fruit.BANANA), None)             # Fruit.BANANA hash is 3
        self.assertEqual(store.get(Fruit.ORANGE), '20 Bananas')     # Fruit.ORANGE hash is 2
        self.assertEqual(store.get(Ball.FOOTBALL), '4 Footballs')       # FOOTBALL hash is 'F'
        self.assertEqual(store.get(Ball.BASKETBALL), '3 Basketballs')   
        self.assertEqual(store.get(CellPhone.APPLE), '10 Apples')

        aset = set()
        aset.add(Fruit.APPLE)       # 1
        aset.add(Fruit.ORANGE)      # 2
        aset.add(Ball.FOOTBALL)     # 'F'
        aset.add(Ball.BASKETBALL)   # 'B'

        aset.add(Fruit.APPLE)       # 1
        aset.add(CellPhone.APPLE)   # 1
        aset.add(CellPhone.HUAWEI)  # 2
        aset.add(1)
        aset.add(2)
        aset.add('B')
        self.assertEqual(len(aset), 4)


if __name__ == '__main__':
    unittest.main()
