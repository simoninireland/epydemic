Generating functions
====================

.. currentmodule:: epydemic.gf

Network scientists often use :term:`generating functions` as a means
of computing with entire probability distributions at once. ``epydemic``
includes a small generating functions library suitable for using this
approach in conjunction with simulations if desired, for example to
check whether a given theoretical prediction is upheld numerically.


Importing the library
---------------------

The generating functions library can be accessed by importing the
``epydemic.gf`` package:

.. code-block:: python

   import epydemic.gf

Alternatively (and better), import only the functions you need:

.. code-block:: python

   from epydemic.gf import gf_from_network, gf_er


Usage
-----

A generating function is a formal power series that associates a
coefficient with a given integer term. ``epydemic``'s generating
functions can be constructed in different ways.

.. autofunction:: gf_series

.. autofunction:: gf_from_coefficients

.. autofunction:: gf_from_network
