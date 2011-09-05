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

from pycerberus.api import Validator
from pycerberus.compat import set
from pycerberus.lib import PythonicTestCase
from pycerberus.schema import SchemaValidator
from pycerberus.validators import StringValidator


class ExtendSchemaTest(PythonicTestCase):
    
    class BasicSchema(SchemaValidator):
        id = Validator()
        formvalidators = (Validator(), )
    
    def schema_class(self):
        return self.__class__.BasicSchema
    
    def schema(self):
        return self.schema_class()()
    
    def known_fields(self, schema):
        return set(schema.fieldvalidators().keys())
    
    # test functions
    
    def test_can_add_additional_validators_to_existing_schema(self):
        schema = self.schema()
        extended_schema = SchemaValidator()
        extended_schema.add('name', StringValidator())
        extended_schema.add_missing_validators(schema)
        
        self.assert_equals(set(['id', 'name']), self.known_fields(extended_schema))
        self.assert_length(1, schema.formvalidators())
    
    def test_existing_keys_are_kept(self):
        schema = self.schema()
        extended_schema = SchemaValidator()
        extended_schema.add('id', StringValidator())
        extended_schema.add_missing_validators(schema)
        
        self.assert_equals(set(['id']), self.known_fields(schema))
        self.assert_isinstance(extended_schema.validator_for('id'), StringValidator)
    
    def test_adding_validators_appends_formvalidators(self):
        schema = self.schema()
        extended_schema = SchemaValidator()
        extended_schema.add('id', StringValidator())
        extended_schema.add_formvalidator(StringValidator())
        extended_schema.add_missing_validators(schema)
        
        self.assert_length(2, extended_schema.formvalidators())
    
    def test_can_add_validators_from_schema_in_a_declarative_way(self):
        class ExtendedSchema(self.schema_class()):
            name = StringValidator()
            formvalidators = (StringValidator(), )
        
        extended_schema = ExtendedSchema()
        self.assert_equals(set(['id', 'name']), self.known_fields(extended_schema))
        self.assert_length(2, extended_schema.formvalidators())
        self.assert_isinstance(extended_schema.formvalidators()[1], StringValidator)
    
    def test_existing_names_from_superclass_are_replaced(self):
        class ExtendedSchema(self.schema_class()):
            id = StringValidator()
        
        extended_schema = ExtendedSchema()
        self.assert_isinstance(extended_schema.validator_for('id'), StringValidator)


