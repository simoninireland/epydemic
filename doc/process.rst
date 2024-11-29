:class:`Process`: Base class for network processes
==================================================

.. currentmodule:: epydemic

.. autoclass:: Process
   :show-inheritance:


.. note::

   Instance names can be any string: however, it may make other tasks
   easier if they are a single word without spaces or other characters
   that Python might become confused by in some contexts, for
   "First_disease" rather than "First disease" or "First.disease".


Setup and initialisation
------------------------

Five methods provide the core API for defining new processes, and are
typically overridden by sub-classes.

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


Setting and accessing parameters
--------------------------------

.. versionadded:: 1.14.1

   Parameter and result handling were changed in ``epydemic`` version
   1.14.1 to accommodate using multiple instances of a process within
   a single simulation.

The :meth:`Process.build` and :meth:`Process.setUp` methods pass
parameters to a process instance. You can access this dict directly,
or (better) access all the relevant parameters in one operation. This
approach works better when there may be multiple instances of a
process, because it automatically takes account of parameters
decorated with instance names.

.. note::

   See the :ref:`tutorial page on running a simulation
   <use-standard-model>` for an example using these functions, and
   the :ref:`cookbook recipe on co-infection <coinfection>` for an
   example using multiple instances.

.. automethod:: Process.getParameters

.. automethod:: Process.setParameters

If necessary you can decorate parameter names manually.

.. automethod:: Process.decoratedNameInInstance


Storing and accessing results
-----------------------------

.. versionadded:: 1.14.1

   Parameter and result handling were changed in ``epydemic`` version
   1.14.1 to accommodate using multiple instances of a process within
   a single simulation.

As with parameters, results may use decorated names to bind them to a
specific process instance.

.. automethod:: Process.setResults

.. automethod:: Process.getResults

As with parameters, :meth:`Process.decoratedNameInInstance` will
return the decorated name of any parameter or result. This is useful
when accessing a set of results through ``pandas``.


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


Identifiers for processes, runs, and state
------------------------------------------

Every process has an identifier that's guaranteed to be unique within
this simulation, and a run identifier that's guaranteed to be unique
to different runs of the same process instance. Taken together, these
two identifiers uniquely identify a single run of a single process
instance.

.. automethod:: Process.uniqueId

.. automethod:: Process.runId

There is a method for defining "constants" to be used as attributes on
nodes and edges for storing process state.

.. automethod:: Process.stateVariable

(See :ref:`subclassing` for an example of how to define state variables.)

Finally, names can be decorated with a process' instance name.

.. automethod:: Process.decoratedName

.. automethod:: Process.undecoratedName


Running multiple instances
--------------------------

You may also want to run several different instances of the same
process within a single simulation, for example when exploring
co-infection with two diseases having different spreading parameters.

.. note::

   ``epydemic`` has supported multiple process instances since version 1.14.1

In this case you can give names to process instances and use these
to decorate their parameters.

.. automethod:: Process.instanceName


Containment
-----------

Processes can have a hierarchy, for example when composed into a
:class:`ProcessSequence`. There are a couple of methods used to access
this hierarchy.

.. automethod:: Process.setContainer

.. automethod:: Process.container
