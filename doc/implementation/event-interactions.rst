.. _implementation-event-interactions:

.. currentmodule:: epydemic

Event interactions and statistical exactness
============================================

A discrete-event simulator works by constructing a sequence of events
that happen within the system being modelled. The macro-scale behaviour
of a process is often independent of the exact sequence chosen,
within limits, but the micro-scale behaviour is always affected by the
events and their order -- and sometimes the micro-scale choices have
macro-scale effects too. This is a consequence of most network
processes being *complex systems* where macro properties emerge from
micro interactions in complex ways.

In ``epydemic`` the :class:`Dynamics` sub-classes are responsible for
choosing and firing events. Their behaviour is described in
:ref:`implementation-dynamics`: in this note we discuss the
effects that different detailed event sequence choices may have and
how they are made in the different dynamics regimes.


Stochastic dynamics: one event at a time
----------------------------------------

The stochastic or Gillespie dynamics of :class:`StochasticDynamics` is
generally considered to be the best choice for simulation. There are a
couple of reasons for this. It is almost always faster than
synchronous dynamics because it deals very time-efficiently with
choices of events.

But the preference for stochastic dynamics really comes from its
mathematical properties. Gillespie simulation is *statistically
exact*: at a time :math:`t`, the probability of choosing an event
:math:`e_t` will depend on the effects of all the events that have
happened since :math:`t = 0`. The changes in the probabilities of
events are often small, but there can be processes in which there are
rapid changes because (for example) there are lots of events firing in
a short space of time, or an event causes some significant change in
the system's future behaviour.


Synchronous dynamics: events in tranches
----------------------------------------

In contrast, synchronous dynamics works in discrete timesteps. At each
timestep it determines a tranche of events that can fire, and then fires
them in sequence.

It's worth pausing to consider the difference in the two mechanisms.
Stochastic dynamics chooses a time in the future and an event to happen
at that time, fires that event, and repeats. Synchronous dynamics
advances the simulation time by 1, chooses all events to fire in that
time interval, fires them in sequence, and repeats.

The synchronous approach can be easier to understand for some people,
and it allows more flexibility for the programmer (since all choices
aren't embedded into probabilities). However, it's important to
realise that the synchronous dynamics is *statistically inexact*.

The reason for this inexactness is that, when the synchronous dynamics
chooses the tranche of events to fire in a timestep, it does so based
on all the events that have happened in previous tranches -- but *not*
on the events in *this* tranche. Suppose that within a timestep an
event :math:`e_i` is fired, and in doing so removes an element from
its locus. What happens if, later in the timestep, there is an event
:math:`e_j` that was chosen to fire on this element? Clearly it can't
now happen, and :class:`SynchronousDynamics` checks for this to make
sure we don't fire such extraneous events.

But this means that not all of the events in a tranche -- the events
that were deemed "fire-able" -- will *be* fired, because the effects
of other events that were not accounted for when populating the
tranche of events nonetheless interfere with our ability to actually
fire events. It is this dependency on the exact details of event
ordering within a tranche that causes the statistical inexactness of
synchronous dynamics.


.. _implementation-event-orderings:

Event orderings
---------------

If the ordering of events within a tranche can have an impact, then we
need to consider how we *choose* that ordering. This turns out to be
an interesting question.

The ordering may not have much of an impact at all: all event
orderings within a timestep may lead to roughly the same macro
behaviour.

But this isn't *necessarily* the case. It turns out there are
processes whose end-state behaviours are critically dependent on
ordering choices when performed under synchronous dynamics. Moreover,
in contrast to the :term:`SIR` process we showed when :ref:`discussing
the two dynamics sub-classes <implementation-dynamics>`, there are
process for which different choices of ordering may cause the *same*
process to exhibit *different* behaviours under synchronous and
stochastic dynamics.

The event ordering is decided by
:meth:`SynchronousDynamics.allEventsInTimestep`, which can be
overridden. Its default behaviour is to extract stochastic events in
the order in which they were registered in the :meth:`Process.build`
method, and then extract the fixed-rate events in the order *they*
were registered.

Other ordering choices may also make sense, though. For example, one
might prefer an ordering in which all events for a given locus --
stochastic and fixed-rate -- happened together. One might want to
shuffle the order in which loci are considered at each timestep,
either randomly or round-robin. Or one might want to mix together the
events in a timestep to reduce the possibility that a particular
choice of locus orderings might change the process' behaviour.

This last choice some close to the behaviour of stochastic dynamics,
and unless there is a reason for choose synchronous dynamics one might
be better just to change dynamics and avoid the issues altogether.

It's worth repeating that *any* ordering choice under synchronous
dynamics *will* be statistically inexact. Nonetheless the synchronous
approach remains prevalent in the network science literature, so if
you're wanting to use ``epydemic`` to reproduce someone else's
experiment it's worth remembering the implications of different event
orderings when building the simulation -- and matching your choice to
the one they use.
