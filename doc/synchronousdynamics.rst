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

* Any events posted for this timestep are fired by calling :meth:`Dynamics.runPendingEvents`.
* The dynamics accesses the underlying process to acquire the event distribution for per-element
  events by calling :meth:`Process.perElementEventDistribution`.
* For each locus having elements, it selects each element in turn and fires an event on
  that element with the probability given for that event.
* The dynamics then access the fixed-rate event distribution of the process
  by calling :meth:`Process.fixedRateEventDistribution`
* For each non-empty locus, it fires at event with the probability given for that event.
* The current simulation time is updated.
* This continues until the process indicates that it has reached equilibrium,
  as determined by :meth:`Process.atEqulibrium`.

.. automethod:: SynchronousDynamics.do
