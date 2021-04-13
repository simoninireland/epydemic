:class:`Dynamics`: Process dynamics over networks
=================================================

.. currentmodule:: epydemic

.. autoclass:: Dynamics
   :show-inheritance:


In use
------

A :class:`Dynamics` object is an instance of :class:`NetworkExperiment`
which is turn an `epyc` experiment, and
hence can be run either stand-alone or as part of a larger planned
experimental protocol. Each simulation is parameterised by a dict
providing the parameters used to condition the simulation, typically
providing event probabilities for the various events that may happen.

In stand-alone mode, a simulation is run by calling the :meth:`run`
method (inherited from `epyc.Experiment`), passing a dict of
parameters. The network dynamics then performs a single simulation
according to the following process:

* The :meth:`Dynamics.setUp` method uses :meth:`NetworkExperiment.setUp` to
  create a working network. It then lets the :class:`Process`
  configure the working copy: it calls :meth:`Process.reset` to reset
  the process, sets its working network by calling :meth:`Process.setNetwork`,
  then builds the process instance using :meth:`Process.build` and sets it
  up rerady for simulation by calling :meth:`Processd.setUp`.
* The :meth:`Dynamics.do` method is called to perform the simulation, returning
  a dict of experimental results. This method is overridden by sub-classes
  to define the style of simulation being performed.
* The :meth:`Dynamics.tearDown` method is called to clean-up the simulation
  class, using :meth:`NetworkExperiment.tearDown` to destroy the working network.

This decomposition is very flexible. At its simplest, a dynamics takes
a fixed prototype network as a parameter to its construction and copies it
for every run. More complex use cases supply an instance of
:class:`NetworkGenerator` that samples from a class of random networks defined
by the experimental parameters.

Note the division of labour. A :class:`Dynamics` object provides the scheduling
for events, which are themselves sapecified and defined in a :class:`Process`
object. There is seldom any need to interact directly with a :class:`Dynamics` object
other than through its execution interface.


Attributes
----------

.. autoattribute:: Dynamics.TIME

.. autoattribute:: Dynamics.EVENTS


Configuring the simulation
--------------------------

A :class:`Dynamics` object runs the process it describes over a
network. It also maintains the simulation time as the simulation progresses.

.. automethod:: Dynamics.process

.. automethod:: Dynamics.currentSimulationTime

.. automethod:: Dynamics.setCurrentSimulationTime


Running the experiment
----------------------

A simulation takes the form of an `epyc` experiment which has set-up,
execution, and tear-down phases.

.. automethod:: Dynamics.setUp

.. automethod:: Dynamics.tearDown

.. automethod:: Dynamics.experimentalResults


Loci
----

Loci for stochastic events are craeted by :class:`Process` instances.

.. automethod:: Dynamics.addLocus

.. automethod:: Dynamics.locus

.. automethod:: Dynamics.loci

.. automethod:: Dynamics.lociForProcess


Probabilistic events
--------------------

Stochastic events can be attached to each locus defined for the simulation.

.. automethod : Dynamics.addEventPerElement

.. automethod:: Dynamics.addFixedRateEvent

Thes events form a probability distribution from which events can be drawn
in the course of the simulation.

.. automethod:: Dynamics.perElementEventDistribution

.. automethod:: Dynamics.fixedRateEventDistribution

.. automethod:: Dynamics.eventRateDistribution


Posted events
-------------

A :class:`Dynamics` object also maintains a queue of posted event.

.. automethod:: Dynamics.postEvent

.. automethod:: Dynamics.postRepeatingEvent

This queue is then accessed to extract the events that need to be fired
up to a given simulation time.

.. automethod:: Dynamics.nextPendingEventBefore

.. automethod:: Dynamics.runPendingEvents
