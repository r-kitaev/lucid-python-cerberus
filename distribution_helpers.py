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

from distutils.command.build import build
import os

from setuptools.command.install_lib import install_lib


__all__ = ['commands_for_babel_support', 'i18n_aware_commands']

def is_babel_available():
    try:
        import babel
    except ImportError:
        return False
    return True

def commands_for_babel_support():
    if not is_babel_available():
        return {}
    from babel.messages import frontend as babel
    
    extra_commands = {
        'extract_messages': babel.extract_messages,
        'init_catalog':     babel.init_catalog,
        'update_catalog':   babel.update_catalog,
        'compile_catalog':  babel.compile_catalog,
    }
    return extra_commands

def module_for_filename(filename):
    if filename.endswith('.py'):
        filename = filename[:-len('.py')]
    module_name = filename.replace(os.sep, '.')
    package_name = module_name.split('.')[-1]
    top_level_module = __import__(module_name)
    module = getattr(top_level_module, package_name)
    return module

def information_from_module(module):
    data = dict()
    for symbol_name in dir(module):
        value = getattr(module, symbol_name)
        if not isinstance(value, basestring):
            continue
        data[symbol_name] = value
    return data

def information_from_file(filename):
    data = dict()
    if os.path.exists(filename):
        execfile(filename, data)
    else:
        data = information_from_module(module_for_filename(filename))
    is_exportable_symbol = lambda key: not key.startswith('_')
    
    externally_defined_parameters = dict()
    for key, value in data.items():
        if is_exportable_symbol(key):
            externally_defined_parameters[key] = value
    return externally_defined_parameters

def i18n_aware_commands():
    if not is_babel_available():
        # setup(..., cmdclass={}) will use just the built-in commands
        return dict()
    
    class i18n_build(build):
        sub_commands = [('compile_catalog', None)] + build.sub_commands
    
    # before doing an 'install' (which can also be a 'bdist_egg'), compile the catalog
    class i18n_install_lib(install_lib):
        def run(self):
            self.run_command('compile_catalog')
            install_lib.run(self)
    command_dict = dict(build=i18n_build, install_lib=i18n_install_lib)
    command_dict.update(commands_for_babel_support())
    return command_dict


