from __future__ import absolute_import
import unittest

from dictproperty import DictProperty
from keyproperty import KeyProperty


class KeyPropertyTests(unittest.TestCase):
    def setUp(self):
        class MyClass(dict):
            def __init__(self, name, account, city, state):
                self['name'] = name
                self['account'] = account
                self['city'] = city
                self['state'] = state
            name = KeyProperty('name')
            account = KeyProperty('account', fset=True, fdel=True)
            city = KeyProperty('city', fget=False, fset=True, fdel=True)
            state = KeyProperty('state', fget=lambda self: 'fixed')
        self.MyClass = MyClass

    def test_missing_key(self):
        mine = self.MyClass('foo', 123, 'newark', 'NJ')
        del mine['account']
        # Key not in get
        self.assertRaises(KeyError,
            lambda: mine.account
        )
        # Key not in del
        def deleter():
            del mine.account
        self.assertRaises(KeyError, deleter)

    def test_getter(self):
        mine = self.MyClass('foo', 123, 'newark', 'NJ')
        self.assertEqual(mine.name, 'foo')
        self.assertEqual(mine['name'], 'foo')
        self.assertEqual(mine.account, 123)
        self.assertEqual(mine['account'], 123)
        self.assertRaises(AttributeError,
            lambda: mine.city
        )
        self.assertEquals(mine.state, 'fixed')

    def test_setter(self):
        mine = self.MyClass('foo', 123, 'newark', 'NJ')

        self.assertRaises(AttributeError, lambda: setattr(mine, 'name', 'bar'))

        self.assertEqual(mine['account'], 123)
        mine.account = 456
        self.assertEqual(mine['account'], 456)
        self.assertEqual(mine.account, 456)

        mine['state'] = 'VA'
        self.assertEqual(mine['state'], 'VA')
        self.assertEqual(mine.state, 'fixed')
        self.assertRaises(AttributeError,
            lambda: setattr(mine, 'state', 'xx')
        )

    def test_deleter(self):
        mine = self.MyClass('foo', 123, 'newark', 'NJ')
        def delname():
            del mine.name
        self.assertRaises(AttributeError)


class DictPropertyTests(unittest.TestCase):
    def setUp(self):
        class MyClass(dict):
            def __init__(self, name, account):
                self['name'] = name
                self['account'] = account
            name = DictProperty('name')
            account = DictProperty('account')
        self.MyClass = MyClass

    def test_getter(self):
        mine = self.MyClass('foo', 123)
        self.assertEqual(mine, {'name': 'foo', 'account': 123})
        self.assertEqual(mine.name, 'foo')
        self.assertEqual(mine.account, 123)

    def test_setter(self):
        mine = self.MyClass('foo', 123)
        mine['name'] = 'bar'
        mine.account = 456
        self.assertEqual(mine.name, 'bar')
        self.assertEqual(mine.account, 456)

    def test_missing(self):
        class MyClass(dict):
            def __init__(self, name):
                self['name'] = name
            name = DictProperty('mangle')
        mine = MyClass('foo')
        self.assertRaises(KeyError, lambda: mine.name)

if __name__ == "__main__":
    unittest.main()
