Shuffle processes: Degree-preserving rewirings of networks
==========================================================

.. currentmodule:: epydemic

``epydemic`` includes processes that rewire networks ahead of
experiments. These processes are inspired by the work reported in
:ref:`Melnik 2011 <MHP11>` and can be used for a number of different
purposes, for example creating a "random" version of an empirical
network or for reducing clustering and other structures without
changing the degree distribution.

:class:`ShuffleK`: Degree-preserving rewiring
---------------------------------------------

.. autoclass:: ShuffleK

.. autoattribute:: ShuffleK.REWIRE_FRACTION

.. automethod:: ShuffleK.build
