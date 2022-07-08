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
from typing import Union, Dict, List, Any, Optional, Tuple, Callable, cast
if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final
from networkx import Graph
from epydemic import NetworkExperiment, Locus, Process, NetworkGenerator, EventFunction, EventDistribution, Element

# Event types (not exported outside this file)
PostedEventFunction = Callable[[], None]
PostedEvent = Tuple[float, int, Process, Optional[PostedEventFunction], Element, str]


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

    The dynamics also provides the interface for :ref:`event-taps`,
    allowing external code to tap-into the changes the experiment makes
    to the network. Sub-classes need to insert calls to this interface
    as appropriate, notably around the main body of the simulation and
    at each significant change.

    :param p: network process to run
    :param g: (optional) prototype network or network generator'''

    # Additional metadata elements
    TIME: Final[str] = 'epydemic.monitor.time'      #: Metadata element holding the logical simulation end-time.
    EVENTS: Final[str] = 'epydemic.monitor.events'  #: Metadata element holding the number of events that happened.


    def __init__(self, p: Process, g: Union[Graph, NetworkGenerator] = None):
        super().__init__(g)

        # initialise other fields
        self._eventId: int = 0                                             # counter for posted events
        self._process: Process = p                                         # network process to run
        self._process.setDynamics(self)                                    # back-link from process to dynamics (for events)
        self._simulationTime: float = 0.0                                  # on-going simulation time
        self._loci: Dict[str, Locus] = dict()                              # dict from names to loci
        self._processLoci: Dict[Process, Dict[str, Locus]] = dict()        # dict from processes to loci for events
        self._perElementEvents: Dict[Process, EventDistribution] = dict()  # dict from processes to events that occur per-element
        self._perLocusEvents: Dict[Process, EventDistribution] = dict()    # dict from processes to events that occur per-locus
        self._postedEvents: List[PostedEvent] = []                         # pri-queue of fixed-time events
        self._postedEventFinder: Dict[int, PostedEvent] = {}               # mapping from event id to event structure

        # initialise the event tap sub-system
        self.initialiseEventTaps()


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
        self._postedEventFinder = dict()
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

        # discard any remaining posted events
        self._postedEventFinder = {}
        self._postedEvents = []


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

        # link locus to the process that defined it
        l.setProcess(p)

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

    def addEventPerElement(self, p: Process, l: Union[str, Locus], pr: float,
                           ef: EventFunction, name: Optional[str] = None):
        """Add a probabilistic event at a locus, occurring with a particular
        (fixed) probability for each element of the locus, and calling
        the :term:`event function` when it is selected.

        The optional name is used in conjunction with
        :ref:`event taps <event-taps>` when calling :meth:`eventFired`.

        :param p: the process
        :param l: the locus or locus name
        :param pr: the event probability
        :param ef: the event function
        :param name: (optional) meaningful name of the event

        """
        if isinstance(l, str):
            l = self.locus(l)
        self._perElementEvents[p].append((l, pr, ef, name))

    def perElementEventDistribution(self, t: float) -> EventDistribution:
        """Return the distribution of per-element events for all processes' loci
        at the given time. By default the distribution is time-independent.

        Note that this method returns the *probability* of events, not their
        expected *rates*, for which use :meth:`perElementEventRateDistribution`.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        probs = []
        for p in self._perElementEvents:
            for (l, pr, ef, name) in self._perElementEvents[p]:
                probs.append((l, pr, ef, name))
        return probs

    def perElementEventRateDistribution(self, t: float) -> EventDistribution:
        """Return the rates of per-element events for all processes' loci
        at the given time. By default the distribution is time-independent.

        Note that this is method returns event *rates*, not their *probabilities*
        as returned by :meth:`perElementEventDistribution`. The rate is simply
        an event's probability multiplied by the size of the locus on which it occurs,
        giving the expected number of events occurring from that locus in unit time.

        :param t: the simulation time
        :returns: a list of (locus, rate, event function) triples"""
        rates = []
        for (l, pr, ef, name) in self.perElementEventDistribution(t):
            rates.append((l, pr * len(l), ef, name))
        return rates

    def addFixedRateEvent(self, p: Process, l: Union[str, Locus], pr: float,
                          ef: EventFunction, name: Optional[str] = None):
        """Add a probabilistic event at a locus, occurring with a particular
        (fixed) probability, and calling the :term:`event function`
        when it is selected.

        The optional name is used in conjunction with
        :ref:`event taps <event-taps>` when calling :meth:`eventFired`.

        :param p: the process
        :param l: the locus or locus name
        :param pr: the event probability
        :param ef: the event function
        :param name: (optional) meaningful name of the event

        """
        if isinstance(l, str):
            l = self.locus(l)
        self._perLocusEvents[p].append((l, pr, ef, name))

    def fixedRateEventDistribution(self, t: float) -> EventDistribution:
        """Return the distribution of fixed-rate events for all processes' loci
        at the given time. By default the distribution is time-independent.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        rates = []
        for p in self._perLocusEvents:
            for (l, pr, ef, name) in self._perLocusEvents[p]:
                if len(l) > 0:
                    rates.append((l, pr, ef, name))
        return rates

    def eventRateDistribution(self, t: float) -> EventDistribution:
        """Return the event distribution, a sequence of (l, r, f, n) tuples
        where l is the locus where the event occurs, r is the rate at
        which an event occurs, f is the event function called to
        make it happen, and n is the event name (which may be None).

        Note the distinction between a *rate* and a *probability*:
        the former can be obtained from the latter simply by
        multiplying the event probability by the number of times it's
        possible in the current network, which for per-element events
        is the population of nodes or edges in a given state.

        It is perfectly fine for an event to have a zero rate. The process
        is assumed to have reached equilibrium if all events have zero rates.

        :param t: current time
        :returns: a list of (locus, rate, event function, event name) tuples"""
        return self.perElementEventRateDistribution(t) + self.fixedRateEventDistribution(t)


    # ---------- Posted events (occurring at a fixed time) ----------

    def _nextEventId(self) -> int:
        """Generate a sequence number for a posted event. This is used to ensure that
        all event triples pushed onto the priqueue are unique in their first two elements,
        and therefore never try to do comparisons with functions (the third element).

        :returns: a sequence number"""
        id = self._eventId
        self._eventId += 1
        return id

    def postEvent(self, t: float, p: Process, e: Element, ef: EventFunction,
                  name: Optional[str] = None) -> int:
        """Post an event that calls the :term:`event function` at time t.
        A unique id it returned that can be used to remove the event
        before it fires using :meth:`unpostEvent`.

        The optional name is used in conjunction with
        :ref:`event taps <event-taps>` when calling :meth:`eventFired`.

        :param t: the current time
        :param p: the process originating the event
        :param e: the element (node or edge) on which the event occurs
        :param ef: the event function
        :param name: (optional) meaningful name of the event
        :returns: the event id

        """
        if t < self.currentSimulationTime():
            ct = self.currentSimulationTime()
            raise ValueError(f'Posting event in the past ({t} < {ct})')

        id = self._nextEventId()
        ev = [t, id, p, (lambda: ef(t, e)), e, name]
        self._postedEventFinder[id] = ev
        heappush(self._postedEvents, ev)
        return id

    def postRepeatingEvent(self, t: float, dt: float, p: Process, e: Element,
                           ef: EventFunction, name: Optional[str] = None):
        """Post an event that starts at time t and re-occurs at interval dt.
        Repeating events can't be removed once posted.

        The optional name is used in conjunction with
        :ref:`event taps <event-taps>` when calling :meth:`eventFired`.

        :param t: the start time
        :param dt: the interval
        :param p: the process originating the event
        :param e: the element (node or edge) on which the event occurs
        :param ef: the element function
        :param name: (optional) meaningful name of the event

        """

        # event function to fire an event and then re-schedule it
        def repeat(tc, e):
            ef(tc, e)
            self.postEvent(tc + dt, p, e, repeat, name)

        self.postEvent(t, p, e, repeat, name)

    def unpostEvent(self, id: int, fatal: bool = True) -> Optional[float]:
        '''Un-post a posted event. This is only legal before the
        event has fired, and will normally raise a KeyError if called on one
        that's not queued: set fatal to False to avoid this.

        :param id: the event id
        :param fatal: whether to raise KeyError for missing events (defaults to True)
        :returns: the simulation time at which the event would have fired, or None'''
        pe = self._postedEventFinder.get(id, None)

        # decide what to do if there's no such event
        if pe is None:
            if fatal:
                raise KeyError(id)
            else:
                return None

        # replace the event function with a dummy
        pe[3] = None

        # remove from the event finder
        del self._postedEventFinder[id]

        # return the time for which the event was scheduled
        return pe[0]

    def pendingEventTime(self, id: int) -> float:
        '''Return the time for which the given event is posted for. This will
        raise a KeyError if the event isn't in the queue, thrtough having fired
        or being un-posted.

        :poram id: the event
        :returns: the event's posted simulation time'''
        (et, _, _, _, _, _)  = self._postedEventFinder[id]
        return et

    def _discardUnpostedEvents(self):
        '''Chew-up and discard any unposted events at the head of the posted
        event queue. After a call to this method the next event on the
        posted event queue (if there is one) is guaranteed to be "real".'''
        while len(self._postedEvents) > 0:
            (_, id, _, ef, _, _) = self._postedEvents[0]
            if ef == None:
                # the head event has been unposted, discard it
                heappop(self._postedEvents)
            else:
                # head event is "real", we're done
                break

    def nextPendingEvent(self) -> Optional[PostedEvent]:
        '''Return the next posted event, or `None` if there are no events.

        :returns: the next posted event or None'''
        self._discardUnpostedEvents()
        if len(self._postedEvents) > 0:
            # return the next event
            pe = heappop(self._postedEvents)
            (_, id, _, ef, _, _) = cast(PostedEvent, pe)
            del self._postedEventFinder[id]
            return pe
        else:
            # no posted events
            return None

        # if we get here there are no events remainiong
        return None

    def nextPendingEventTime(self) -> float:
        '''Return the simulation time for the next pending posted event, without
        affecting the event queue.

        :returns: the simulation time or None'''
        self._discardUnpostedEvents()
        if len(self._postedEvents) > 0:
            # return the next event time
            (et, _, _, _, _, _) = cast(PostedEvent, self._postedEvents[0])
            return et
        else:
            # no posted events
            return None

    def nextPendingEventBefore(self, t: float) -> Optional[PostedEvent]:
        """Return the next pending event to occur at or before time t.

        :param t: the current time
        :returns: a posted event or None"""
        et = self.nextPendingEventTime()
        if et is None:
            # no posted events remaining
            return None
        elif et <= t:
            # next event should be fired now
            return self.nextPendingEvent()
        else:
            # next event lies after the requested time
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
            pe = self.nextPendingEventBefore(t)
            if pe is None:
                # no more pending events, return however many we've fired already
                return n
            else:
                # fire the event
                (et, _, p, pef, e, name) = cast(PostedEvent, pe)
                self.setCurrentSimulationTime(et)  # set the correct time
                pef()
                self.eventFired(t, p, name, e)
                n += 1


    # ---------- Event taps ----------

    def initialiseEventTaps(self):
        '''Initialise the event tap sub-system, which allows external code
        access to the event stream of the simulation as it runs.

        The default does nothing.'''
        pass

    def simulationStarted(self, params: Dict[str, Any]):
        '''Called when the simulation has been configured and set up, any
        processes built, and is ready to run.

        The default does nothing.

        :param params: the experimental parameters'''
        pass

    def simulationEnded(self, res: Union[Dict[str, Any], List[Dict[str, Any]]]):
        '''Called when the simulation has stopped, immediately before tear-down.

        The default does nothing.

        :param res: the experimental results'''
        pass

    def eventFired(self, t: float, p: Process, name: str, e : Element):
        '''Respond to the occurrance of the given event. The method is
        passed the simulation time, originating process, event name,
        and the element affected -- and isn't passed the event
        function, which is used elsewhere.

        This method is called in the past tense, *after* the event function
        has been run. This lets the effects of the event be observed.

        The event name is simply the optional name that was given to the event
        when it was declared using :meth:`addEventPerElement` or
        :meth:`addFixedRateEvent`. It will be None if no name was provided.

        The default does nothing. It can be overridden by sub-classes to
        provide event-level logging or other functions.

        :param t: the simulation time
        :param p: the process firing the event
        :param name: the event name
        :param e: the element

        '''
        pass
