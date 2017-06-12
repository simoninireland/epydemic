:class:`StochasticDynamics`: Stochastic (Gillespie) process dynamics
====================================================================

.. currentmodule:: epydemic
   
.. autoclass:: StochasticDynamics


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
