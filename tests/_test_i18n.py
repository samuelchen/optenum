# from __future__ import division
import unittest
import six
from optenum import Option
from gettext import gettext
from django.utils.translation import gettext_lazy


class Fruit(object):
    APPLE = Option(1, 'APPLE', 'Apple')
    ORANGE = 2, gettext('Orange is good.')
    BANANA = 3, gettext_lazy('Banana is best.')


class TestOption(unittest.TestCase):

    def raiseAssert(self, e):
        raise AssertionError('Should raise %s' % e)

    def test_option(self):
        opt = Option(1, 'FOO')
        self.assertIs(opt.code, 1)
        self.assertEqual(str(opt), '1')
        self.assertIsInstance(opt, Option)
        self.assertTrue(issubclass(type(opt), Option))
