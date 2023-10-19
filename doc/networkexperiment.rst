:class:`NetworkExperiment`: An experiment over a network
========================================================

.. currentmodule:: epydemic

.. autoclass:: NetworkExperiment
   :show-inheritance:


In use
------

:class:`NetworkExperiment` simply adds functions to associate a network or a network
generator with a computational experiment.

.. automethod:: NetworkExperiment.network

.. automethod:: NetworkExperiment.setNetworkGenerator

.. automethod:: NetworkExperiment.networkGenerator

During set-up the experiment instantiates a working copy network for
use within the experiment, deleting it afterwards. If the experiment
was provided with a single "prototype" network, whis is copied each
time; if it was provided with an instance of
:class:`NetworkGenerator`, a new instance of the class of networks
defined by the generator is used.

.. automethod:: NetworkExperiment.setUp


Event taps
----------

Whenever the network changes, there is an opportunity for the
experiment to log it or take some other action. We refer to this as
the *event tap*, as it captures the entire stream of events regardless
of how they are defined. See :ref:`event-taps` for a discussion.

To use the event tap interface, you need to override these
methods (they all have empty defaults) and ensure that they're called
from the right places.

.. automethod:: NetworkExperiment.eventFired

There are three other methods that are called within the core of the
experiment to set up and manage the event tap.

.. automethod:: NetworkExperiment.initialiseEventTaps

.. automethod:: NetworkExperiment.simulationStarted

.. automethod:: NetworkExperiment.simulationEnded

This is simply an interface definition: all the default
implementations are empty. To use the event taps you need to override
these methods for every experiment. The methods should be called as
follows:

- :meth:`NetworkExperiment.initialiseEventTaps`: Early in the
  construction process, to allow any data structures to be created.
- :meth:`NetworkExperiment.simulationStarted`: After any set-up and
  immediately before the work of the experiment (simulation) starts,
  so that the overridden method gets to see the experiment right
  before execution.
- :meth:`NetworkExperiment.eventFired`: Immediately after each
  "event", however defined, to that the overridden method gets to see
  the effect that the method had.
- :meth:`NetworkExperiment.simulationEnded`: After the last event
  and before any tear-down, so that the overridden method gets to see
  the final result of the simulation.
