from distutils.core import setup, Extension
module1 = Extension('stringcheck', ['stringcheck.c'])


setup (name = 'stringcheck',
       version = '1.0',
       description = 'Fast checking for legal characters in a string',
       ext_modules = [module1])