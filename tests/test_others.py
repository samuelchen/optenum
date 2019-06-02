import unittest
from optenum.mysix import is_identifier


class TestOthers(unittest.TestCase):

    def test_is_identifier(self):
        self.assertFalse(is_identifier('1a'))
        self.assertFalse(is_identifier('a-b'))
        self.assertFalse(is_identifier(' a'))
        self.assertFalse(is_identifier('a b'))
        self.assertFalse(is_identifier('a\tb'))
        self.assertFalse(is_identifier('\tab'))
        self.assertFalse(is_identifier('ab\t'))
        self.assertFalse(is_identifier('ab '))
        self.assertFalse(is_identifier('ab\n'))
        self.assertFalse(is_identifier('\nab'))
        self.assertFalse(is_identifier('a\nb'))
        self.assertFalse(is_identifier('a\\b'))
        self.assertFalse(is_identifier('a/b'))
        self.assertFalse(is_identifier('a"'))
        self.assertFalse(is_identifier('a.b'))
        self.assertFalse(is_identifier(''))


if __name__ == '__main__':
    unittest.main()
