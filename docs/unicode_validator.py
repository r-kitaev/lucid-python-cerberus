# -*- coding: UTF-8 -*-

from pycerberus.api import Validator
from pycerberus.i18n import _


__all__ = ['UnicodeValidator']


class UnicodeValidator(Validator):
    
    def __init__(self, max=None):
        self.super()
        self._max_length = max
    
    def messages(self):
        return {
                'invalid_type': _(u'Validator got unexpected input (expected string, got %(classname)s).'),
                'too_long': _(u'Please enter at maximum %(max_length) characters.')
               }
    # Alternatively you could also declare a class-level variable:
    # messages = {...}
    
    def convert(self, value, context):
        try:
            return unicode(value, 'UTF-8')
        except Exception:
            classname = value.__class__.__name__
            self.error('invalid_type', value, context, classname=classname)
    
    def validate(self, converted_value, context):
        if self._max_length is None:
            return
        if len(converted_value) > self._max_length:
            self.error('too_long', converted_value, context, max_length=self._max_length)


