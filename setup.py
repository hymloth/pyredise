from distutils.core import setup, Extension
str_check = Extension('pyredise.stringcheck', ['pyredise/fast_regex/stringcheck.c'])

       
setup (name = 'pyredise',
       version = '0.15',
       packages=['pyredise', 'stemmers'],
       description = 'Python Redis Search Engine',
       url = "http://github.com/hymloth/pyredise",
       download_url = "http://www.noowit.com/static/scripts/pyredise_latest.zip",
       author = "Christos Spiliopoulos",
       author_email = "santos.koniordos@gmail.com",
       license = "Apache License, Version 2.0",
       ext_modules = [str_check] )