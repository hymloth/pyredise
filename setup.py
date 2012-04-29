from distutils.core import setup, Extension
str_check = Extension('pyredise.stringcheck', ['pyredise/fast_regex/stringcheck.c'])

       
setup (name = 'pyredise',
       version = '0.12',
       packages=['pyredise'],
       description = 'Python Redis Search Engine',
       url = "http://github.com/hymloth/pyredise",
       download_url = "http://github.com/hymloth/pyredise/tarball/master",
       author = "Christos Spiliopoulos",
       author_email = "santos.koniordos@gmail.com",
       license = "Apache License, Version 2.0",
       ext_modules = [str_check] )