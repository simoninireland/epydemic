# Networks dynamics simulation base class
#
# Copyright (C) 2017--2021 Simon Dobson
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

import sys
from heapq import heappush, heappop
from networkx import Graph
from epydemic import NetworkExperiment, Locus, Process, NetworkGenerator, EventFunction, EventDistribution, Element
if sys.version_info >= (3, 8):
    from typing import Union, Final, Dict, List, Any, Optional, Tuple, Callable
else:
    # backport compatibility with older typing
    from typing import Union, Dict, List, Any, Optional, Tuple, Callable
    from typing_extensions import Final

# Event types (not exported outside this file)
PostedEventFunction = Callable[[], None]
PostedEvent = Tuple[float, int, PostedEventFunction]


class Dynamics(NetworkExperiment):
    '''An abstract simulation framework for running a process over a network.

    This is the abstract base class for implementing different kinds
    of network process dynamics as computational experiments suitable
    for running under ``epyc``. Sub-classes provide synchronous and
    stochastic (Gillespie) simulation dynamics.

    The dynamics runs a network process provided as a :class:`Process`
    object. It is provided with a network generator that is called to
    generate a new experimental network instance for each run. The
    generator can be any iterator but will typically be an instance of
    :class:`NetworkGenerator`.

    :param p: network process to run
    :param g: (optional) prototype network or network generator'''

    # Additional metadata elements
    TIME: Final[str] = 'epydemic.Dynamics.time'      #: Metadata element holding the logical simulation end-time.
    EVENTS: Final[str] = 'epydemic.Dynamics.events'  #: Metadata element holding the number of events that happened.

    def __init__(self, p: Process, g: Union[Graph, NetworkGenerator] = None):
        super().__init__(g)

        # initialise other fields
        self._eventId: int = 0                                             # counter for posted events
        self._process: Process = p                                         # network process to run
        self._simulationTime: float = 0.0                                  # on-going simulation time
        self._process.setDynamics(self)                                    # back-link from process to dynamics (for events)
        self._loci: Dict[str, Locus] = dict()                              # dict from names to loci
        self._processLoci: Dict[Process, Dict[str, Locus]] = dict()        # dict from processes to loci for events
        self._perElementEvents: Dict[Process, EventDistribution] = dict()  # dict from processes to events that occur per-element
        self._perLocusEvents: Dict[Process, EventDistribution] = dict()    # dict from processes to events that occur per-locus
        self._postedEvents: List[PostedEvent] = []                         # pri-queue of fixed-time events


    # ---------- Configuration ----------

    def process(self) -> Process:
        '''Return the network process being run.

        :returns: the process'''
        return self._process

    def currentSimulationTime(self) -> float:
        '''Return the current simulation time.

        :returns: the current time'''
        return self._simulationTime

    def setCurrentSimulationTime(self, t: float):
        '''Set the current simulation time. This should only be used by
        sub-classes when running the simulation: doing so in any other
        context risks damaging the simulation.

        :param t: the new simualtion time

        '''
        self._simulationTime = t


    # ---------- Results ----------

    def experimentalResults(self) -> Dict[str, Any]:
        '''Report the process' experimental results. This simply calls through
        to the :meth:`Process.results` method of the process being
        simulated.

        :returns: the results of the process

        '''
        return self._process.results()


    # ---------- Set-up and tear-down ----------

    def setUp(self, params: Dict[str, Any]):
        '''Set up the experiment for a run. This performs the inherited
        actions, then builds the network process that the dynamics is
        to run.

        :params params: the experimental parameters

        '''
        super().setUp(params)

        # set up the event stream
        self._loci = dict()
        self._processLoci = dict()
        self._perElementEvents = dict()
        self._perLocusEvents = dict()
        self._postedEvents = []
        self._eventId = 0
        self._simulationTime = 0.0

        # build and set up the process
        self._process.reset()
        self._process.build(params)
        self._process.setUp(params)

    def tearDown(self):
        '''At the end of each experiment, throw away any posted by un-executed
        events.

        '''
        self._process.tearDown()
        super().tearDown()
        self._postedEvents= []


    # ---------- Stochastic events (drawn from a distribution) ----------

    def addLocus(self, p: Process, n: str, l: Locus = None) -> Locus:
        """Add a named locus associated with the given process.

        :param p: the process
        :param n: the locus name
        :param l: the locus (defaults to a simple set-based locus)
        :returns: the locus"""
        if n in self._loci.keys():
            raise Exception("Locus {n} already exists in the simulation".format(n = n))

        # store locus by name
        if l is None:
            l = Locus(n)
        self._loci[n] = l

        # update process record
        if p not in self._processLoci:
            # new process, add loci and event lists
            self._processLoci[p] = dict()
            self._perElementEvents[p] = []
            self._perLocusEvents[p] = []
        self._processLoci[p][n] = l

        # return the locus
        return l

    def locus(self, n: str) -> Locus:
        '''Retrieve a locus by name.

        :param n: the locus name
        :returns: the locus'''
        return self._loci[n]

    def loci(self) -> Dict[str, Locus]:
        '''Return all the loci in the simulation.

        :returns: a dict from names to loci'''
        return self._loci

    def lociForProcess(self, p: Process) -> Dict[str, Locus]:
        '''Return all the loci defined for a specific process.

        :param p: the process
        :returns: a dict from names to loci'''
        if p in self._processLoci:
            # process has loci, return them
            return self._processLoci[p]
        else:
            # process doesn't have loci, return an empty dict
            return dict()

    def addEventPerElement(self, p: Process, l: Union[str, Locus], pr: float, ef: EventFunction):
        """Add a probabilistic event at a locus, occurring with a particular (fixed)
        probability for each element of the locus, and calling the :term:`event function`
        when it is selected.

        :param p: the process
        :param l: the locus or locus name
        :param pr: the event probability
        :param ef: the event function"""
        if isinstance(l, str):
            l = self.locus(l)
        self._perElementEvents[p].append((l, pr, ef))

    def perElementEventDistribution(self, p: Process, t: float) -> EventDistribution:
        """Return the distribution of per-element events for the given process' loci
        at the given time. By default the distribution is time-independent.

        :param p: the process
        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        if p in self._perElementEvents:
            return self._perElementEvents[p]
        else:
            return []

    def addFixedRateEvent(self, p: Process, l: Union[str, Locus], pr: float, ef: EventFunction):
        """Add a probabilistic event at a locus, occurring with a particular (fixed)
        probability, and calling the :term:`event function` when it is selected.

        :param p: the process
        :param l: the locus or locus name
        :param pr: the event probability
        :param ef: the event function"""
        if isinstance(l, str):
            l = self.locus(l)
        self._perLocusEvents[p].append((l, pr, ef))

    def fixedRateEventDistribution(self, p: Process, t: float) -> EventDistribution:
        """Return the distribution of fixed-rate events for the given process' loci
        at the given time. By default the distribution is time-independent.

        :param p: the process
        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        if p in self._perElementEvents:
            return self._perLocusEvents[p]
        else:
            return []

    def eventRateDistribution(self, t: float) -> EventDistribution:
        """Return the event distribution, a sequence of (l, r, f) triples
        where l is the locus where the event occurs, r is the rate at
        which an event occurs, and f is the event function called to
        make it happen.

        Note the distinction between a *rate* and a *probability*:
        the former can be obtained from the latter simply by
        multiplying the event probability by the number of times it's
        possible in the current network, which for per-element events
        is the population of nodes or edges in a given state.

        It is perfectly fine for an event to have a zero rate. The process
        is assumed to have reached equilibrium if all events have zero rates.

        :param t: current time
        :returns: a list of (locus, rate, event function) triples"""
        rates = []

        for p in self._perElementEvents:
            # convert per-element events to rates
            for (l, pr, ef) in self._perElementEvents[p]:
                rates.append((l, pr * len(l), ef))

            # add fixed-rate events for non-empty loci
            for (l, pr, ef) in self._perLocusEvents[p]:
                if len(l) > 0:
                    rates.append((l, pr, ef))

        return rates


    # ---------- Posted events (occurring at a fixed time) ----------

    def _nextEventId(self) -> int:
        """Generate a sequence number for a posted event. This is used to ensure that
        all event triples pushed onto the priqueue are unique in their first two elements,
        and therefore never try to do comparisons with functions (the third element).

        :returns: a sequence number"""
        id = self._eventId
        self._eventId += 1
        return id

    def postEvent(self, t: float, e: Element, ef: EventFunction):
        """Post an event that calls the :term:`event function` at time t.

        :param t: the current time
        :param e: the element (node or edge) on which the event occurs
        :param ef: the event function"""
        heappush(self._postedEvents, (t, self._nextEventId(), (lambda: ef(t, e))))

    def postRepeatingEvent(self, t: float, dt: float, e: Element, ef: EventFunction):
        """Post an event that starts at time t and re-occurs at interval dt.

        :param t: the start time
        :param dt: the interval
        :param e: the element (node or edge) on which the event occurs
        :param ef: the element function"""

        def repeat(tc, e):
            ef(tc, e)
            tp = tc + dt
            heappush(self._postedEvents, (tp, self._nextEventId(), (lambda: repeat(tp, e))))

        heappush(self._postedEvents, (t, self._nextEventId(), (lambda: repeat(t, e))))

    def nextPendingEventBefore(self, t: float) -> Optional[PostedEventFunction]:
        """Return the next pending event to occur at or before time t.

        :param t: the current time
        :returns: a pending event function or None"""
        if len(self._postedEvents) > 0:
            # we have events, grab the soonest
            (et, id, pef) = heappop(self._postedEvents)
            if et <= t:
                # event should have occurred, return
                return pef
            else:
                # this (and therefore all further events) are in the future, put it back
                heappush(self._postedEvents, (et, id, pef))
                return None
        else:
            # we don't have any events
            return None

    def runPendingEvents(self, t: float) -> int:
        '''Retrieve and fire any pending events at time t. This handles
        the case where firing an event posts another event that needs to be run
        before other already-posted events coming before time t: in other words,
        it ensures that the simulation order is respected.

        :param t: the current time
        :returns: the number of events fired'''
        n = 0
        while True:
            pef = self.nextPendingEventBefore(t)
            if pef is None:
                # no more pending events, return however many we've fired already
                return n
            else:
                # fire the event
                pef()
                n += 1
