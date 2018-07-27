:class:`SIS`: The SIS process
=============================

.. currentmodule:: epydemic

.. autoclass:: SIS
   
The Synchronous-Infected-Susceptible or SIS process is a variant of
the more common SIR process which cycles between only two states,
keeping nodes part of the dynamics indefinitely.

Nodes in the network represent individuals, with edges representing
contacts between them. Each individual is assigned a dynamical state
which changes according to the rules of the model.

SIS is a :term:`compartmented model of disease` with two :term:`compartments`:

* *Susceptible (S)*, when an individual be infected with the disease; and
* *Infected (I)*, when an individual can infect neighbouring susceptible
  individuals.


Dynamical states
----------------

SIS simulation places nodes into one of three compartments:

.. autoattribute:: SIS.SUSCEPTIBLE
		   
.. autoattribute:: SIS.INFECTED


Parameters
----------

The process is parameterised by three parameters:

.. autoattribute:: SIS.P_INFECTED

.. autoattribute:: SIS.P_INFECT

.. autoattribute:: SIS.P_REMOVE

The :attr:`SIS.P_INFECTED` parameter defines the proportion of nodes
that are initially placed into the :attr:`SIS.INFECTED` compartment, with
all other nodes being placed into the :attr:`SIS.SUSCEPTIBLE` compartment.


Dynamics
--------

Dynamics in SIS occurs in two places:

* At infected nodes, which which recover back to susceptible with a
  probability given by the :attr:`SIS.P_REMOVE` parameter; and
* At SI edges, where the node at one endpoint is susceptible and the
  node at the other is infected.

These two options define the loci for the SIS model.

.. autoattribute:: SIS.SI

The other locus is named :attr:`SIS.INFECTED`, the same as the
compartment.

		   
Building the model
------------------

Building the model creates the two epidemic compartments and
installs the necessary loci and events to define the disease
dynamics. The event methods are described more thoroughly below.

.. automethod:: SIS.build
		
		   
Event methods
-------------

Event methods are defined for each of the two dynamical rules for the
process: infection and removal (recovery).

.. automethod:: SIS.infect
		
.. automethod:: SIS.remove
		
		
