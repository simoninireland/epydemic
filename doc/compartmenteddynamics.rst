Dynamics for compartmented models
=================================

.. currentmodule:: epydemic

The :class:`SynchronousDynamics` and :class:`StochasticDynamics`
classes define the basic mechanisms for the two main process
simulation approaches. In both cases, there is a common way to run
processes specified with compartmented models that massively simplify
the creation of simulations. 

In practice, these classes typically require no sub-classing, as all the
variant behaviour can be more effectively provided in the code for
the :term:`compartmented model of disease` in a :class:`CompartmentedModel`
sub-class.


:class:`CompartmentedStochasticDynamics`
-----------------------------------------

.. autoclass:: CompartmentedStochasticDynamics
   :show-inheritance:
	 
To set up the experiment we provide the parameters for the experiment
as usual.

.. automethod:: CompartmentedStochasticDynamics.setUp

Running the model requires that we convert the event *probability*
distribution into an event *rate* distribution.

.. automethod:: CompartmentedStochasticDynamics.eventRateDistribution

Finally, we defer the experimental results collection to the model.

.. automethod:: CompartmentedStochasticDynamics.experimentalResults


:class:`CompartmentedSynchronousDynamics`
-----------------------------------------

.. autoclass:: CompartmentedSynchronousDynamics
   :show-inheritance:
	 
To set up the experiment we provide the parameters for the experiment
as usual.

.. automethod:: CompartmentedSynchronousDynamics.setUp

Under synchronous dynamics we use the model-provided event
probabilities to test whether an event occurred at each possible locus
in each discrete timestep.

.. automethod:: CompartmentedSynchronousDynamics.eventDistribution

Finally, we defer the experimental results collection to the model.

.. automethod:: CompartmentedSynchronousDynamics.experimentalResults
