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

import gettext
import os
import sys

from pkg_resources import resource_filename

__all__ = ['_', 'GettextTranslation']


class GettextTranslation(object):
    
    def __init__(self, domain='messages', **kwargs):
        self._gettext_domain = domain
        self._gettext_args = kwargs
    
    def _domain(self):
        return self._gettext_domain
    
    def _default_localedir(self):
        locale_dir_in_egg = resource_filename(__name__, "/locales")
        if os.path.exists(locale_dir_in_egg):
            return locale_dir_in_egg
        locale_dir_on_filesystem = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locales')
        if os.path.exists(locale_dir_on_filesystem):
            return locale_dir_on_filesystem
        return os.path.normpath('/usr/share/locale')
    
    def _locale(self, context):
        return (context or {}).get('locale', 'en')
    
    def _args(self, context):
        args = self._gettext_args.copy()
        args.setdefault('localedir', self._default_localedir())
        args['languages'] = [self._locale(context)]
        return args
    
    def translation(self, context):
        return gettext.translation(self._domain(), fallback=True, **self._args(context))
    
    def _context_from_stack(self):
        frame = sys._getframe(2)
        locals_ = frame.f_locals
        if 'context' not in locals_:
            return {}
        return locals_['context'] or {}
    
    def __getattr__(self, name):
        if name not in ('gettext', 'ugettext'):
            raise AttributeError(name)
        translation = self.translation(self._context_from_stack())
        if name == 'ugettext' and not hasattr(translation, 'ugettext'):
            # Python3 has no ugettext - everything is unicode by 
            # default…
            name = 'gettext'
        return getattr(translation, name)


# If we name that method '_' pygettext will choke on that...
def some_name_which_is_not_reserved_by_gettext(message):
    return message
_ = some_name_which_is_not_reserved_by_gettext

