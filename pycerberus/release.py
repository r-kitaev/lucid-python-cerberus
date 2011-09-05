# -*- coding: UTF-8 -*-
"Release information about pycerberus."

name = 'pycerberus'
version = '0.4.2'
description = 'Highly flexible, no magic input validation library'
long_description = '''
pycerberus is a framework to check user data thoroughly so that you can protect
your application from malicious (or just garbled) input data.

* Remove stupid code which converts input values: After values are validated, you 
  can work with real Python types instead of strings - e.g. 42 instead of '42', 
  convert database IDs to model objects transparently.
* Implement custom validation rules: Writing custom validators is 
  straightforward, everything is well documented and pycerberus only uses very 
  little Python magic.
* Focus on your value-adding application code: Save time by implementing every 
  input validation rule only once, but 100% right instead of implementing a 
  dozen different half-baked solutions.
* Ready for global business: i18n support (based on GNU gettext) is built in, 
  adding custom translations is easy.
* Tune it for your needs: You can implement custom behavior in your validators,
  e.g. fetch translations from a database instead of using gettext or define
  custom translations for built-in validators.
* Use it wherever you like: pycerberus is used in a SMTP server, trac macros as 
  well as web applications - there are no dependencies on a specific context 
  like web development.


Changelog
******************************

0.4.2 (05.05.2011)
====================
- More fixes for source distribution because of missing files in tar.gz

0.4.1 (16.04.2011)
====================
- Fix source distribution (distribution_helpers.py were not included)

0.4 (13.04.2011)
====================
- pycerberus now supports Python 3!
- Fix installation/egg generation without babel
- Added a schema which can parse positional parameters from a string into a 
  dict before processing the data like a normal schema would do

0.3.3 (04.07.2010)
==================
- Fix installation issue: pycerberus is actually not zip-safe

0.3.2 (05.06.2010)
==================
- Fix egg file generation: Include all necessary packages in eggs
- added babel support to setup.py
- updated pot file and completed German translation
- fix exception if translations for preferred locale are not available (fall 
  back to english messages)

0.3.1 (07.04.2010)
==================
- Fixed bug due to duplicated message in DomainNameValidator/EmailAddressValidator
- Validator can now strip inputs (False by default)
- StringValidator now also treats '' as empty value (as well as None)

0.3 (27.03.2010)
==================
- Python 2.3 compatibility
- Schema can raise error if unknown items are processed
- Basic domain name validator
- Basic email address validator

0.2 (16.03.2010)
==================
- You now can declare custom messages as a class-level dict
- Added interface to retrieve error details from InvalidDataErrors
- Added validation schemas to validate a set of values (typically a web form).
  Schemas can also inherit from other schemas to avoid code duplication.
- Validators try to make thread-safety violations obvious
- Nicer API to retrieve error details from an InvalidDataError

0.1 (30.01.2010)
==================
 - initial release
'''
author = 'Felix Schwarz'
author_email = 'felix.schwarz@oss.schwarz.eu'
url = 'http://www.schwarz.eu/opensource/projects/pycerberus'
download_url = 'http://www.schwarz.eu/opensource/projects/%(name)s/download/%(version)s/%(name)s-%(version)s.tar.gz' % dict(name=name, version=version)
# prefix it with '_' so the symbol is not passed to setuptools.setup()
_copyright = u'2009-2011 Felix Schwarz'
license='MIT'

