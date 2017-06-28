:class:`SIS_FixedRecovery`: SIS with a fixed recovery interval
==============================================================

.. currentmodule:: epydemic

.. autoclass:: SIS_FixedRecovery

Models of this kind have slightly more predictable behaviour (since
they use a fixed rather than randomly-distributed recovery time), and
so can be useful for some kinds of analysis.


Additional parameters and node attributes
-----------------------------------------

Instead of taking a recovery probability (as defined by
:attr:`SIS.P_REMOVE`), :class:`SIS_FixedRecovery` accepts a fixed
time interval over which an infected node will remain infected
before being removed.

.. autoattribute:: SIS_FixedRecovery.T_INFECTED

We also record the infection time of a node explicitly:

.. autoattribute:: SIS_FixedRecovery.INFECTION_TIME

		   
Building the model
------------------

.. automethod:: SIS_FixedRecovery.build
		
		   
Setup and events
----------------

In setting up the model, we need an additional step to make sure that
any nodes initially infected are set to recover at the appropriate
simulation time.

.. automethod:: SIS_FixedRecovery.setUp


Only a single event method is needed, with :meth:`SIS.recover` being
inherited.

.. automethod:: SIS_FixedRecovery.infect
		
		
