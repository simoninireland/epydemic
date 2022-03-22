# Setup for epydemic
#
# Copyright (C) 2017--2022 Simon Dobson
#
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from setuptools import setup

with open('README.rst') as f:
    longDescription = f.read()

setup(name='epydemic',
      version='1.9.2',
      description='Epidemic network simulations in Python',
      long_description=longDescription,
      url='http://github.com/simoninireland/epydemic',
      author='Simon Dobson',
      author_email='simoninireland@gmail.com',
      license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   'Topic :: Scientific/Engineering'],
      python_requires='>=3.6',
      packages=['epydemic', 'epydemic.gf'],
      package_data={'epydemic': ['py.typed']},
      zip_safe=False,
      install_requires=[ "networkx >= 2.4", "epyc >= 1.6.1", "pandas", "numpy >= 1.18", "scipy", "mpmath", "python-dotenv", "epydemicarchive_client",  ],
      extra_requires={':python_version < 3.8': ['typing_extensions']},
)
