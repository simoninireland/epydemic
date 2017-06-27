:class:`StochasticDynamics`: Stochastic (Gillespie) process dynamics
====================================================================

.. currentmodule:: epydemic

The idea of stochastic event-based simulation arose in *ab initio*
chemistry to simulate interactions between molecules. The basic
technique is due to `Gillespie <Gil76>`_ and was later `refined by him
<Gil77>`_.

The basic idea of Gillespie simulation is to structure an experiment
in terms of events which occur with some probability over continuous
time. Individual event probabilities are converted to rates by
multiplying the individual probability by the number of possible ways
it can occur at this instance, leading to a probability distribution
of events and the time until they occur. We then draw from this
distribution and update it according to the behaviour defined for that
particular event. This allows the rates of events to change over time.

.. autoclass:: StochasticDynamics
   :show-inheritance:
	 

Creating a dynamics
-------------------

.. automethod:: StochasticDynamics.__init__


Running a dynamics
------------------

To run a process' dynamics we need two things: the event rate table
that maps an event type and its rate to the function for that event;
and the overall experimental control that runs the experiment and
packages-up some key common results.

.. automethod:: StochasticDynamics.eventRateDistribution

.. automethod:: StochasticDynamics.do
