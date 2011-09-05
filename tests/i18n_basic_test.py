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

from pycerberus.test_util import ValidationTest
from pycerberus.validators import IntegerValidator


class MessagesFromBuiltInValidatorsAreTranslatedTest(ValidationTest):
    
    validator_class = IntegerValidator
    
    def test_error_messages_are_translated(self):
        self.assert_equals('Please enter a number.', self.get_error('foo', locale='en').details().msg())
        self.assert_equals('Bitte geben Sie eine Zahl ein.', self.get_error('foo', locale='de').details().msg())
    
    def test_variable_parts_are_added_after_translation(self):
        expected_message = u'(String erwartet, "list" erhalten)'
        translated_message = self.get_error([], locale='de').details().msg()
        self.assert_contains(expected_message, translated_message)
    
    def test_fallback_to_english_translation_for_unknown_locales(self):
        self.assert_equals('Please enter a number.', self.get_error('foo', locale='unknown').details().msg())


