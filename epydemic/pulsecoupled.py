# A pulse-coupled oscillator process
#
# Copyright (C) 2017--2022 Simon Dobson
#
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from math import exp, log
from networkx import neighbors, complete_graph
import sys
from typing import Dict, Any
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final
from epydemic import rng, Process, Node, Element


class PulseCoupledOscillator(Process):
    '''A pulse-coupled oscillator :term:`synchronisation` process.
    This follows closely on the definition provided by Mirollo and
    Strogatz :cite:`MirolloStrogatz`, a model inspired by
    synchronising biological systems such as fireflies and human heart
    cells.

    The basic model consists of a collection of :math:`N` nodes, each
    equipped with a state and an oscillator. As the phase of each
    oscillator advances it advances the corresponding state variable.
    When the state reaches 1 the node is triggered and fires -- for
    example by emitting a pulse of light -- and resets its state and
    phase to 0. On observing such a pulse, each other node advances
    its own state by some amount :math:`\epsilon`. If this takes the node's
    state above 1, then it too resets its phase and state to 0, and is
    henceforth synchronised with the node that triggered it; otherwise
    the node's phase is advanced to match its new state.

    Note that, in this model, a node does *not* flash when it becomes
    synchronised, but is will flash after the next period (unless it
    again synchronises to another node before it fires). Note also
    that all synchronised nodes will fire at the same time, so there
    will be a potentially large number of flashes happening at the
    same time. (Both these properties can be relaxed.)

    In the original formulation :cite:`MirolloStrogatz` the
    oscillators sit in a complete network, so that every node observes
    flashes from every other node. This has the interesting property
    that, once synchronised, two nodes will *stay* synchronised, so the
    number of phases and the size of the largest set of synchronised
    are both monotonic (decreasing and increasing respectively). This
    isn't necessarily true for other networks.

    '''

    # Tuning parameters
    PHASE_PRECISION: int = 5                                       #: Number of places or precision for phases.

    # Experimental parameters
    PERIOD: Final[str] = 'epydemic.pulsecoupled.period'             #: Parameter name for the oscillator period.
    B: Final[str] = 'epydemic.pulsecoupled.dissipation'             #: Paramater name for the dissipation constant.
    COUPLING: Final[str] = 'epydemic.pulsecoupled.coupling'         #: Parameter name for firing coupling strength.

    # Results
    PHASES: Final[str] = 'epydemic.pulsecoupled.phases'             #: The final phases of all the nodes.
    FIRING_TIMES: Final[str] = 'epydemic.pulsecouplepd.firingTimes' #: A list of firing times.
    FIRING_NODES: Final[str] = 'epydemic.pulsecoupled.firingNodes'  #: A list of nodes firing at these times.

    # Model state placeholders
    NODE_EVENT_ID: str = None                                       #: Identifier of the next firing event.

    # Event names
    FIRED: Final[str] = 'epydemic.pulsecoupled.fired'               #: The name of the firing event.


    def __init__(self):
        super().__init__()

        # state variable tags
        self.NODE_EVENT_ID = self.stateVariable('event')

        # state
        self._period: float = 0.0              # period for oscillators
        self._b: float = 0                     # phase state function parameter
        self._coupling: float = 0.0            # coupling strength between oscillators
        self._firingTimes: List[float] = []    # firing times
        self._firingNodes: List[Node] = []     # node firing at these times


    # ---------- Helper methods ----------

    def normalisePhase(self, phi: float) -> float:
        '''Ensure the phase is normalised and quantised. This ensures
        that the phase is in the range :math:`[0.0, 1.0]` and stored to
        a precision set by :attr:`PHASE_PRECISION` to avoid problems with
        floating-point rounding.

        :param phi: the phase
        :returns: the normalised phase'''
        return  max(min(round(phi, self.PHASE_PRECISION), 1.0), 0.0)

    def getFiringTime(self, n: Node):
        '''Get the next firing time of a node.

        :param n: the node
        :returns: the next scheduled firing time'''
        g = self.network()
        id = g.nodes[n].get(self.NODE_EVENT_ID, None)
        if id is None:
            return None
        else:
            return self.pendingEventTime(id)

    def setFiringTime(self, n: Node, et: float):
        '''Set the next firing time of a node, replacing the
        currently-scheduled event.

        :param n: the node
        :param et: the next scheduled firing time'''
        g = self.network()

        # remove any existing firing event
        id = g.nodes[n].get(self.NODE_EVENT_ID, None)
        if id is not None:
            self.unpostEvent(id, fatal=False)

        # add a new firing event
        g.nodes[n][self.NODE_EVENT_ID] = self.postEvent(round(et, self.PHASE_PRECISION), n, self.fired, name=self.FIRED)

    def getPhase(self, t: float , n: Node, normalise: bool = False) -> float:
        '''Get the phase of a node. This is computed by working back
        from the next-scheduled firing time.

        By default this method returns the "raw" phase, and so treats phases
        of 0.0 and 1.0 as being different. Calling with `normalise = True` will
        map any phase of 1.0 to 0.0. This makes it easier to find all the nodes
        with oscillators at the same phase: however, it's sometimes important
        to differentiate the two values (such as when deciding if an oscillator
        should fire), so the default keeps the two phases distinct.

        :param t: the time
        :param m: the node
        :param normalise: (optional) if True, combine phases of 0.0 and 1.0 (defaults to False)
        :returns: the current phase'''
        g = self.network()

        # get the time at which we're supposed to fire next
        oldTime = self.getFiringTime(n)

        # compute the current phase
        phi = self.normalisePhase(1 - (oldTime - t) / self._period)

        # normalise if requested
        if phi == 1.0 and normalise:
            # wrap phase around
            phi = 0.0

        return phi

    def getState(self, t: float, n: Node) -> float:
        '''Get the state of the given node.

        :param t: the time
        :param n: the node
        :returns: the state of the node'''
        return self.phaseToState(self.getPhase(t, n))

    def setPhase(self, t: float, n: Node, phi: float):
        '''Set the phase of the given node. This re-sets the next
        firing time for the node.

        :param t: the time
        :param n: the node
        :param phi: the phase'''
        self.setFiringTime(n, t + self.normalisePhase(1 - phi) * self._period)


    # ---------- Phase and state management ----------

    def phaseToState(self, phi: float) -> float:    # f (2.15)
        '''Convert a phase to the corresponding state (function
        :math:`f` in :cite:`MirolloStrogatz`).

        :param phi: the phase
        :returns: the state'''
        return (1 / self._b) * log (1 + (exp(self._b) - 1) * phi)

    def stateToPhase(self, u: float) -> float:      # g (2.14)
        '''Convert a state to the corresponding phase (function
        :math:`g` in :cite:`MirolloStrogatz`).

        :param u: the state
        :returns: the phase'''
        return (exp(self._b * u) - 1) / (exp(self._b) - 1)

    def bumpPhase(self, phi: float) -> float:       # h (2.1)
        '''Advance the phase and state of a node after it has observed
        a firing (the "return map" function :math:`h` in :cite:`MirolloStrogatz`).
        By default this increments the state by the value given in the
        :attr:`COUPLING` parameter.

        :param phi: the phase
        :returns: the updated phase'''
        return self.normalisePhase(self.stateToPhase(self._coupling + self.phaseToState(phi)))


    # ---------- Dynamics management ----------

    def initialisePhases(self):
        '''Initialise the phases of the oscillators at all the nodes
        to a random value on the range :math:`[0.0, 1.0]`.'''
        g = self.network()
        for n in g.nodes():
            state = rng.random()
            phase = self.stateToPhase(state)
            self.setPhase(0.0, n, phase)
            #print(f'Node {n} phase {phase} fire {firingTime}')

    def fire(self, t: float, n: Node):
        '''Handle the firing of an oscillator, when its phase hits 1.
        This marks all neighbours for update and resets the phase of
        this node to 0.

        This method can be overridden to provide extra behaviours on
        firing. Be sure to call the base method first.

        :param t: the simulation time
        :param n: the node that is firing'''
        #print(f'fire {n}')

        g = self.network()

        # mark all adjacent nodes for bumping
        for m in neighbors(g, n):
            self._bumping.add(m)

        # re-set phase
        self.setPhase(t, n, 0.0)
        self._bumped.add(n)

    def synchronised(self, t: float, n: Node, m: Node):
        '''What to do when a node becomes synchronised with another.
        The default sets its phase to 0, meaning it will fire at
        the end of its next cycle: it *won't* fire now.

        :param t: the time
        :param n: the node that fired
        :param m: the node that is now newly-synchronised with n'''
        #print(f'Sync {m}')
        self.setPhase(t, m, 0.0)

    def cascade(self, t: float, n: Node, m: Node):
        '''Cascade the firing of one node into updating the phases
        of its neighbours, which may then synchronise them.

        :param t: the simulation time
        :param n: the node that fired
        :param m: the node being updated as a result of n firing'''

        # get the state
        state = self.getState(t, m)
        if state == 1.0 or state == 0.0:
            # already synchronised, and so will fire itself on schedule
            #print(f'pass {m}')
            pass
        else:
            # we're not synchronised, change phase
            newPhase = self.bumpPhase(self.getPhase(t, m))
            self.setPhase(t, m, newPhase)
            newState = self.getPhase(t, m)
            if newState == 1.0 or newState == 0.0:
                # this brought us to firing threshold
                self.synchronised(t, n, m)


    # ---------- Events ----------

    def fired(self, t: float, n: Node):
        '''The event called when a node's oscillator hits a phase
        of 1.0. This triggers the node, firing it and incrementing the
        phases of all its neighbours.

        We track all the nodes that are triggered as a result of this
        event to ensure that they are only triggered at most once in
        any cascade.

        :param t: the simulation time
        :param n: the node that is firing'''
        #print(f'*** {n} fired at {t} ***')

        # set up sets for bumped nodes
        self._bumping = set()
        self._bumped = set()

        # fire the node
        self.fire(t, n)

        # save the firing node and firing time
        self._firingTimes.append(t)
        self._firingNodes.append(n)

        # run state updates for all bumped nodes
        while len(self._bumping) > 0:
            m = self._bumping.pop()
            if m not in self._bumped:
                self.cascade(t, n, m)
                self._bumped.add(m)


    # ---------- Experiment management ----------

    def setUp(self, params: Dict[str, Any]):
        '''Initialise the oscillator phases.

        :param params: the experimental parameters'''
        super().setUp(params)
        self.initialisePhases()

    def build(self, params: Dict[str, Any]):
        '''Build the oscillator model.

        Each parameter gets a default of 1 if not set explicitly.

        :param params: the experimental parameters'''
        super().build(params)

        # grab the parameters
        self._period = params.get(self.PERIOD, 1.0)      # defaults to unit period
        self._b = params.get(self.B, 1.0)                # defaults to unit dissipation
        self._coupling = params.get(self.COUPLING, 1.0)  # defaults to unit coupling

        # set up the result arrays
        self._firingTimes = []
        self._firingNodes = []

    def results(self) -> Dict[str, Any]:
        '''Add the final phases of all oscillators to the results.

        :returns: the experimental results'''
        rc = super().results()

        # final phases of all oscillators
        g = self.network()
        t = self.currentSimulationTime()
        rc[self.PHASES] = [self.getPhase(t, n) for n in g.nodes()]

        # firing times
        rc[self.FIRING_TIMES] = self._firingTimes
        rc[self.FIRING_NODES] = self._firingNodes

        return rc
