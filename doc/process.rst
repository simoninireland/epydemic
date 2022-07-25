:class:`Process`: Base class for network processes
==================================================

.. currentmodule:: epydemic

.. autoclass:: Process
   :show-inheritance:


Setup and initialisation
------------------------

Five methods provide the core API for defining new processes, and are typically overridden by sub-classes.

.. automethod:: Process.reset

.. automethod:: Process.build

.. automethod:: Process.setUp

.. automethod:: Process.tearDown

.. automethod:: Process.dynamics

.. automethod:: Process.currentSimulationTime

.. automethod:: Process.results


Process hierarchy
-----------------

Processes can be nested, for example using a :class:`ProcessSequence`.
The component processes can be accessed using a common interface:

.. automethod:: Process.processes

.. automethod:: Process.allProcesses


Getting ready to run
--------------------

Several other methods provide information for the process.

.. automethod:: Process.setNetwork

.. automethod:: Process.network

.. automethod:: Process.setDynamics

.. automethod:: Process.dynamics

.. automethod:: Process.setMaximumTime

.. automethod:: Process.maximumTime



Accessing and evolving the network
----------------------------------

A process will generally want to access the working network in the course of its execution,
mainly in event functions. Accessing the network can be done directly, through :meth:`network`:
however, processes often need to track changes made to the network, and for this reason the
class provides an interface for evolving the network, paralleling the methods available
in `networkx`.

The interface may be overridden and extended by sub-classes. Three methods form the general core.

.. automethod:: Process.addNode

.. automethod:: Process.removeNode

.. automethod:: Process.addEdge

.. automethod:: Process.removeEdge

Four other "bulk" methods are deinfed in terms of the basic methods, and so don't typically
need to be overridden specifically.

.. automethod:: Process.addNodesFrom

.. automethod:: Process.removeNodesFrom

.. automethod:: Process.addEdgesFrom

.. automethod:: Process.removeEdgesFrom


Loci
----

Loci are the "locations" at which things happen. The purpose of a :class:`Locus` is to keep
track of something -- a set of nodes, the entire network, and so forth -- so that
simulation can proceed efficiently.

.. automethod:: Process.addLocus

.. automethod:: Process.loci

.. automethod:: Process.locus


Events
------

Events are the code fragments that run as part of the simulation. The
collection of events defined by a process form all the possible
actions that the simulation will perform. Events can be given
meaningful names, which don't affect the execution of the simulation.

There are three broad classes of events. *Per-element* events occur
with a probability on each element of a locis. This means that loci
with more elements will generate a higher rate of events.

.. automethod:: Process.addEventPerElement

*Fixed-rate* events, by contrast, occur with a probability that's
independent of the number of elements in a locus, as long as it's not
empty. This means that the rate at which such events fire is
independent of the size of the locus.

.. automethod:: Process.addFixedRateEvent

These two kinds of events are both *stochastic*, in the sense that
they are generated according to an exponential probability
distribution.

In contrast, *posted* events are set to occur at a particular
simulation time. As the simulation proceeds it will execute posted
events in the correct time sequence relative to the different
stochastic events that are generated.

.. automethod:: Process.postEvent

.. automethod:: Process.unpostEvent

.. automethod:: Process.pendingEventTime

.. automethod:: Process.postRepeatingEvent


Event distributions
-------------------

The stochastic events form probability distributions from which events
can be drawn in the course of the simulation. The events are added
using the methods above; the distributions are computed automatically.

.. automethod:: Process.perElementEventDistribution

.. automethod:: Process.perElementEventRateDistribution

.. automethod:: Process.fixedRateEventDistribution

In some cases it may be necessary to create the distributions
directly, in which case these methods can be overridden.


Identifiers for instances, runs, and state
------------------------------------------

Every process instance has an identifier that's guaranteed to be
unique within this simulation, and a run identifier that's
guaranteed to be unique to different runs of the same process
instance. Taken together, these two identifiers uniquely identify
a single run of a single process instance.

.. automethod:: Process.instanceId

.. automethod:: Process.runId

There is also a method for defining "constants" to be used as
attributes on nodes and edges for storing process state.

.. automethod:: Process.stateVariable

(See :ref:`subclassing` for an example of how to define state variables.)


Containment
-----------

Processes can have a hierarchy, for example when composed into a
:class:`ProcessSequence`. There are a couple of methods used to access
this hierarchy.

.. automethod:: Process.setContainer

.. automethod:: Process.container
