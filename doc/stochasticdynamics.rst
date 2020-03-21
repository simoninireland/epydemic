:class:`StochasticDynamics`: Stochastic (Gillespie) process dynamics
====================================================================

.. currentmodule:: epydemic

.. autoclass:: StochasticDynamics
   :show-inheritance:
	 

Running a dynamics
------------------

The idea of stochastic event-based simulation arose in *ab initio*
chemistry to simulate interactions between molecules. The basic
technique is due to :ref:`Gillespie <Gil76>` and was later
:ref:`refined further <Gil77>` by him.

The basic idea of Gillespie simulation is to structure an experiment
in terms of events which occur with some probability over continuous
time. Individual event probabilities are converted to rates by
multiplying the individual probability by the number of possible ways
it can occur at this instance, leading to a probability distribution
of events and the time until they occur. We then draw from this
distribution and update it according to the behaviour defined for that
particular event. This allows the rates of events to change over time.

The dynamics works as follows:

* The event rate distribution is acquird from the process by calling :meth:`Process.eventRateDistribution`,
  which returns both per-event and fixed-rate events.
* Based on these rates, a random time offset to the next event is drawn from an
  exponential distribution.
* The event that occurs at this time is then drawn from the combined distribution
  of all the available events.
* The simulation time is updated by the time offset.
* Any events posted for before this time are run by calling :meth:`Dynamics.runPendingEvents`.
* An element is drawn randomly from the event locus, and the corresponding event is fired.
* This process continues until the process is at equilibrium, as indicated
  by its :meth:`Process.atEquilibrium` method.

.. automethod:: StochasticDynamics.do
