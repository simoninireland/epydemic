:class:`SIR_FixedRecovery`: SIR with a fixed recovery interval
==============================================================

.. currentmodule:: epydemic

.. autoclass:: SIR_FixedRecovery

Models of this kind have slightly more predictable behaviour (since
they use a fixed rather than randomly-distributed recovery time), and
so can be useful for some kinds of analysis. For example,
:ref:`Newman <New02>` uses fixed-time recovery for his seminal analysis
of epidemic spreading processes.


Additional parameters and node attributes
-----------------------------------------

Instead of taking a recovery probability (as defined by
:attr:`SIR.P_REMOVE`), :class:`SIR_FixedRecovery` accepts a fixed
time interval over which an infected node will remain infected
before being removed.

.. autoattribute:: SIR_FixedRecovery.T_INFECTED

We also record the infection time of a node explicitly:

.. autoattribute:: SIR_FixedRecovery.INFECTION_TIME

		   
Building the model
------------------

.. automethod:: SIR_FixedRecovery.build

In setting up the model, we need an additional step to make sure that
any nodes initially infected are set to be removed at the appropriate
simulation time.

.. automethod:: SIR_FixedRecovery.setUp


Events
------

Only a single event method needs overriding, with :meth:`SIR.remove` being
inherited.

.. automethod:: SIR_FixedRecovery.infect
		
		
