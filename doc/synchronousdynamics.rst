:class:`SynchronousDynamics`: Synchronous process dynamics
==========================================================

.. currentmodule:: epydemic

.. autoclass:: SynchronousDynamics
   :show-inheritance:


Extra metadata
--------------

.. autoattribute:: SynchronousDynamics.TIMESTEPS_WITH_EVENTS


Running a dynamics
------------------

Synchronous dynamics works as follows:

* Any events posted for (or before) the current simulation time are
  fired by calling :meth:`Dynamics.runPendingEvents`.
* The stochastic and fixed-rate events are extracted using
  :meth:`SynchronousDynamics.allEventsInTimestep`
* The events are fired in the order returned. All events are
  "fire-able" at the start of the timestep; they
  may not actually be fired if a previous (in the same timestep) has
  removed the event's element from the locus.
* The number of events fired is updated.
* The current simulation time is updated.
* This continues until the process indicates that it has reached
  equilibrium, as determined by :meth:`Process.atEqulibrium`.

The exact events determined to be fire-able are computed by
:meth:`allEventsInTimestep`, which by default does the following:

* Accesses the underlying process to acquire the event
  distribution for per-element events by calling
  :meth:`Process.perElementEventDistribution`.
* For each locus having elements, it selects each element in turn and
  decides whether to fire an event at this element based on the
  probability given for that event.
* Accesses the fixed-rate event distribution of the
  process by calling :meth:`Process.fixedRateEventDistribution`
* For each non-empty locus, it chooses at event with the probability
  given for that event, chooses a random element on which to fire it.

Firing an event first calls its :term:`event function` and then
reports its firing to the :term:`event tap`.

.. automethod:: SynchronousDynamics.do

.. automethod:: SynchronousDynamics.allEventsInTimestep

Refer to :ref:`implementation-event-orderings` for more details on
how this method can affect simulations.
