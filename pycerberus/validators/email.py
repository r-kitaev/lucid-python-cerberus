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
from pycerberus.validators.domain import DomainNameValidator

__all__ = ['EmailAddressValidator']


class EmailAddressValidator(DomainNameValidator):
    """A validator to check if an email address is syntactically correct.
    
    Please note that there is no clear definition of an 'email address'. Some
    parts are defined in consecutive RFCs, there is a notion of 'string that is 
    accepted by a MTA' and last but not least a fuzzy 'general expectation' what
    an email address should be about.
    
    Therefore this validator is currently extremly simple and does not handle
    internationalized local parts/domains.
    
    For the future I envision some extensions here:
     - support internationalized domain names (possibly also encode to/
       decode from idna) if specified by flag
     - More flexible structure if there must be a second-level domain
    
    Something that should not happen in this validator:
     - Open SMTP connections to check if an account exists
     - specify default domains if missing
    
    These things can be implemented in derived validators
    """
    
    def messages(self):
        return {
            'single_at':         _(u"An email address must contain a single '@'."),
            'invalid_email_character': _(u'Invalid character %(invalid_character)s in email address %(emailaddress)s.'),
        }
    
    def validate(self, emailaddress, context):
        parts = emailaddress.split('@')
        if len(parts) != 2:
            self.error('single_at', emailaddress, context)
        localpart, domain = parts
        self.super(domain, context)
        self._validate_localpart(localpart, emailaddress, context)
    
    # --------------------------------------------------------------------------
    # private helpers
    
    def _validate_localpart(self, localpart, emailaddress, context):
        match = re.search('([^a-zA-Z0-9\.\_])', localpart)
        if match is not None:
            values = dict(invalid_character=repr(match.group(1)), emailaddress=repr(emailaddress))
            self.error('invalid_email_character', localpart, context, **values)

