# -*- coding: utf-8 -*-

# -- Import project information ------------------------------------------------

import os

def get_release_info():
    release_info = {}
    execfile(os.path.join('..', 'pycerberus', 'release.py'), release_info)
    return release_info
release_info = get_release_info()

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# The suffix of source filenames.
source_suffix = '.txt'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = release_info['name']
copyright = release_info['_copyright']

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = release_info['version']
# The full version, including alpha/beta/rc tags.
release = version + ''

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']


# Output file base name for HTML help builder.
htmlhelp_basename = 'pycerberusdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'pycerberus.tex', u'pycerberus Documentation',
   u'Felix Schwarz', 'manual'),
]


# -- Add source directory to PYTHONPATH ----------------------------------------

import os
import sys

# don't need to import 
sys.path.append(os.path.abspath('..'))


# -- Code to show nicer autodoc signatures -------------------------------------

import inspect


class NonStringRepr(object):
    
    def __init__(self, value):
        self._value = value
    
    def __repr__(self):
        return self._value


def _use_classnames_instead_of_class_repr(argspec):
    defaults = []
    if argspec.defaults is not None:
        for default in argspec.defaults:
            if isinstance(default, type):
                defaults.append(NonStringRepr(default.__name__))
                continue
            defaults.append(default)
    tuple_argspec = [i for i in argspec]
    tuple_argspec[3] = defaults
    return tuple_argspec

def process_signature(app, what, name, obj, opts, sig, return_annotation):
    if what == 'class':
        if not inspect.ismethod(obj.__init__):
            # object.__init__ is a slot wrapper, inspect will throw an exception
            # for that so we just build the correct argspec manually
            tuple_argspec = (['self'], None, None, None)
        else:
            argspec = inspect.getargspec(obj.__init__)
            tuple_argspec = _use_classnames_instead_of_class_repr(argspec)
        signature = inspect.formatargspec(*tuple_argspec)
        return (signature, return_annotation)
    return (sig, return_annotation)


def setup(app):
    app.connect('autodoc-process-signature', process_signature) 


