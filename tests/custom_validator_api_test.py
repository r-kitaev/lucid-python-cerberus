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
from pycerberus.test_util import ValidationTest


class ValidatorWithCustomMessageForKey(Validator):
    
    def validate(self, value, context):
        self.error('inactive', value, context)
    
    def messages(self):
        return {'inactive': 'Untranslated message'}
    
    def message_for_key(self, key, context):
        assert key == 'inactive'
        return 'message from custom lookup'


class CustomValidatorAPITest(ValidationTest):
    
    validator_class = ValidatorWithCustomMessageForKey
    
    def test_validators_can_custom_lookup_mechanism_for_messages(self):
        self.assert_equals('message from custom lookup', self.message_for_key('inactive'))



class CanDeclareMessagesInClassDictValidator(Validator):
    messages = {'classlevel': 'Message from class-level.'}
    
    def validate(self, value, context):
        self.error('classlevel', value, context)


class CanDeclareMessagesInClassDictTest(ValidationTest):
    
    validator_class = CanDeclareMessagesInClassDictValidator
    
    def test_can_declare_messages_in_classdict(self):
        self.assert_equals('Message from class-level.', self.message_for_key('classlevel'))


