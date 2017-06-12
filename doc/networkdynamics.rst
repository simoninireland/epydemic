:class:`Dynamics`: Process dynamics over networks
=================================================

.. currentmodule:: epydemic
   
.. autoclass:: Dynamics


Creating a dynamics class
-------------------------

.. automethod:: Dynamics.__init__


Setting the network
-------------------

A `Dynamics` object runs the process it describes over a network. The
network is treated as a prototype that is copied before the start of
each experiment, so that any manipulations or labelling the experiment
caries out are torn down before the next run.

.. automethod:: Dynamics.network

.. automethod:: Dynamics.setNetworkPrototype


Equilibrium
-----------

There are two ways of deciding whether a simulation has reached
equilibrium: by running the simulation for a fixed (long) time, or by
providing an explicit decision procedure.

.. automethod:: Dynamics.setMaximumTime

.. automethod:: Dynamics.at_equilibrium


Running the experiment
----------------------

A simulation takes the form of an `epyc` experiment which has set-up,
execution, and tear-down phases.

.. automethod:: Dynamics.setUp

.. automethod:: Dynamics.tearDown


Extracting basic results
------------------------

Once an experiment is run we will need to summarise the results. How
this is done depends on the dynamics and the simulation method, but
the :class:`Dynamics` class provides some basic operations that can be
used.

.. automethod:: Dynamics.skeletonise

.. automethod:: Dynamics.populations
		


		
