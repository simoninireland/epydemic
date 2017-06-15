SIS processes
=============

.. currentmodule:: epydemic
   
The Synchronous-Infected-Susceptible or SIS process is a variant on
the more standard SIR model in which individuals are re-inserted into
the susceptible population on recovery, essentially providing a model
in which infection does not provide immunity. SIS also allows endemic
diseases to form, existing indefinitely in the network at low levels.

Nodes in the network represent individuals, with edges representing
contacts between them. Each individual is assigned a dynamical state
which changes according to the rules of the model.

SIS is a :term:`compartmented model of disease` with two :term:`compartments`:


* *Susceptible (S)*, when an individual be infected with the disease; and
* *Infected (I)*, when an individual can infect neighbouring susceptible
  individuals.

Individuals recovering from infection become immediately susceptible
to new infection.

An SIS simulation is parameterised by four parameters, provided when
the simulation is run:

* ``pInfect``: the probability that an infected node will infect a
  neighbouring susceptible node
* ``pRecover``: the probability that an infected node will recover and
  become removed
* ``pInfected``: the probability that a node in the network will be
  infected at the start of the simulation

At the end of a simulation the :meth:`do` method returns a results
dict to which it adds the following collected statistics:

* ``max_outbreak_size``: the size of the largest infected component at
  the end of the simulation
* ``max_outbreak_proportion``: the size of the largest infected
  component as a proportion of the network size
* ``mean_outbreak_proportion``: the average size of an infected
  component
  

Dynamical states
----------------

SIS simulation uses the :attr:`Dynamics.DYNAMICAL_STATE` attribute on
nodes to store their current state. The possible states are:

.. autoattribute:: SISSynchronousDynamics.SUSCEPTIBLE
		   
.. autoattribute:: SISSynchronousDynamics.INFECTED

		   
Synchronous dynamics
--------------------

The synchronous dynamics runs the SIS process in discrete time, with
infections radiating from each infected node.

.. autoclass:: SISSynchronousDynamics
   :show-inheritance:

.. automethod:: SISSynchronousDynamics.__init__

.. automethod:: SISSynchronousDynamics.setUp

.. automethod:: SISSynchronousDynamics.at_equilibrium

.. automethod:: SISSynchronousDynamics.dynamics

.. automethod:: SISSynchronousDynamics.model

.. automethod:: SISSynchronousDynamics.do

		
Stochastic dynamics
-------------------

The stochastic dynamics runs the SIS process in in continuous
time. Infections occur at a rate proportional to the number of
neighbouring susceptible and infected nodes (also known as *SI
edges*), while recovery happens at a rate proportional to the number
of infected nodes.

.. autoclass:: SISStochasticDynamics
   :show-inheritance:

.. automethod:: SISStochasticDynamics.__init__

.. automethod:: SISStochasticDynamics.setUp

.. automethod:: SISStochasticDynamics.at_equilibrium

.. automethod:: SISStochasticDynamics.transitions

.. automethod:: SISStochasticDynamics.infect

.. automethod:: SISStochasticDynamics.recover

.. automethod:: SISStochasticDynamics.do


