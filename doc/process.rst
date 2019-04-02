:class:`Process`: Base class for network processes
==================================================

.. currentmodule:: epydemic

.. autoclass:: Process


Getting ready to run
--------------------

A process is provided by the simulation dynamics with the network over which it is
running. This can then be accessed from the main methods.

.. automethod:: Process.setNetwork

.. automethod:: Process.network

.. automethod:: Process.reset


Important methods for sub-classes
---------------------------------

Three methods proivide the core API for defining new processes.

.. automethod:: Process.build

.. automethod:: Process.setUp

.. automethod:: Process.results


Loci
----

Loci are the "locations" at which things happen. The purpose of a :class:`Locus` is to keep
track of something -- a set of nodes, the entire network, and so forth -- so that
simulation can proceed efficiently.

.. automethod:: Process.addLocus

.. automethod:: Process.locus

Loci also provide an operator interface.

.. automethod:: Process.__getitem__

.. automethod:: Process.__setitem__

.. automethod:: Process.__contains__

.. automethod:: Process.__iter__

Loci are generally transparent to to process-writers, however, as the following helper
methods provide standard ways to create them.

.. automethod:: Process.trackNetwork

.. automethod:: Process.trackAllNodes

.. automethod:: Process.trackAllEdges


Events
------

Events are the code fragments that run as part of the simulation. The collection
of events defined by a process form all the possible actions that the simulation
will perform. Events are stochastic, being equipped with a probability of
occurrance that the dynamics uses when selecting when and what event to fire.

.. automethod:: Process.addEvent

.. automethod:: Process.eventDistribution
