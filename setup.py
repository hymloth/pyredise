from distutils.core import setup, Extension
str_check = Extension('pyredise.stringcheck', ['pyredise/fast_regex/stringcheck.c'])

       
setup (name = 'pyredise',
       version = '0.1',
       packages=['pyredise'],
       description = 'Python Redis Search Engine',
       ext_modules = [str_check] )