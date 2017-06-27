:class:`SIR`: The SIR processes
===============================

.. currentmodule:: epydemic
   
The Synchronous-Infected-Recovered or SIR process is one of the oldest
models of disease, first arising in a paper by :ref:`Kermack and
McKendrick <KMcK27>` in 1927.

Nodes in the network represent individuals, with edges representing
contacts between them. Each individual is assigned a dynamical state
which changes according to the rules of the model.

SIR is a :term:`compartmented model of disease` with three :term:`compartments`:

* *Susceptible (S)*, when an individual be infected with the disease;
* *Infected (I)*, when an individual can infect neighbouring susceptible
  individuals; and
* *Removed (R)*, when an individual has recovered from the infection and
  neither infects nor can be infected.

Essentially a removed individual takes no further part in the
dynamics.


Dynamical states
----------------

SIR simulation places nodes into one of three compartments:

.. autoattribute:: SIR.SUSCEPTIBLE
		   
.. autoattribute:: SIR.INFECTED
		   
.. autoattribute:: SIR.REMOVED


Parameters
----------

The process is parameterised by three parameters:

.. autoattribute:: SIR.P_INFECTED

.. autoattribute:: SIR.P_INFECT

.. autoattribute:: SIR.P_REMOVE

The :attr:`SIR.P_INFECTED` parameter defines the proportion of nodes
that are initially placed into the :attr:`SIR.INFECTED` compartment, with
all other nodes being placed into the :attr:`SIR.SUSCEPTIBLE` compartment.


Dynamics
--------

Dynamics in SIR occurs in two places:

* At infected nodes, which which are removed with a probability given
  by the :attr:`SIR.P_REMOVE` parameter; and
* At SI edges, where the node at one endpoint is susceptible and the
  node at the other is infected.

These two options define the loci for the SIR model.

.. autoattribute:: SIR.SI

The other locus is named :attr:`SIR.INFECTED`, the same as the
compartment.

		   
Building the model
------------------

Building the model creates the three epidemic compartments and
installs the necessary loci and events to define the disease
dynamics. The event methods are described more thoroughly below.

.. automethod:: SIR.build
		
		   
Event methods
-------------

Event methods are defined for each of the two dynamical rules for the
process: infection and removal (recovery).

.. automethod:: SIR.infect
		
.. automethod:: SIR.remove
		
		
