:class:`CompartmentedModel`: Compartmented models of disease
============================================================

.. currentmodule:: epydemic


.. autoclass:: CompartmentedModel
   :show-inheritance:


Attributes
----------

.. autoattribute:: Dynamics.DYNAMICAL_STATE
		   
.. autoattribute:: Dynamics.OCCUPIED


Creating a model
----------------

.. automethod:: CompartmentedModel.__init__


Building the model
------------------

Building a model means specifying the various compartments, loci, and events,
and their associated probabilities. These methods are typically
called from the :neth:`build` method, which is called during set-up to
build the model using the experiment's simulation parameters.  

.. automethod:: CompartmentedModel.addCompartment

.. automethod:: CompartmentedModel.addLocus

.. automethod:: CompartmentedModel.addEvent


Model setup
-----------

Immediately before being run, the model is set up by placing all
the nodes into compartments chosen randomly from the initial
compartment distribution defined by the probabilities passed to
:meth:`addCompartment` when the compartments are created. All edges
are also marked as unoccupied. 

.. automethod:: CompartmentedModel.setUp

.. automethod:: CompartmentedModel.initialCompartmentDistribution


Running the model
-----------------

The main mechanism for running a compartmented model is to change the
compartment of an individual node. This generally happens in event
functions. The events are triggered according to a probability
distribution that allows the dynamics to pick an event. Edges can also
be marked as "occupied" by the dynamics, meaning that they were
included in the spread of the disease.

.. automethod:: CompartmentedModel.changeCompartment

.. automethod:: CompartmentedModel.eventDistribution

.. automethod:: CompartmentedModel.markOccupied

 
Extracting basic results
------------------------

Once an experiment is run we will need to summarise the results. How
this is done depends on the dynamics and the simulation method, but
the :class:`CompartmentedModel` class provides some basic operations that can be
used.

.. automethod:: CompartmentedModel.results

.. automethod:: CompartmentedModel.skeletonise

		
