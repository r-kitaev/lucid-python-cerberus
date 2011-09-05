# -*- coding: UTF-8 -*-
#
# The MIT License
# 
# Copyright (c) 2009-2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pycerberus.api import Validator
from pycerberus.errors import InvalidArgumentsError
from pycerberus.i18n import _

__all__ = ['IntegerValidator']


class IntegerValidator(Validator):
    
    def __init__(self, min=None, max=None, *args, **kwargs):
        self.min = min
        self.max = max
        if (self.min is not None) and (self.max is not None) and (self.min > self.max):
            message = 'min must be smaller or equal to max (%s > %s)' % (repr(self.min), repr(self.max))
            raise InvalidArgumentsError(message)
        self.super(*args, **kwargs)
    
    def messages(self):
        return {
                'invalid_type': _(u'Validator got unexpected input (expected string, got "%(classname)s").'),
                'invalid_number': _(u'Please enter a number.'),
                'too_low': _(u'Number must be %(min)d or greater.'),
                'too_big': _(u'Number must be %(max)d or smaller.'),
               }
    
    def convert(self, value, context):
        if not isinstance(value, (int, basestring)):
            classname = value.__class__.__name__
            self.error('invalid_type', value, context, classname=classname)
        try:
            return int(value)
        except ValueError:
            self.error('invalid_number', value, context)
    
    def validate(self, value, context):
        if (self.min is not None) and (value < self.min):
            self.error('too_low', value, context, min=self.min)
        if (self.max is not None) and (value > self.max):
            self.error('too_big', value, context, max=self.max)


