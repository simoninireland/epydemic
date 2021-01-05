.. _standard-generators:

Standard network generators
===========================

.. currentmodule :: epydemic

Below is a list of standard network generators built-in to ``epydemic``. These
are intended to cover the common use cases, and in particular the classes ofnetwork
that are used commonly in experimental network science.

.. note ::

    See :ref:`build-generators` for a tutorial on how to add new generators.


:class:`FixedNetwork`: A single example network
------------------------------------------------

.. autoclass :: FixedNetwork


:class:`ERNetwork`: Random networks with Poisson-distributed node degrees
-------------------------------------------------------------------------

.. autoclass :: ERNetwork

.. autoattribute :: ERNetwork.N

.. autoattribute :: ERNetwork.PHI

.. autoattribute :: ERNetwork.KMEAN


:class:`BANetwork`: Random networks with powerlaw-distributed node degrees
--------------------------------------------------------------------------

.. autoclass :: BANetwork

.. autoattribute :: BANetwork.N

.. autoattribute :: BANetwork.M



:class:`PLCNetwork`: Random networks with powerlaw-distributed node degrees and an exponential cutoff
-----------------------------------------------------------------------------------------------------

.. autoclass :: PLCNetwork

.. note ::

    Using this class of networks for human populations is discussed in :ref:`model-human-population`.

.. autoattribute :: PLCNetwork.N

.. autoattribute :: PLCNetwork.EXPONENT

.. autoattribute :: PLCNetwork.CUTOFF

