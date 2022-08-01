.. _implementation-event-times:

.. currentmodule:: epydemic

Event times
===========

``epydemic`` include two kinds of events: a :term:`stochastic event`
drawn from a probability distribution; and a :term:`posted event`.
In a :term:`continuous time` system the times at which these events
can occur are represented by floating-point numbers: not actually
continuous, of course, but continuous enough for proper simulation.

Problems can arise when using floating-point numbers indiscriminately,
however. Many operations inevitably lead to rounding errors, and this
can cause some hard-to-find bugs where two values that "should" be
equal aren't within the implementation. Normally all we require of two
simulation times is that we can determine whether one happens before
the other, and there is no enormous problem if rounding causes two
times to be swapped (or indeed made equal).

However, if we perform more complex and more essential calculations
with event times, we may find ourselves trying to determine more than
just an ordering. In this case, rounding errors can suddenly appear
and become significant.

This situation arises in the implementation of :ref:`pulse-coupled
oscillators <pulsecoupled>` Each oscillator has an associated phase, a
state, and a posted event that will cause it to fire when its state
next hits 1. Rather than store phase and state explicitly, we compute
them from the event time. This means we don't run the risk of the
three values becoming inconsistent; however, it also means that we
need to calculate with, and test equality on, event times. So not just
an ordering. At this point we may observe rounding errors.

There is a simple solution to this problem. Rather than use the full
generality of floating-point numbers for phases and event times, we
can "quantise" the values so that they occur with fine granularity but
a fixed precision. Since rounding errors typically occur only at high
decimal places, and since we don't actually *need* to represent time
to arbitrary precision, we can avoid the cases in which rounding
errors affect us.

There are two places we could implement this:

1. locally, within the :class:`PulseCoupledOscillator` class, by
   quantising the values we use for phases; or
2. globally, within the :class:`Dynamics` class, to only allow event
   times to happen to a given precision.

We've chosen the former as a simpler and less burdensome approach,
encapsulated within the :meth:`PulseCoupledOscillator.normalisePhase`
method. This might turn out not to have been the right choice in the
long run, and if more situations arise in which unrestricted event
times cause problems we may change to the latter. In the meantime, if
you find yourself interacting with event times, please be careful
about the numerical precision.
