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

To run a process' dynamics we need to define two things: the action
that runs in each single timestep; and the overall experimental
control that runs the experiment and packages-up some key common
results.

.. automethod:: SynchronousDynamics.dynamics

.. automethod:: SynchronousDynamics.do
