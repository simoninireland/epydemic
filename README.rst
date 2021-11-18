epydemic: Epidemic simulations on networks in Python
=====================================================

.. image:: https://badge.fury.io/py/epydemic.svg
    :target: https://badge.fury.io/py/epydemic

.. image:: https://readthedocs.org/projects/pyepydemic/badge/?version=latest
    :target: https://pyepydemic.readthedocs.io/en/latest/index.html

.. image:: https://github.com/simoninireland/epydemic/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/simoninireland/epydemic/actions/workflows/ci.yaml

.. image:: https://www.gnu.org/graphics/gplv3-88x31.png
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html

Overview
--------

``epydemic`` is a Python library that implements simulations of
epidemic (and other) processes on networks. Epidemic processes are
very important in both network science and its applications. The most
common application is to study the ways in which diseases progress in
different network conditions, depending on their infectiousness and
other properties.

``epydemic`` provides simulation under synchronous and stochastic
(Gillespie) dynamics, using the well-known ``networkx`` package to
represent and manipulate networks. It supports a generic model for
compartmented models of disease with several standard models provided
and which can be extended to other, more complex, diseases. It also
supports other network processes such as addition-deletion networks,
and a library for handling generating functions used in network
analysis.

``epydemic`` is built on top of the ``epyc`` experiment management
library, allowing simulations to be conducted at scale on individual
machines, multicore machines, and parallel computing clusters.


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
    pip install .



Documentation
-------------

API documentation for `epydemic` is available on `ReadTheDocs <https://pyepydemic.readthedocs.io/en/latest/>`_
(please note the slightly different project name).



Author and license
------------------

Copyright (c) 2017-2021, Simon Dobson <simoninireland@gmail.com>

Licensed under the `GNU General Public Licence v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.
