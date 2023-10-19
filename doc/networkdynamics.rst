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

.. note::

   Simulations don't use :class:`Dynamics` objects directly, but
   instead use a sub-class. See :ref:`implementation-dynamics` for an
   explanation of the differences between approaches.

In stand-alone mode, a simulation is run by calling the :meth:`run`
method (inherited from `epyc.Experiment`), passing a dict of
parameters. The network dynamics then performs a single simulation
according to the following process:

* The :meth:`Dynamics.setUp` method uses
  :meth:`NetworkExperiment.setUp` to delete any old working network
  and build a new one. It then lets the :class:`Process` configure the
  working copy: it calls :meth:`Process.reset` to reset the process,
  sets its working network by calling :meth:`Process.setNetwork`, then
  builds the process instance using :meth:`Process.build` and sets it
  up ready for simulation by calling :meth:`Process.setUp`.
* The :meth:`Dynamics.do` method is called to perform the simulation, returning
  a dict of experimental results. This method is overridden by sub-classes
  to define the style of simulation being performed.
* The :meth:`Dynamics.tearDown` method is called to clean-up the simulation
  class, using :meth:`Process.tearDown` to tear-down the process

This decomposition is very flexible. At its simplest, a dynamics takes
a fixed prototype network as a parameter to its construction and copies it
for every run. More complex use cases supply an instance of
:class:`NetworkGenerator` that samples from a class of random networks defined
by the experimental parameters.

.. note::

   In versions of `epydemic` prior to 1.13.1 the working network was
   discarded as part of tear-down, making it inaccessible once the
   experimental run had ended.

   Starting with version 1.13.1, this behaviour was changed so that
   the working network is retained until the *next* experiment is
   performed, whereupon it is discarded and a new working network is
   created.

   This change simplifies using `epydemic` at a small scale, since one
   can directly see the network that exists after an experimental run
   without having to explicitly save it. It makes no difference beyond
   this.

Note the division of labour. A :class:`Dynamics` object provides the scheduling
for events, which are themselves specified and defined in a :class:`Process`
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


Stochastic event distributions
------------------------------

The stochastic events are defined and managed in the :class:`Process`
class. The dynamics only cares about their distributions.

.. automethod:: Dynamics.perElementEventDistribution

.. automethod:: Dynamics.perElementEventRateDistribution

.. automethod:: Dynamics.fixedRateEventDistribution

.. automethod:: Dynamics.eventRateDistribution


.. _dynamics-posted-events:

Posted events
-------------

A :class:`Dynamics` object also maintains a queue of posted event.

.. automethod:: Dynamics.postEvent

.. automethod:: Dynamics.postRepeatingEvent

This queue is then accessed to extract the events that need to be fired
up to a given simulation time.

.. automethod:: Dynamics.nextPendingEvent

.. automethod:: Dynamics.nextPendingEventTime

.. automethod:: Dynamics.nextPendingEventBefore

.. automethod:: Dynamics.pendingEventTime

.. automethod:: Dynamics.runPendingEvents

Posted events can be un-posted at any time before they
fire. (Repeating events can't be un-posted once posted.)

.. automethod:: Dynamics.unpostEvent
