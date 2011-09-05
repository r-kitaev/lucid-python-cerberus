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
from pycerberus.validators.string import StringValidator

__all__ = ['DomainNameValidator']


class DomainNameValidator(StringValidator):
    """A validator to check if an domain name is syntactically correct."""
    
    def messages(self):
        return {
            'invalid_domain_character': _('Invalid character %(invalid_character)s in domain %(domain)s.'),
            'leading_dot':       _('Invalid domain: %(domain)s must not start with a dot.'),
            'trailing_dot':      _('Invalid domain: %(domain)s must not end with a dot.'),
            'double_dot':        _('Invalid domain: %(domain)s must not contain consecutive dots.'),
        }
    
    def validate(self, value, context):
        self.super()
        if value.startswith('.'):
            self.error('leading_dot', value, context, domain=repr(value))
        if value.endswith('.'):
            self.error('trailing_dot', value, context, domain=repr(value))
        if '..' in value:
            self.error('double_dot', value, context, domain=repr(value))
        
        match = re.search('([^a-zA-Z0-9\.\-])', value)
        if match is not None:
            self.error('invalid_domain_character', value, context, invalid_character=repr(match.group(1)), domain=repr(value))



