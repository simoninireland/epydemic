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

``epydemic``'s generating functions can be constructed in four
different ways: from an explicit series, from a sequence of
coefficients, from a function that returns the coefficient of a given
term, or from a network.

.. autofunction:: gf_from_series

.. autofunction:: gf_from_coefficients

.. autofunction:: gf_from_coefficient_function

.. autofunction:: gf_from_network

There are also :ref:`standard constructors for common generating
functions <standard-gfs>` corresponding to common degree distributions.

.. warning::

   When implementing a generating function using a series with
   :func:`gf_from_series` it's important that the series can be
   manipulated and computed in certain specific ways. See
   :ref:`gf-maths-constraints` for details. (The other construction methods
   have no similar traps for the unwary.)


In use
------

Generating functions expose several main functions. Firstly, a
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

Finally, generating functions have (some) algebra implemented for them
directly. They can be multiplied and divided by a constant, which is
use when (for example) computing an :term:`epidemic threshold`:

.. code-block:: python

   N = int(1e4)
   kmean = 10
   pRemove = 0.002
   G0 = gf_er(N, kmean=kmean)

   # compute G1 from the first derivative of G0
   G1 = G0.dx() / N

   # compute the critical threshold
   p_c = float(pRemove / G1.dx()(1))

They can also be added together, subtracted one from the other, and
multiplied together. These operations all return new generating
functions, and so can be combined with differentiation. To check that
differentiation is linear, for example, we might do:

.. code-block:: python

   # create two generating functions from coefficients
   gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
   gf2 = gf_from_coefficients([0, 2])

   # differentiate twice, two different ways
   d1 = (gf1 * gf2).dx(2)
   d2 = (gf1 * gf2).dx().dx()

   # make sure the results are the same
   for i in range(6):
      self.assertEqual(d1[i], d2[i])
