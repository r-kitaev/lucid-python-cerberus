#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The MIT License
# 
# Copyright (c) 2009-2011 Felix Schwarz <felix.schwarz@oss.schwarz.eu>
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

import gzip
import os
from StringIO import StringIO
import subprocess
import tarfile
import tempfile


def build_documentation(project_dir):
    doc_dir = os.path.join(project_dir, 'docs')
    temp_file = tempfile.TemporaryFile()
    # We don't need any output on stdout
    subprocess.call(['make', 'html'], cwd=doc_dir, stdout=temp_file)

def make_relative_filename(topdir, filename):
    assert filename.startswith(topdir)
    relative_filename = filename[len(topdir):]
    if relative_filename.startswith(os.sep):
        relative_filename = relative_filename[len(os.sep):]
    return relative_filename

def make_tarname(topdir, filename, path_prefix):
    relative_name = make_relative_filename(topdir, filename)
    tarname = '%s/%s' % (path_prefix, relative_name)
    return tarname

def add_file(tar, filename, arcname, project_dir, path_prefix):
    tarname = make_tarname(project_dir, filename, path_prefix)
    if arcname is not None:
        tarname = make_tarname(project_dir, arcname, path_prefix)
    tar.add(filename, arcname=tarname)

def build_fname_with_changed_path_prefix(project_dir, root, arcname, basename):
    nr_of_dirs = lambda path: len(path.split('/'))
    relative_root = make_relative_filename(project_dir, root)
    assert nr_of_dirs(arcname) <= nr_of_dirs(relative_root), 'Untested'
    
    offset_path_items = relative_root.split('/')[nr_of_dirs(arcname):]
    offset_path = os.path.join(arcname, *offset_path_items)
    tar_fname = os.path.join(project_dir, offset_path, basename)
    return tar_fname

def add_files_below_directory(tar, dirname, arcname, project_dir, path_prefix):
    for (root, dirs, files) in os.walk(dirname):
        for basename in files:
            if basename.endswith('.pyc'):
                continue
            fname = os.path.join(root, basename)
            tar_fname = fname
            if arcname is not None:
                tar_fname = build_fname_with_changed_path_prefix(project_dir, root, arcname, basename)
            tarname = make_tarname(project_dir, tar_fname, path_prefix)
            tar.add(fname, tarname)

def create_tarball(project_dir, package_files, path_prefix):
    tar_fp = StringIO()
    tar = tarfile.open(fileobj=tar_fp, mode='w')
    
    for filename in package_files:
        arcname = None
        if not isinstance(filename, basestring):
            filename, arcname = filename
        filename = os.path.join(project_dir, filename)
        if os.path.isfile(filename):
            add_file(tar, filename, arcname, project_dir, path_prefix)
        else:
            add_files_below_directory(tar, filename, arcname, project_dir, path_prefix)
    tar.close()
    tar_fp.seek(0,0)
    return tar_fp

def get_name_and_version():
    release_info = {}
    execfile(os.path.join('pycerberus', 'release.py'), release_info)
    return (release_info['name'], release_info['version'])

def main():
    name, version = get_name_and_version()
    this_dir = os.path.abspath(os.path.dirname(__file__))
    build_documentation(this_dir)
    
    package_files = ('docs', 'examples', 'pycerberus', 'tests', 'Changelog.txt', 
                     'COPYING.txt', 'README.python3.txt', 'setup.py', 
                     'setup.cfg', 'distribution_helpers.py',
                     ('build/html', 'docs/html'))
    tar_fp = create_tarball(this_dir, package_files, '%s-%s' % (name, version))
    
    gz_filename = '%s-%s.tar.gz' % (name, version)
    gzip.open(gz_filename, 'wb').write(tar_fp.read())

if __name__ == '__main__':
    main()


