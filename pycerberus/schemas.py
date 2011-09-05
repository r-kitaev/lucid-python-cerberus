# -*- coding: UTF-8 -*-
#
# The MIT License
# 
# Copyright (c) 2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu>
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

import re

from pycerberus.i18n import _
from pycerberus.schema import SchemaValidator

__all__ = ['PositionalArgumentsParsingSchema']


class PositionalArgumentsParsingSchema(SchemaValidator):
    """This schema parses a string containing arguments within a specified order
    and returns a dict where each of these parameters is mapped to a specific 
    key for easy retrieval.
    
    You specify the order of parameters (and the keys) in the class-level 
    attribute ``parameter_order``::
    
        class ConfigListSchema(PositionalArgumentsParsingSchema):
            first_key = StringValidator()
            second_key = IntegerValidator()
            parameter_order = (first_key, second_key)
    
    By default the items are separated by comma though you can override in the
    method ``separator_pattern()``. If there are more items than keys specified,
    this schema will behave like any other schema (depending if you set the
    class-level attribute ``allow_additional_parameters``).
    """
    
    def __init__(self, *args, **kwargs):
        self.super()
        self.set_internal_state_freeze(False)
        self.set_allow_additional_parameters(False)
        self.set_parameter_order(getattr(self.__class__, 'parameter_order', ()))
        self.set_internal_state_freeze(True)
    
    def messages(self):
        return {'additional_items': _('Too many parameters: %(additional_items)s')}
    
    def separator_pattern(self):
        return '\s*,\s*'
    
    def split_parameters(self, value, context):
        arguments = []
        if len(value) > 0:
            arguments = re.split(self.separator_pattern(), value.strip())
        return arguments
    
    def _parameter_names(self):
        return list(self._parameter_order)
    
    def aggregate_values(self, parameter_names, arguments):
        """This method can manipulate or aggregate parsed arguments. In this 
        class, it's just a noop but sub classes can override this method to do
        more interesting stuff."""
        return parameter_names, arguments
    
    def _map_arguments_to_named_fields(self, value, context):
        parameter_names = self._parameter_names()
        arguments = self.split_parameters(value, context)
        
        parameter_names, arguments = self.aggregate_values(parameter_names, arguments)
        nr_missing_parameters = max(len(parameter_names) - len(arguments), 0)
        nr_additional_parameters = max(len(arguments) - len(parameter_names), 0)
        arguments.extend([None] * nr_missing_parameters)
        parameter_names.extend(['extra%d' % i for i in xrange(nr_additional_parameters)])
        return dict(zip(parameter_names, arguments))
    
    def set_parameter_order(self, parameter_names):
        self._parameter_order = parameter_names
    
    def process(self, value, context=None):
        if value is None:
            value = {}
        fields = self._map_arguments_to_named_fields(value, context or {})
        print 'fields', fields
        return self.super(fields, context=context)


