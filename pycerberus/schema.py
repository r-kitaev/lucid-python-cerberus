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

from pycerberus.api import BaseValidator, EarlyBindForMethods, Validator
from pycerberus.compat import set
from pycerberus.i18n import _
from pycerberus.errors import InvalidDataError

__all__ = ['SchemaValidator']


class SchemaMeta(EarlyBindForMethods):
    def __new__(cls, classname, direct_superclasses, class_attributes_dict):
        fields = cls.extract_fieldvalidators(class_attributes_dict, direct_superclasses)
        formvalidators = cls.extract_formvalidators(class_attributes_dict, direct_superclasses)
        cls.restore_overwritten_methods(direct_superclasses, class_attributes_dict)
        schema_class = EarlyBindForMethods.__new__(cls, classname, direct_superclasses, class_attributes_dict)
        schema_class._fields = fields
        schema_class._formvalidators = formvalidators
        return schema_class
    
    def is_validator(cls, value):
        if isinstance(value, BaseValidator):
            return True
        elif isinstance(value, type) and issubclass(value, BaseValidator):
            return True
        return False
    is_validator = classmethod(is_validator)
    
    def _filter_validators(cls, items):
        validators = []
        for item in items:
            validator = item
            if isinstance(item, (tuple, list)):
                validator = item[1]
            if not cls.is_validator(validator):
                continue
            validators.append(item)
        return validators
    _filter_validators = classmethod(_filter_validators)
    
    def extract_fieldvalidators(cls, class_attributes_dict, superclasses):
        fields = {}
        for superclass in superclasses:
            if not hasattr(superclass, '_fields'):
                continue
            validators = cls._filter_validators(superclass._fields.items())
            # In Python 2.3 you can only pass dicts to {}.update()
            fields.update(dict(validators))
        
        new_validators = cls._filter_validators(class_attributes_dict.items())
        for key, validator in new_validators:
            fields[key] = validator
            del class_attributes_dict[key]
        return fields
    extract_fieldvalidators = classmethod(extract_fieldvalidators)
    
    def extract_formvalidators(cls, class_attributes_dict, superclasses):
        formvalidators = []
        for superclass in superclasses:
            if not hasattr(superclass, '_formvalidators'):
                continue
            formvalidators.extend(cls._filter_validators(superclass._formvalidators))
        
        if 'formvalidators' in class_attributes_dict:
            validators = class_attributes_dict['formvalidators']
            if not callable(validators):
                formvalidators.extend(cls._filter_validators(validators))
        return tuple(formvalidators)
    extract_formvalidators = classmethod(extract_formvalidators)
    
    def restore_overwritten_methods(cls, direct_superclasses, class_attributes_dict):
        super_class = direct_superclasses[0]
        for name in dir(super_class):
            if name not in class_attributes_dict:
                continue
            old_value = getattr(super_class, name)
            new_value = class_attributes_dict[name]
            if name != 'formvalidators' and not cls.is_validator(new_value):
                continue
            class_attributes_dict[name] = old_value
    restore_overwritten_methods = classmethod(restore_overwritten_methods)


class SchemaValidator(Validator):
    
    __metaclass__ = SchemaMeta
    
    def __init__(self, *args, **kwargs):
        self._fields = {}
        self._formvalidators = []
        self.allow_additional_parameters = True
        self.super()
        self._setup_fieldvalidators()
        self._setup_formvalidators()
    
    def _init_validator(self, validator):
        if isinstance(validator, type):
            validator = validator()
        return validator
    
    def _setup_fieldvalidators(self):
        for name, validator in self.__class__._fields.items():
            self.add(name, validator)
    
    def _setup_formvalidators(self):
        for formvalidator in self.__class__._formvalidators:
            self.add_formvalidator(formvalidator)
    
    # -------------------------------------------------------------------------
    # additional public API 
    
    def add(self, fieldname, validator):
        self._fields[fieldname] = self._init_validator(validator)
    
    def validator_for(self, field_name):
        return self._fields[field_name]
    
    def add_formvalidator(self, formvalidator):
        self._formvalidators.append(self._init_validator(formvalidator))
    
    def fieldvalidators(self):
        return self._fields.copy()
    
    def formvalidators(self):
        return tuple(self._formvalidators)
    
    def add_missing_validators(self, schema):
        for name, validator in schema.fieldvalidators().items():
            if name in self.fieldvalidators():
                continue
            self.add(name, validator)
        for formvalidator in schema.formvalidators():
            self.add_formvalidator(formvalidator)
    
    # -------------------------------------------------------------------------
    # overridden public methods
    
    def messages(self):
        return {
                'invalid_type': _(u'Validator got unexpected input (expected "dict", got "%(classname)s").'),
                'additional_items': _(u'Additional fields detected: %(additional_items)s.'),
               }
    
    def convert(self, fields, context):
        if fields is None:
            return self.empty_value(context)
        if not isinstance(fields, dict):
            self.error('invalid_type', fields, context, classname=fields.__class__)
        return self._process_fields(fields, context)
    
    def is_empty(self, value, context):
        # Schemas have a different notion of being "empty"
        return False
    
    def empty_value(self, context):
        return {}
    
    # -------------------------------------------------------------------------
    # private
    
    def _value_for_field(self, field_name, validator, fields, context):
        if field_name in fields:
            return fields[field_name]
        return validator.empty_value(context)
    
    def _process_field(self, key, validator, fields, context, validated_fields, exceptions):
        try:
            original_value = self._value_for_field(key, validator, fields, context)
            converted_value = validator.process(original_value, context)
            validated_fields[key] = converted_value
        except InvalidDataError, e:
            exceptions[key] = e
    
    def _process_field_validators(self, fields, context):
        validated_fields = {}
        exceptions = {}
        for key, validator in self.fieldvalidators().items():
            self._process_field(key, validator, fields, context, validated_fields, exceptions)
        if len(exceptions) > 0:
            self._raise_exception(exceptions, context)
        if (not self.allow_additional_parameters) and (not set(fields).issubset(set(self.fieldvalidators()))):
            additional_items = set(fields).difference(set(self.fieldvalidators()))
            additional_arguments = ' '.join(["'%s'" % fields[key] for key in additional_items])
            self.error('additional_items', None, context, additional_items=additional_arguments)
        return validated_fields
    
    def _process_form_validators(self, validated_fields, context):
        for formvalidator in self.formvalidators():
            validated_fields = formvalidator.process(validated_fields, context=context)
        return validated_fields
    
    def _process_fields(self, fields, context):
        validated_fields = self._process_field_validators(fields, context)
        return self._process_form_validators(validated_fields, context)
    
    def _raise_exception(self, exceptions, context):
        first_field_with_error = exceptions.keys()[0]
        first_error = exceptions[first_field_with_error].details()
        raise InvalidDataError(first_error.msg(), first_error.value(), first_error.key(), 
                               context, error_dict=exceptions)
    
    def set_allow_additional_parameters(self, value):
        self.allow_additional_parameters = value
    
    # -------------------------------------------------------------------------


