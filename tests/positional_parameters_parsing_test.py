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

from pycerberus.schema import SchemaValidator
from pycerberus.schemas import PositionalArgumentsParsingSchema
from pycerberus.test_util import ValidationTest
from pycerberus.validators import IntegerValidator, StringValidator


class TestPositionalArgumentsWithoutData(ValidationTest):
    
    validator_class = PositionalArgumentsParsingSchema
    
    def test_accept_input_without_parameters(self):
        self.assert_equals({}, self.schema().process(''))
        self.assert_equals({}, self.schema().process(None))
    
    def test_bails_out_if_additional_parameters_are_passed(self):
        e = self.assert_error('fnord')
        self.assert_equals(u"Too many parameters: 'fnord'", e.msg())


class TestPositionalArgumentsWithSingleParameter(ValidationTest):
    
    class SingleParameterSchema(PositionalArgumentsParsingSchema):
        foo = StringValidator()
        parameter_order = ('foo', )
    validator_class = SingleParameterSchema    
    
    def test_bails_out_if_no_parameter_is_passed(self):
        self.assert_error('')
        self.assert_error(None)
    
    def test_bails_out_if_too_many_parameters_are_passed(self):
        self.assert_error('foo, bar')
    
    def test_accepts_one_parameter(self):
        self.assert_equals({'foo': 'fnord'}, self.schema().process('fnord'))


class TestPositionalArgumentsWithMultipleParameters(ValidationTest):
    
    class MultipleParametersSchema(PositionalArgumentsParsingSchema):
        foo = StringValidator()
        bar = IntegerValidator()
        parameter_order = ('foo', 'bar')
    validator_class = MultipleParametersSchema    
    
    def test_bails_out_if_only_one_parameter_is_passed(self):
        self.assert_error('fnord')
    
    def test_accepts_two_parameter(self):
        self.assert_equals({'foo': 'fnord', 'bar': 42}, self.schema().process('fnord, 42'))



class TestProgrammaticSchemaConstructionForPositionalArguments(ValidationTest):
    def setUp(self):
        schema = PositionalArgumentsParsingSchema()
        schema.set_internal_state_freeze(False)
        schema.add('id', IntegerValidator())
        schema.set_parameter_order(['id'])
        schema.set_internal_state_freeze(True)
        # the helper methods will use this private attribute
        self._validator = schema
        
    def test_can_instantiate_schema_programmatically(self):
        self.assert_equals({'id': 42}, self.schema().process('42'))
        self.assert_error('foo')
        self.assert_error('foo, bar')
        

