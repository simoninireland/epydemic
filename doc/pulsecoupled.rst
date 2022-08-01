.. _pulsecoupled:

:class:`PulseCoupledOscillator`: The canonical synchronisation process
======================================================================

.. currentmodule:: epydemic

.. autoclass:: PulseCoupledOscillator
   :show-inheritance:


Parameters
----------

.. autoattribute:: PulseCoupledOscillator.PERIOD

.. autoattribute:: PulseCoupledOscillator.B

.. autoattribute:: PulseCoupledOscillator.COUPLING

Note that, unlike many processes, these parameters all have defaults
set in :meth:`PulseCoupledOscillator.build`.


Results
-------

.. autoattribute:: PulseCoupledOscillator.PHASES

.. autoattribute:: PulseCoupledOscillator.FIRING_TIMES

.. autoattribute:: PulseCoupledOscillator.FIRING_NODES


State variables
---------------

The only state variable holds an internal identifier for the posted
event that will fire the node. It's highly unlikely this will be
useful outside the mechanics of the simulation.

.. autoattribute:: PulseCoupledOscillator.NODE_EVENT_ID


Core parts of the oscillator process
------------------------------------

The model is initialised by giving a phase to every oscillator.

.. automethod:: PulseCoupledOscillator.initialisePhases

The behaviour of firing, obsevration of flashes, and synchronisation
of one oscillator to another can all be overridden or extended.

.. automethod:: PulseCoupledOscillator.fire

.. automethod:: PulseCoupledOscillator.cascade

.. automethod:: PulseCoupledOscillator.synchronised


Setup and initialisation
------------------------

.. automethod:: PulseCoupledOscillator.build

.. automethod:: PulseCoupledOscillator.setUp

.. automethod:: PulseCoupledOscillator.results


Events
------

The process defines one event that occurs whenever a node fires.

.. automethod:: PulseCoupledOscillator.fired

.. autoattribute:: PulseCoupledOscillator.FIRED


Managing state and phase
------------------------

The state and phase parts of the system are managed by a pair of
functions that convert between them.

.. automethod:: PulseCoupledOscillator.phaseToState

.. automethod:: PulseCoupledOscillator.stateToPhase

These are combined to advance the phase of an oscillator according to
flashes it observes.

.. automethod:: PulseCoupledOscillator.bumpPhase

The state and phase of an oscillator are managed using a small set of
methods that manage the next firing time of an oscillator (if left to
its own devices, without being updated).

.. automethod:: PulseCoupledOscillator.getPhase

.. automethod:: PulseCoupledOscillator.setPhase

.. automethod:: PulseCoupledOscillator.getState

.. automethod:: PulseCoupledOscillator.setFiringTIme

.. automethod:: PulseCoupledOscillator.getFiringTime

It is important to manage the phase carefully to avoid numerical
instability caused by unrestricted use of floating-point operations.
Phases are kept in the range :math:`[0.0, 1.0]` and held to a fixed
numerical precision defined by
:attr:`PulseCoupledOscillator.PHASE_PRECISION`. (See :ref:`the
implementation note on event times <implementation-event-times>` for a
discussion of this.)

.. automethod:: PulseCoupledOscillator.normalisePhase


Tuning parameters
-----------------

The precision with which phases are held can be changed if required
-- although the default is almost certainly adequate.

.. autoattribute:: PulseCoupledOscillator.PHASE_PRECISION
