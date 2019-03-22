import unittest
from optenum import Option, Options


class EnumFruits(Options):
    APPLE = 1
    ORANGE = 2
    BANANA = 3


class EnumCellPhone(Options):
    APPLE = 1
    SAMSUNG = Option(2, name='SAMSUNG')
    HUAWEI = (3, 'Huawei cellphone')


class DoorStates(Options):
    OPEN = 'O', 'Door is opened'
    CLOSED = ('C', 'Door is closed')
    IN_OPENING = 'IO'
    IN_CLOSING = 'IC'

    IN_PROGRESS_STATUS = Options._G(IN_OPENING, IN_CLOSING)


class TestCustomizedOptions(unittest.TestCase):

    def test_enum(self):
        self.assertEqual(EnumFruits.APPLE, 1)
        self.assertEqual(EnumFruits.APPLE.name, 'APPLE')
        self.assertLess(EnumFruits.ORANGE, EnumFruits.BANANA)

        self.assertEqual(EnumCellPhone.SAMSUNG, 2)

        self.assertEqual(EnumCellPhone.HUAWEI.text, 'Huawei cellphone')

        self.assertEqual(EnumFruits.APPLE, EnumCellPhone.APPLE)
        self.assertIsNot(EnumFruits.APPLE, EnumCellPhone.APPLE)

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

    def test_lookup_by_code(self):
        opt = EnumFruits.lookup_by_code(3)
        self.assertIsInstance(opt, Option)
        self.assertEqual(EnumFruits.BANANA, opt)
        self.assertEqual(EnumFruits.BANANA, opt.code)
        self.assertEqual(opt.code, EnumFruits.BANANA)

    def test_lookup_by_name(self):
        opt = EnumFruits.lookup_by_name('ORANGE')
        self.assertIsInstance(opt, Option)
        self.assertEqual(EnumFruits.ORANGE, opt)
        self.assertEqual(EnumFruits.ORANGE, opt.code)
        self.assertEqual(opt.code, EnumFruits.ORANGE)

    def test_get_code_list(self):
        codes = EnumFruits.get_code_list()
        self.assertIsInstance(codes, list)
        self.assertIn(1, codes)
        self.assertIn(2, codes)
        self.assertIn(3, codes)
        self.assertEqual(len(codes), 3)

        order_by = EnumFruits.get_order_by_kw_name()       # "name"
        codes = EnumFruits.get_code_list(order_by=order_by)
        self.assertEqual(codes[0], 1)
        self.assertEqual(codes[1], 3)
        self.assertEqual(codes[2], 2)
        self.assertEqual(len(codes), 3)

        order_by = EnumFruits.get_order_by_kw_code()       # "code"
        codes = EnumFruits.get_code_list(order_by=order_by, reverse=True)
        self.assertEqual(codes[0], 3)
        self.assertEqual(codes[1], 2)
        self.assertEqual(codes[2], 1)
        self.assertEqual(len(codes), 3)

    def test_get_name_list(self):
        names = EnumFruits.get_name_list()
        self.assertIsInstance(names, list)
        self.assertIn('APPLE', names)
        self.assertIn('ORANGE', names)
        self.assertIn('BANANA', names)
        self.assertEqual(len(names), 3)

        order_by = EnumFruits.get_order_by_kw_name()       # "name"
        names = EnumFruits.get_name_list(order_by=order_by)
        self.assertEqual(names[0], 'APPLE')
        self.assertEqual(names[1], 'BANANA')
        self.assertEqual(names[2], 'ORANGE')
        self.assertEqual(len(names), 3)

        order_by = EnumFruits.get_order_by_kw_code()       # "code"
        names = EnumFruits.get_name_list(order_by=order_by, reverse=True)
        self.assertEqual(names[0], 'BANANA')
        self.assertEqual(names[1], 'ORANGE')
        self.assertEqual(names[2], 'APPLE')
        self.assertEqual(len(names), 3)

    def test_get_code_name_list(self):
        lst = EnumFruits.get_code_name_list()
        self.assertIsInstance(lst, list)
        self.assertIn((1, 'APPLE'), lst)
        self.assertIn((2, 'ORANGE'), lst)
        self.assertIn((3, 'BANANA'), lst)
        self.assertEqual(len(lst), 3)

        order_by = EnumFruits.get_order_by_kw_name()       # "name"
        lst = EnumFruits.get_code_name_list(order_by=order_by, code_first=False)
        self.assertEqual(lst[0], ('APPLE', 1))
        self.assertEqual(lst[1], ('BANANA', 3))
        self.assertEqual(lst[2], ('ORANGE', 2))
        self.assertEqual(len(lst), 3)

        order_by = EnumFruits.get_order_by_kw_code()       # "code"
        lst = EnumFruits.get_code_name_list(order_by=order_by, reverse=True, code_first=False)
        self.assertEqual(lst[0], ('BANANA', 3))
        self.assertEqual(lst[1], ('ORANGE', 2))
        self.assertEqual(lst[2], ('APPLE', 1))
        self.assertEqual(len(lst), 3)

    def test_get_code_text_list(self):
        lst = DoorStates.get_code_text_list()
        self.assertIsInstance(lst, list)
        self.assertIn(('O', 'Door is opened'), lst)
        self.assertIn(('C', 'Door is closed'), lst)
        self.assertEqual(len(lst), 4)

        order_by = DoorStates.get_order_by_kw_name()       # "name"
        lst = DoorStates.get_code_text_list(order_by=order_by)
        self.assertEqual(lst[0], ('C', 'Door is closed'))
        self.assertEqual(lst[1], ('IC', None))
        self.assertEqual(lst[3], ('O', 'Door is opened'))
        self.assertEqual(len(lst), 4)

        order_by = DoorStates.get_order_by_kw_code()       # "code"
        lst = DoorStates.get_code_text_list(order_by=order_by, reverse=True, code_first=False)
        self.assertEqual(lst[0], ('Door is opened', 'O'))
        self.assertEqual(lst[1], (None, 'IO'))
        self.assertEqual(lst[2], (None, 'IC'))
        self.assertEqual(lst[3], ('Door is closed', 'C'))
        self.assertEqual(len(lst), 4)


if __name__ == '__main__':
    unittest.main()
