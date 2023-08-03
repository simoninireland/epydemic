:class:`NetworkExperiment`: An experiment over a network
========================================================

.. currentmodule:: epydemic

.. autoclass:: NetworkExperiment
   :show-inheritance:


In use
------

:class:`NetworkExperiment` simply adds functions to associate a network or a network
generator with a computational experiment.

.. automethod:: NetworkExperiment.network

.. automethod:: NetworkExperiment.setNetworkGenerator

.. automethod:: NetworkExperiment.networkGenerator

During set-up the experiment instantiates a working copy network for
use within the experiment, deleting it afterwards. If the experiment
was provided with a single "prototype" network, whis is copied each
time; if it was provided with an instance of
:class:`NetworkGenerator`, a new instance of the class of networks
defined by the generator is used.

.. automethod:: NetworkExperiment.setUp
