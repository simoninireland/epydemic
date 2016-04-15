# Setup for the "Complex networks, complex processes" software package
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

setup(name = 'cncp',
      version = '0.1',
      description = 'Complex networks, complex processes',
      url = 'http://github.com/simoninireland/cncp/lib/cncp',
      author = 'Simon Dobson',
      author_email = 'simon.dobson@computer.org',
      license = 'CC-BY-NC-SA',
      packages = [ 'cncp' ],
      install_requires = [ 'networkx',
                           'numpy' ],
      zip_safe = False)
