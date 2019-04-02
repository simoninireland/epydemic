The simulation process
======================

.. currentmodule:: epydemic

The process of simulating processes (including epidemic processes) on networks is
quite involved and quite computationally expensive. `epydemic` implements simulations
in a way that aims to be as easy  as possible for programmers to specify while
also being as efficient as possible. There's a tension between these two goals, for
which `epydemic` tends to err on the side of simplicity: it's better to be correct,
but slower, than to be wrong, faster.

The `epydemic` simulation framework consists of a number of classes that you
sub-class to define the processes you want to simulate. There are three main classes
involved: processes, loci, and dynamics. We'll describe each class individually,
and then show how they fit together.


Processes
---------

The most important class is the :class:`Process`, which defines a stochastic process that
runs on a network. By "running on a network" we mean that the process defines the say that
the network evolves in time, which typically involves some or all of the following activities:

   - Changing the state of a node or edge, for example by changing the properties
     associated with them;
   - Adding or deleting nodes; and
   - Adding or deleting edges, also referred to a re-wiring.


Loci
----

A :class:`Locus` is a collection of nodes or edges at which changes occur. The easiest way
to think of a locus is simply as a set of nodes or edges characterised by some property. A
process then defines events that occur at a locus.


Dynamics
--------

A :class:`Dynamics` is a class that defines a particular way of performing a discrete-event
simulation. A dynamics describes the way in which a process is applied to evolve the network.
While it's common (and indeed necessary) to define new process sub-classes, dynamics
can usually be treated just as "black box" frameworks whose inner workings seldom matter.

There are two kinds of dynamics currently supported by `epydemic`:

   - The :class:`SynchronousDynamics` works in discrete time. At each timestep it
     examines each node or edge in each locus and, for each event, decides whether that
     event occurs on that node.
   - The :class:`StochasticDynamics` works in continuous time using the mechanism of
     Gillespie simulation. It computes a joint probability distribution of events,
     nodes, and edges, and then draws the next event and its occurrance time  from
     this distribution. This can be very efficient if events are rare, since it jumps
     over times when "nothing happens".


