:class:`Dynamics`: Process dynamics over networks
=================================================

.. currentmodule:: epydemic

.. autoclass:: Dynamics
   :show-inheritance:


In use
------

A :class:`Dynamics` object is an instance of `epyc.Experiment`, and
hence can be run either stand-alone or as part of a larger planned
experimental protocol. Each simulation is parameterised by a dict
providing the parameters used to condition the simulation, typically
providing event probabilities for the various events that may happen.

In stand-alone mode, a simulation is run by calling the :meth:`run`
method (inherited from `epyc.Experiment`), providing a dict of
parameters. The network dynamics then performs a single simulation
according to the following process:

* The :meth:`Dynamics.setUp` method creates a copy of the prototype
  network that was supplied at construction time or by calling
  :meth:`Dynamics.setNetworkPrototype`. It then lets the :class:`Process`
  configure the working copy: it calls :meth:`Process.reset` to reset
  the process, sets its working network by calling :meth:`Process.setNetwork`,
  then builds the process instance using :meth:`Process.build` and sets it
  up rerady for simulation by calling :meth:`Processd.setUp`.
* The :meth:`Dynamics.do` method is called to perform the simulation, returning
  a dict of experimental results. This method is overridden by sub-classes
  to define the style of simulation being performed.
* The :meth:`Dynamics.tearDown` method is called to clean-up the simulation
  class, typically destroying the working network instance

This decomposition is very flexible. At its simplest, a network takes
a prototype network as a parameter to its construction and copies it
for every run.

Note the division of labour. A :class:`Dynamics` object provides the scheduling
for evenets, which are themselves sapecified and defined in a :class:`Process`
object. There is seldom any need to interact directly with a :class:`Dynamics` object
other than through its execution interface.


Attributes
----------

.. autoattribute:: Dynamics.TIME

.. autoattribute:: Dynamics.EVENTS


Configuring the simulation
--------------------------

A :class:`Dynamics` object runs the process it describes over a
network. The network is treated as a prototype that is copied before
the start of each experiment, so that any manipulations or labelling
the experiment caries out are torn down before the next run.

.. automethod:: Dynamics.setNetworkPrototype

.. automethod:: Dynamics.setNetworkPrototype

.. automethod:: Dynamics.network

.. automethod:: Dynamics.process


Running the experiment
----------------------

A simulation takes the form of an `epyc` experiment which has set-up,
execution, and tear-down phases.

.. automethod:: Dynamics.setUp

.. automethod:: Dynamics.tearDown

.. automethod:: Dynamics.experimentalResults



Probabilistic events
--------------------

The way in which stochastic events are run depends on the :class:`Dynamics` sub-class.


Posted events
-------------

.. automethod:: Dynamics.runPendingEvents



