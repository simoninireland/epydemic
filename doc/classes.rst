.. _classes:

.. currentmodule:: epydemic

Class structure
===============

Simulation framework
--------------------

.. inheritance-diagram:: StochasticDynamics SynchronousDynamics
			 Locus
			 Process CompartmentedModel
   :parts: 1
   :top-classes: Experiment

Processes
---------

.. inheritance-diagram:: SIR SIS SEIR SIRS
			 SIR_FixedRecovery SIR_VariableInfection SIS_FixedRecovery
			 AddDelete Percolate Monitor NetworkStatistics
			 ProcessSequence
   :parts: 1

Percolation
-----------

.. inheritance-diagram:: SitePercolation BondPercolation
   :parts: 1


Network generators
------------------

.. inheritance-diagram:: FixedNetwork ERNetwork BANetwork PLCNetwork
   :parts: 1
