.. _classes:

.. currentmodule:: epydemic

Class structure
===============

.. inheritance-diagram:: StochasticDynamics SynchronousDynamics
   :parts: 1
   :top-classes: Experiment

.. inheritance-diagram:: SIR SIS SEIR SIRS
			 SIR_FixedRecovery SIS_FixedRecovery
			 AddDelete Percolate Monitor NetworkStatistics
			 ProcessSequence
   :parts: 1

.. inheritance-diagram:: FixedNetwork ERNetwork BANetwork PLCNetwork
   :parts: 1
