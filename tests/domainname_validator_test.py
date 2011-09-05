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

from pycerberus.test_util import ValidationTest
from pycerberus.validators import DomainNameValidator


class DomainNameValidatorTest(ValidationTest):
    
    validator_class = DomainNameValidator
    
    def test_accepts_simple_domain_names(self):
        self.assert_equals('example.com', self.process('example.com'))
        self.assert_equals('bar-baz.example', self.process('bar-baz.example'))
    
    def test_reject_domain_with_leading_dot(self):
        msg = self.assert_error('.example.com').msg()
        self.assert_equals("Invalid domain: '.example.com' must not start with a dot.", msg)
    
    def test_reject_domain_with_trailing_dot(self):
        # Actually this test might be a bit fishy as this is actually a valid 
        # domain name. I guess the notion of 'domain name' varies, depending
        # on the context
        msg = self.assert_error('example.com.').msg()
        self.assert_equals("Invalid domain: 'example.com.' must not end with a dot.", msg)
    
    def test_reject_domain_with_double_dots(self):
        msg = self.assert_error('example..com').msg()
        self.assert_equals("Invalid domain: 'example..com' must not contain consecutive dots.", msg)
    
    def test_reject_domain_with_invalid_characters(self):
        msg = self.assert_error('foo_bar.example').msg()
        self.assert_equals("Invalid character '_' in domain 'foo_bar.example'.", msg)


