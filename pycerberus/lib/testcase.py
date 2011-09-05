# -*- encoding: utf-8 -*-
"""The idea is to improve Python's unittest.TestCase class with a more pythonic
API and some convenience functionality."""

# Authors: 
#  - Felix Schwarz <felix.schwarz@agile42.com>
#  - Martin Häcker <martin.haecker@agile42.com>

from unittest import TestCase

from pycerberus.lib.simple_super import SuperProxy


__all__ = ['PythonicTestCase']


class PythonicTestCase(TestCase):
    
    super = SuperProxy()
    
    def assert_raises(self, exception_type, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
        except exception_type, e:
            return e
        # We want the same error message as assertRaises but we must not 
        # assume that callable is idempotent
        self.assertRaises(exception_type, lambda: None)
    
    def assert_false(self, actual, msg=None):
        self.assertEquals(False, actual, msg=msg)
    
    def assert_true(self, actual, msg=None):
        self.assertEquals(True, actual, msg=msg)
    
    def assert_trueish(self, actual, msg=None):
        if actual:
            return
        self.failureException(msg)
    
    def assert_none(self, actual, msg=None):
        self.assertEquals(None, actual, msg=msg)
    
    def assert_not_none(self, actual, msg=None):
        self.assertNotEquals(None, actual, msg=msg)
    
    def assert_equals(self, expected, actual, msg=None):
        self.assertEquals(expected, actual, msg=msg)
    
    def assert_not_equals(self, expected, actual, msg=None):
        self.assertNotEquals(expected, actual, msg=msg)
    
    def assert_almost_equals(self, expected, actual, places=None, msg=None):
        self.assertAlmostEqual(expected, actual, places=places, msg=msg)
    
    def assert_isinstance(self, value, klass, msg=None):
        if isinstance(value, klass):
            return
        if msg is None:
            class_name = lambda klass: klass.__name__
            msg = '%s is not an instance of %s' % (class_name(value.__class__), class_name(klass))
        raise AssertionError(msg)
    
    def assert_not_contains(self, expected_value, actual_iterable):
        if expected_value not in actual_iterable:
            return
        raise AssertionError('%s in %s' % (repr(expected_value), repr(list(actual_iterable))))
    
    def assert_contains(self, expected_value, actual_iterable):
        if expected_value in actual_iterable:
            return
        raise AssertionError('%s not in %s' % (repr(expected_value), repr(list(actual_iterable))))
    
    def assert_dict_contains(self, subdict, a_dict):
        for key, value in subdict.items():
            self.assert_contains(key, a_dict)
            self.assert_equals(value, a_dict[key])
    
    def assert_length(self, expected_length, iterable):
        self.assert_equals(expected_length, len(iterable))
    
    def assert_callable(self, a_callable):
        self.assert_true(callable(a_callable), '%s is not callable' % repr(a_callable))


