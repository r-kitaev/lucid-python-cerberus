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
from pycerberus.errors import ThreadSafetyError
from pycerberus.test_util import ValidationTest


class DetectThreadSafetyViolationInValidatorTest(ValidationTest):
    class NonThreadSafeValidator(Validator):
        def validate(self, value, context):
            self.fnord = 42
    
    validator_class = NonThreadSafeValidator
    
    def test_can_detect_threadsafety_violations(self):
        self.assert_raises(ThreadSafetyError, self.process, 42)
    
    def test_can_disable_threadsafety_detection(self):
        class ValidatorWrittenByExpert(self.validator_class):
            def __init__(self, *args, **kwargs):
                self._is_internal_state_frozen = False
                self.super()
        self.init_validator(ValidatorWrittenByExpert())
        self.assert_equals(42, self.process(42))


