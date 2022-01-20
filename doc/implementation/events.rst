.. _implementation-events:

.. currentmodule:: epydemic

Discrete-event simulation
=========================

``epydemic`` is basically a discrete-event simulator with a mixed
population of events.


The basics of discrete-event simulation
---------------------------------------

Discrete-event simulation represents a process as a sequence of events
happening in sequence. Each event happens at a specific instant in
time, and may give rise to further events to happen later. The job of
the simulator is to progress simulated time forward and execute the
events in the correct temporal order -- even though they may be have
been generated in some other order.

For example, suppose we have a sequence of events A, B, C, with A
scheduled to happen before B, and B before C. The execution of A might
given rise to two other events D and E where D occurs before B and E
occurs after B but before C. After executing A, the future event order
then becomes D, B, E, C, and the simulator will execute D next.

Clearly one cannot meaningfully create an event that should execute
before the current simulation time.


Event implementation
--------------------

Events are implemented in ``epydemic`` simply as methods on a
:class:`Process` object that are called when the event "fires". An
event is associated with a node or edge in the network, and can then
perform any arbitrary function relating to that network
element. (Examples include changing the :term:`compartments` of nodes,
or re-wiring edges.)

Events can also be named, which both provides a useful hook for
debugging and explanation, and is a key part of the
:ref:`event-taps` sub-system.


Posted and stochastic events
----------------------------

``epydemic`` supports two kinds of events: posted and stochastic.

A *posted* event is an event that happens at a specific, known,
simulation time. that is to say, *both* the event *and* the time when
it will happen are known when the event is created. Events are posted
by calling :meth:`Dynamics:postEvent`.

A *stochastic* event is an event chosen using a stochastic process,
meaning that the event happens (or doesn't) on some model element
(typically a node or edge). Events are declared using
:meth:`Dynamics.addFixedRateEventr` or :meth:`Dynamics.addEventPerElement`.
Exactly how these events are chosen depend on the dynamics used (see below).


Decomposition
-------------

Different parts of the code are responsible for different aspects of
the simulation.

The :class:`Dynamics` class abstracts the functions of the
simulator. It maintains an event queue containing all posted events,
the loci for stochastic events, and the event probabilities that apply
to those loci. Taken together, these form the distribution for
stochastic events.

Each dynamics class has an associated :class:`Process` instance which
build the process in terms of loci and event probabilities, and
defines the event functions. The :class:`SIR` process, for example,
has two events types (infection and removal). The probability of these
events occuring is a function of the number of SI edges and the number
of I nodes (two loci), and the disease dynamics specified when the
process is created.

The logic of this decomposition is that the :class:`Dynamics` holds
all the information relating to a single simulation run. The
:class:`Process` sets up the simulation and provides the logic for how
events are handled. This makes ``epydemic`` more flexible in two key
respects: it can support diffrent simulation dynamics using the same
process definition (see below), and it can combine processes together
to form composite processes.  Neither of these two options would be
available if we (for example) defined a process by sub-classing the
simulation dynamics directly.


.. _event-taps:

Event taps
----------

As well as evaluating an event function, the event stream is "tapped"
to a single well-known method, :meth:`Dynamics.eventFired`. This
allows sub-classes of :class:`Dynamics` to act on *every* event,
regardless of which process defines it and whether it was stochastic
or posted.

When events are defined or posted using the various methods, they can
optionally be given names. These names are then passed to
:meth:`Dynamics.eventFired`, and form the only way in which different
types of events can be differentiated.

This feature isn't used at all within "core" ``epydemic``, but is
provided as another extension mechanism that can be used if and when
needed.


Dynamics
--------

The concrete sub-classes of :class:`Dynamics` define exactly how all
these ideas are realised.

A :class:`SynchronousDynamics` is a :term:`discrete time`
simulator. At each timestep it runs all the events posted before this
time that remain to run, and then checks all the elements that *might*
have an event run on them and selects those that *do* undergo events
using the given event probability. This technique can be slower than
other approaches, but is needed for some processes where the global
distribution of events is hard to compute.

A :class:`StochasticDynamics` is a :term:`continuous time`
simulator. It maintains a joint probability distribution defining the
probability of a given event occurring in a given time interval into
the future. It draws from this distribution, advances the simulation
time by the chosen interval, runs any posted events that should have
occurred before this time, and then chooses an element on which to run
the event. This technique is known as :term:`Gillespie simulation` and
is both efficient and stochastically exact.
