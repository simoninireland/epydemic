:class:`Opinion`: An opinion dynamics process
=============================================

.. currentmodule:: epydemic

.. autoclass:: Opinion


Dynamical states
----------------

Opinion dynamics uses three compartments:

.. autoattribute:: Opinion.IGNORANT

.. autoattribute:: Opinion.SPREADER

.. autoattribute:: Opinion.STIFLER


Parameters
----------

The process is parameterised by three parameters:

.. autoattribute:: Opinion.P_AFFECTED

.. autoattribute:: Opinion.P_AFFECT

.. autoattribute:: Opinion.P_STIFLE


Loci
----

Opinion spreading uses two loci:

* Between ignorant and spreader nodes (GP edges), where the opinion is
  spread (the :attr:`Opinion.GP` locus); and
* Between spreaders and spreaders or stiflers (PPT edges) where the
  opinion is quashed (the :attr:`Opinion.PPT` locus).


Building the model
------------------

.. automethod:: Opinion.build


Event methods
-------------

.. automethod:: Opinion.affect

.. automethod:: Opinion.stifle


Running the model
-----------------

.. automethod:: Opinion.atEquilibrium
