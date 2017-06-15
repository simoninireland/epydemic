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

The :class:`StochasticDynamics` class provides the basic statistical
machinery for performing a simulation. Sub-classes must provide (at
least) a :meth:`transitions` method to return the probability
distribution being drawn from, and an event service routine for each
event that can occur which will be called to update the simulation.  

.. autoclass:: StochasticDynamics
   :show-inheritance:
	 

Creating a dynamics class
-------------------------

.. automethod:: StochasticDynamics.__init__


Running a dynamics
------------------

To run a process' dynamics we need to define two things: the
transition table that maps an event type and its rate to the function
for that event; and the overall experimental control that runs the
experiment and packages-up some key common results.

:class:`StochasticDynamics` encodes a stochastic dynamics, meaning
that the simulation selects an event and a time in the future and then
jumps directly to that point to execute the event.

.. automethod:: StochasticDynamics.transitions

.. automethod:: StochasticDynamics.do
