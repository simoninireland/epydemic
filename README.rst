epydemic: Epidemic simulations on networks in Python
=====================================================

Overview
--------

``epydemic`` is a Python library that implements simulations of epidemic
(and other) processes over networks. Epidemic processes are very
important in both network science and its applications. The most
common application is to study the was in which diseases progress in
different network conditions, depending on their infectiousness and
other properties.

``epydemic`` provides the basic simulation machinery for performing
epidemic simulations under two different simulation regimes:
synchronous simulation in which time proceeds in discrete time
intervals, and stochastic or Gillespie simulations which are better
for handling a wider range of probabilities (but which are slightly
harder to specify).



Installation
------------

You can install ``epydemic`` directly from PyPi using ``pip``:

::

   pip install epydemic

The master distribution of ``epydemic`` is hosted on GitHub. To obtain a
copy, just clone the repo:

::
   
    git clone git@github.com:simoninireland/epydemic.git
    cd epydemic
    python setup.py install


   
Documentation
-------------

API documentation for `epydemic` is available on `ReadTheDocs <https://pyepydemic.readthedocs.io/en/latest/>`_
(please note the slightly different project name).



Author and license
------------------

Copyright (c) 2017-2018, Simon Dobson <simon.dobson@computer.org>

Licensed under the `GNU General Public License v3 <http://www.gnu.org/licenses/gpl.html>`_.

