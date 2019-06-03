import unittest
from optenum import Option, Options, OptionGroup as G


class Fruit(Options):
    APPLE = 1
    ORANGE = 2
    BANANA = 3


class EnumCellPhone(Options):
    APPLE = 1
    SAMSUNG = Option(2, name='SAMSUNG')
    HUAWEI = (3, 'Huawei cellphone')


class DoorState(Options):
    OPEN = 'O', 'Door is opened'
    CLOSED = ('C', 'Door is closed')
    IN_OPENING = 'IO'
    IN_CLOSING = 'IC'

    # IN_PROGRESS_STATUS = Options._G(IN_OPENING, IN_CLOSING)

    _FLAG = False           # underscore leading name is not an option

    x = lambda y: y

    # None uppercase name for classmethod is available.
    @classmethod
    def toggle(cls, status):
        if status is cls.OPEN:
            return cls.CLOSED
        elif status is cls.CLOSED:
            return cls.OPEN
        elif status is cls.IN_OPENING:
            return cls.IN_CLOSING
        else:
            return cls.IN_OPENING

    # None uppercase name for staticmethod is available.
    @staticmethod
    def Foo():
        pass

    # None uppercase name for property is available.
    @property
    def bar(self):
        return ''

    @bar.setter
    def bar(self, val):
        pass

    # None uppercase name for function is available.
    def baz(self):
        pass


class TestCustomizedOptions(unittest.TestCase):

    def test_enum(self):
        self.assertEqual(Fruit.APPLE, 1)
        self.assertEqual(Fruit.APPLE.name, 'APPLE')
        self.assertLess(Fruit.ORANGE, Fruit.BANANA)

        self.assertEqual(EnumCellPhone.SAMSUNG, 2)

        self.assertEqual(EnumCellPhone.HUAWEI.text, 'Huawei cellphone')

        self.assertEqual(Fruit.APPLE, EnumCellPhone.APPLE)
        self.assertIsNot(Fruit.APPLE, EnumCellPhone.APPLE)

    def test_invalid_definition(self):
        try:
            class MyOptions(Options):
                foo = 1
                Bar = 2
                BAZ_1 = 3
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def test_diff_attr_option_name(self):
        try:
            class MyOptions(Options):
                FOO = 1
                BAR = Option(code=2, name='Bar')        # name must be 'BAR'
        except Exception as e:
            self.assertIsInstance(e, ValueError)

    def test_duplicated_options(self):
        try:
            class MyOptions(Options):
                FOO = 1
                FOO = Option(code=2, name='Bar')        # duplicated name
        except Exception as e:
            self.assertIsInstance(e, ValueError)

        try:
            class MyOptions(Options):
                FOO = 1
                BAR = Option(code=1, name='Bar')        # duplicated code
        except Exception as e:
            self.assertIsInstance(e, ValueError)

    def test_get_item(self):
        self.assertEqual('O', DoorState['OPEN'])
        self.assertEqual(DoorState.OPEN, DoorState['OPEN'])
        self.assertEqual(DoorState.OPEN, DoorState[DoorState.OPEN.name])
        self.assertEqual('C', DoorState.get('CLOSED'))
        self.assertEqual('IC', DoorState.get('IN_CLOSING'))
        # self.assertEqual(Option.NOT_DEFINED, DoorState.get('Foo'))
        self.assertEqual(None, DoorState.get('Foo'))
        self.assertEqual(None, DoorState.get('Foo'))
        self.assertRaises(KeyError, DoorState.__getitem__, ('FOO',))
        self.assertRaises(KeyError, DoorState.__getitem__, (DoorState.OPEN,))
        self.assertRaises(TypeError, DoorState.__setitem__, ('FOO', 'bar'))

    def test_collection_codes(self):
        codes = Fruit.codes
        self.assertIsInstance(codes, list)
        self.assertIn(1, codes)
        self.assertIn(2, codes)
        self.assertIn(3, codes)
        self.assertEqual(len(codes), 3)

    def test_collection_names(self):
        names = Fruit.names
        self.assertIsInstance(names, list)
        self.assertIn('APPLE', names)
        self.assertIn('ORANGE', names)
        self.assertIn('BANANA', names)
        self.assertEqual(len(names), 3)

    def test_collection_all(self):
        lst = Fruit.all
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 3)
        self.assertIn(Fruit.APPLE, lst)
        self.assertIn(Fruit.ORANGE, lst)
        self.assertIn(Fruit.BANANA, lst)

    def test_collection_tuples(self):
        lst = Fruit.tuples
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 3)
        val = lst[0]
        self.assertIsInstance(val, tuple)
        self.assertIn(('APPLE', 1, None), lst)
        self.assertIn(('ORANGE', 2, None), lst)
        self.assertIn(('BANANA', 3, None), lst)

    def test_collection_items(self):
        items = Fruit.items
        self.assertIsInstance(items, dict)
        self.assertEqual(len(items), 3)
        self.assertIn('APPLE', items)
        self.assertIn(Fruit.ORANGE, items.values())
        self.assertIn(Fruit.BANANA.name, items.keys())

    def test_get_list(self):
        lst = Fruit.get_list('code')
        self.assertIsInstance(lst, list)
        self.assertIn(Fruit.APPLE, lst)
        self.assertEqual(len(lst), 3)

        lst = Fruit.get_list('name')
        self.assertIsInstance(lst, list)
        self.assertIn(Fruit.APPLE.name, lst)

        lst = Fruit.get_list('name', 'text')
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 3)
        name, text = lst[0]
        self.assertIn(name, Fruit.names)

        lst = Fruit.get_list('code', 'name', 'text')
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 3)
        code, name, text = lst[0]
        self.assertIn(code, Fruit)

    def test_get_dict(self):
        items = Fruit.get_dict('code', 'name')
        self.assertIsInstance(items, dict)
        self.assertIn(Fruit.APPLE.code, items)
        self.assertEqual(len(items), 3)

        items = Fruit.get_dict('name', 'code', 'text')
        self.assertIsInstance(items, dict)
        self.assertIn(Fruit.APPLE.name, items)
        self.assertEqual(len(items), 3)
        apple = items.get(Fruit.APPLE.name)
        self.assertIsInstance(apple, tuple)
        self.assertEqual(len(apple), 2)
        self.assertIn(Fruit.APPLE, apple)

    def test_ignore_invalid_name(self):

        # invalid name
        try:
            class Bar(Options):
                Invalid= (1, 2)
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

        # ignore invalid name
        class Foo(Options):
            __IGNORE_INVALID_NAME__ = True
            Ignored = (1, 2)

        self.assertEqual(Foo.Ignored, (1, 2))

    def test_tags_groups(self):

        class Foo(Options):
            A = 1, None, ['BAR']
            B = 2, 'B is 2', ['FOO']
            C = 'C', 'C is letter', ('FOO', 'BAR')
            D = 'd', 'day'

            BAZ = G(B, D)

        self.assertEqual(Foo.FOO, (Foo.B, Foo.C))
        self.assertEqual(Foo.FOO, (2, 'C'))
        self.assertEqual(Foo.FOO, (Foo.B, 'C'))
        self.assertEqual(Foo.FOO, (2, Foo.C))
        self.assertIn(Foo.C, Foo.FOO)
        self.assertIn(Foo.C, Foo.BAR)
        self.assertEqual(Foo.FOO + Foo.BAR, (2, 'C', 1, 'C'))
        self.assertEqual(Foo.FOO + Foo.BAR, (Foo.B, 'C', 1, Foo.C))

        self.assertEqual(Foo.BAZ, (Foo.B, Foo.D))
        self.assertEqual(Foo.BAR + Foo.BAZ, (1, 'C', 2, 'd'))

        Foo.D.add_tag('BAR')
        self.assertEqual(Foo.BAR, (1, 'C', 'd'))
        Foo.C.remove_tag('BAR')
        self.assertEqual(Foo.BAR, (1, Foo.D))

        Foo.C.remove_tag('FOO')
        self.assertEqual(Foo.FOO, (Foo.B, ))
        self.assertEqual(tuple(Foo.C.tags), ())

        Foo.B.remove_tag('FOO')
        self.assertEqual(Foo.FOO, ())

    def test_grouping_single_option(self):

        class Foo(Options):
            A = 1
            B = 2, 'B is 2'
            C = 'C', 'C is letter', ['FOO']
            D = Option('d', name='D')
            E = Option('e1', 'E', 'Earth')
            F = Option('15', 'F', 'Finish', ['FOO'])

            G1 = G(A)
            G2 = G(B)
            G3 = G(C)
            G4 = G(D)
            G5 = G(E)
            G6 = G(F)

        self.assertEqual(Foo.G1, (Foo.A, ))
        self.assertEqual(Foo.G2, (Foo.B, ))
        self.assertEqual(Foo.G3, (Foo.C, ))
        self.assertEqual(Foo.G4, (Foo.D, ))
        self.assertEqual(Foo.G5, (Foo.E, ))
        self.assertEqual(Foo.G6, (Foo.F, ))


if __name__ == '__main__':
    unittest.main()
