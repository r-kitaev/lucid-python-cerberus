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

import os

from pycerberus.test_util import PythonicTestCase
from pycerberus.i18n import GettextTranslation


class GettextTranslationInfrastructureTest(PythonicTestCase):
    
    def test_domain(self):
        self.assert_equals('messages', GettextTranslation()._domain())
        self.assert_equals('foobar', GettextTranslation(domain='foobar')._domain())
    
    def _localedir(self, **kwargs):
        return GettextTranslation(**kwargs)._args(None)['localedir']
    
    def test_default_localedir_is_in_source_folder(self):
        this_file = os.path.abspath(__file__)
        source_root_dir = os.path.dirname(os.path.dirname(this_file))
        default_locale_dir = self._localedir()
        self.assert_true(default_locale_dir.startswith(source_root_dir), default_locale_dir)
    
    def test_can_specify_localedir(self):
        localedir = '/usr/share/locale'
        self.assert_equals(localedir, self._localedir(localedir=localedir))
    
    def test_can_extract_locale_name_from_context(self):
        translation = GettextTranslation()
        self.assert_equals('en', translation._locale(None))
        self.assert_equals('en', translation._locale({}))
        self.assert_equals('fr', translation._locale({'locale': 'fr'}))


