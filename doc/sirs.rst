:class:`SIRS`: The SIRS process
===============================

.. currentmodule:: epydemic

.. autoclass:: SIRS


Parameters
----------

As well as the usual :class:`SIR` parameters, SIRS also includes the
probability of becoming susceptible again.  

.. autoattribute:: SIRS.P_RESUSCEPT

		   
Building the model
------------------

.. automethod:: SIRS.build
		
		   
Event methods
-------------

.. automethod:: SIRS.resuscept
			
