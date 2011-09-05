I'm not using Python 3 for any project in production right now. However I'd like to support the Python 3 transition. Therefore I ensure that all tests also pass on Python 3 and I believe you can use pycerberus on Python 3 just fine. I'm testing Python 3 using the latest version of Fedora. As the Python 3 userbase is so small currently, I won't make any effort to maintain compatibility for older versions of Python 3 (e.g. Python 3.0).

Python 3 support for pycerberus is done by the help of the wonderful '2to3' tool which can do all required syntax changes for Python 3. By doing that, I can maintain a single source tree and all fixes for Python 2 are automatically in the Python 3 version.

However there are some shortcomings that you should be aware of:

1. Full i18n support requires Babel and there is no version of Babel with Python 3 support yet. Therefore I don't use Babel on Python 3. However you can get localized error messages if you use Babel with Python 2 to compile the catalog files. After the initial generation of the mo files (done at install time), Babel is not required anymore. For the most recent status of Babel with Python 3, please read http://babel.edgewall.org/ticket/209 . I plan on adding Python 3 support for Babel 1.0.
2. nosetests introduced Python 3 in version 1.0, earlier versions don't work. As nosetests is only necessary to run the unit tests, most people can ignore this limitation.
3. 2to3 support in pycerberus behaves differently than the distribute default: Whenever you call setup.py with Python 3 (e.g. for build/develop), 2to3 will be run on all Python source files. These will be modified in place so after you used Python 3 on a pycerberus working directory, you can not use it with Python 2 anymore. This is mostly because bitten (http://bitten.edgewall.org) does not support conditional build recipies yet. So this limitation is in place to have a build client testing also the Python 3 version of pycerberus.


IMPORTANT:
If you're using pycerberus on Python 3, please tell me how it works for you! :-)

