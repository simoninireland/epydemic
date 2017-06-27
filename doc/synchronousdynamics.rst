:class:`SynchronousDynamics`: Synchronous process dynamics
==========================================================

.. currentmodule:: epydemic
   
.. autoclass:: SynchronousDynamics


Creating a dynamics class
-------------------------

.. automethod:: SynchronousDynamics.__init__


Extra metadata
--------------

The synchronous dynamics records extra metadata.

.. autoattribute:: SynchronousDynamics.TIMESTEPS_WITH_EVENTS



Running a dynamics
------------------

To run a process' dynamics we need to define three things: the process
for a single timestep; the model function that will be run for each
node; and the overall experimental control that runs the experiment
and packages-up some key common results.

:class:`SynchronousDynamics` encodes a synchronous dynamics, meaning
that each timestep runs the model by default on each node in the network.

.. automethod:: SynchronousDynamics.dynamics

.. automethod:: SynchronousDynamics.model

.. automethod:: SynchronousDynamics.do
