:class:`SEIR`: The SEIR process
===============================

.. currentmodule:: epydemic

.. autoclass:: SEIR



Dynamical states
----------------

SEIR simulation places nodes into one of four compartments:

.. autoattribute:: SEIR.SUSCEPTIBLE

.. autoattribute:: SEIR.EXPOSED

.. autoattribute:: SEIR.INFECTED
		   
.. autoattribute:: SEIR.REMOVED


Parameters
----------

The process is parameterised by five parameters:

.. autoattribute:: SEIR.P_EXPOSED

.. autoattribute:: SEIR.P_INFECT_ASYMPTOMATIC

.. autoattribute:: SEIR.P_INFECT_SYMPTOMATIC

.. autoattribute:: SEIR.P_SYMPTOMS

.. autoattribute:: SEIR.P_REMOVE

The :attr:`SEIR.P_EXPOSED` parameter defines the proportion of nodes
that are initially placed into the :attr:`SEIR.EXPOSED` compartment, with
all other nodes being placed into the :attr:`SEIR.SUSCEPTIBLE` compartment.


Loci
----

Dynamics in SEIR occurs in four places:

* At SI edges, where the node at one endpoint is susceptible and the
  node at the other is infected;
* At SI edges, where the node at one endpoint is susceptible and the
  node at the other is infected;
* At exposed nodes which show symptoms; and
* At infected nodes, which which are removed.

These four options define the loci for the SEIR model.

.. autoattribute:: SEIR.SE

.. autoattribute:: SEIR.SI

The other loci are named :attr:`SEIR.EXPOSED` and :attr:`SEIR.INFECTED`, the same
as the corresponding compartments.

		   
Building the model
------------------

Building the model creates the three epidemic compartments and
installs the necessary loci and events to define the disease
dynamics. The event methods are described more thoroughly below.

.. automethod:: SEIR.build
		
		   
Event methods
-------------

Event methods are defined for each of the two dynamical rules for the
process: infection and removal.

.. automethod:: SEIR.infectAsymptomatic

.. automethod:: SEIR.infect
		
.. automethod:: SEIR.symptoms
		
.. automethod:: SEIR.remove
		
		
