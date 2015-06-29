from distutils.core import setup, Extension


       
setup (name = 'pyredise',
       version = '0.18',
       packages=['pyredise', 'pyredise.stemmers'],
       description = 'Python Redis Search Engine',
       url = "http://github.com/hymloth/pyredise",
       download_url = "https://github.com/hymloth/pyredise/archive/v1.8.zip",
       author = "Christos Spiliopoulos",
       author_email = "santos.koniordos@gmail.com",
       license = "Apache License, Version 2.0",
        )