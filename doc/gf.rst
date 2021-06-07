.. _gf:

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

Generating functions aren't imported along with the rest of
``epydemic``. Instead, import the ``epydemic.gf`` package:

.. code-block:: python

   import epydemic.gf

Alternatively (and better), import only the functions you need:

.. code-block:: python

   from epydemic.gf import gf_from_network, gf_er


Construction
------------

``epydemic``'s generating functions can be constructed in different
ways: from an explicit series, from a sequence of coefficients, or
from a network.

.. autofunction:: gf_series

.. autofunction:: gf_from_coefficients

.. autofunction:: gf_from_network

There are also :ref:`standard constructors for common generating
functions <standard-gfs>` corresponding to common degree distributions.


In use
------

Generating functions expose three main functions. Firstly, a
generating function can be evaluated by applying it to a value:

.. code-block:: python

   isolated_fraction = gf(0)

Secondly, a generating function can be queried to extract the
coefficient attached to a particular term:

.. code-block:: python

   nodes_of_degree_5 = gf[5]

Thirdly, a generating function can be differentiated one or more
times:

.. code-block:: python

   G0 = gf_er(50000, 20)

   # extract the mean degree
   G0prime = G0.dx()
   mean_degree = G0prime(1)

   # extract the degree-5 nodes (the hard way)
   nodes_of_degree_5 = (G0.dx(5))(0) / math.factorial(5)
