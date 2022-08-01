# Networks process base class
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

from typing import Dict, List, Tuple, Any, Callable, Iterable, Union, Optional
from networkx import Graph
from epydemic import Node, Edge, Element

# There is a circular import between Process and Dynamics, and between
# Process and Locus, at the typing level (but not at the execution
# level), when providing types for dynamics() and setDynamics(). To
# deal with this we only import Dynamics in order to type-check
# Process, and not for execution.  (See
# https://www.stefaanlippens.net/circular-imports-type-hints-python.html)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from epydemic import Dynamics, Locus


# Types for handling events
EventFunction = Callable[[float, Element], None]                     #: Type of event-handler functions.
EventDistribution = List[Tuple['Locus', float, EventFunction, str]]  #: Type of event distributions.


class Process():
    """A process that runs over a network. This is the abstract base class
    for all network processes.  It provides the essential routines to
    build, set-up, run, and extract results from a
    process. Sub-classes provide the actual behaviour by defining
    simulation events and attaching them to the network in different
    ways.

    A process definition is largely declarative, in the sense that it
    sets up event handlers and their probabilities. These are used by
    a process dynamics (a sub-class of :class:`Dynamics`) to actually
    run a simulation of the process.

    Processes can be composed into larger structures, for example as part of
    a :class:`ProcessSequence`.

    The process class includes an interface for interacting with the
    working network. The basic interface is extended and overridden in
    different sub-classes that interact with the network in different
    ways. The process also provides helper methods to save explicit
    use of the :class:`Dynamics` when writing events.

    """

    # defaults
    DEFAULT_MAX_TIME: float = 20000.0      #: Default maximum simulation time.
    INSTANCE_SEQ: int = 0                  #: Process instance sequence number.

    def __init__(self):
        super().__init__()

        # set the default maximum time, which persists across runs of the process
        self._maxTime = self.DEFAULT_MAX_TIME

        # set the hierarchy
        self._containerProcess: 'Process' = None

        # set the identifiers
        self._instanceId = Process.INSTANCE_SEQ
        Process.INSTANCE_SEQ += 1
        self._runId = 0

        # reset this instance
        #self.reset()


    # ---------- Process instance and run identifiers ----------

    def processes(self) -> List['Process']:
        '''Return a list of component processes. For a standard process
        this is just the process itself.

        :returns: a list containing this process'''
        return [self]

    def allProcesses(self) -> List['Process']:
        '''Return a recursive list of component processes. For a standard process
        this is the same as calling :math:`processes`..

        :returns: a list containing this process'''
        return self.processes()

    def instanceId(self) -> int:
        '''Return the unique instance identifier of this process.

        :returns: the instacne id'''
        return self._instanceId

    def runId(self) -> int:
        '''Return the unique run identifier for the current run. This
        is updated whenever the process is reset by a call to :meth:`reset`.

        :returns: the run id'''
        return self._runId


    # ---------- Process state variables ----------

    def stateVariable(self, stem: str) -> str:
        '''Create a unique name for a state variable using the given stem.
        The default combines the stem with the process instance id.

        :param stem: the name stem
        :returns: the state variable name'''
        return '{s}-{n}'.format(s=stem, n=self.instanceId())


    # ---------- Process containment ----------

    def setContainer(self, ps: 'Process'):
        '''Register this process as being composed as part of another process.

        :param ps: the containing process'''
        self._containerProcess = ps

    def container(self) -> 'Process':
        '''Return the container process this process is part of. This will
        be None for "simple" processes.

        :return: the container process or None'''
        return self._containerProcess


    # ---------- Setup and initialisation ----------

    def reset(self):
        """Reset the process ready to be built. This resets all the internal
        process state variables.

        """
        self._runId += 1
        self._perElementEvents = []
        self._perLocusEvents = []

    def build(self, params: Dict[str, Any]):
        """Build the process model. This should be overridden by sub-classes,
        and should create the various elements of the model.

        :param params: the model parameters

        """
        pass

    def setUp(self, params: Dict[str, Any]):
        """Set up the network under the given dynamics. The default does
        nothing: sub-classes should override it to initialise node states
        or establish other properties ready for the experiment.

        :param params: the simulation parameters

        """
        pass

    def tearDown(self):
        """Tear down any structures built for this run of the process. The
        default does nothing.

        """
        pass


    # ---------- State access and update ----------

    def setNetwork(self, g: Graph):
        """Set the network the process is running over.

        :param g: the network

        """
        self._dynamics.setNetwork(g)

    def network(self) -> Graph:
        """Return the network the process is running over.

        :returns: the network

        """
        return self._dynamics.network()

    def setDynamics(self, d: 'Dynamics'):
        '''Set the instance of :class:`Dynamics` that runs the process.

        :param d: the dynamics'''
        self._dynamics = d

    def dynamics(self) -> 'Dynamics':
        '''Return the instance of :class:`Dynamics` running this process.

        :returns: the dynamics

        '''
        return self._dynamics

    def setMaximumTime(self, t: float):
        """Set the maximum default simulation time. The default is given by
        :attr:`DEFAULT_MAX_TIME`.  This is used by
        :meth:`atEquilibrium` as the default way to determine
        equilibrium.

        The maximum time may be slightly exceeded due to the ways in
        which events are drawn.

        Setting the maximum time persists across runs of the process,
        and isn't reset to its default by calling :meth:`reset`.

        :param t: the maximum simulation time

        """
        self._maxTime = t

    def maximumTime(self) -> float:
        """Return the maximum assumed simulation time.

        :returns: the maximum simulation time"""
        return self._maxTime


    # ---------- Termination and results ----------

    def currentSimulationTime(self) -> float:
        '''Return the current simulation time. Only makes sense
        when called from a running simulation.

        :returns: the time'''
        return self.dynamics().currentSimulationTime()

    def atEquilibrium(self, t: float) -> bool:
        """Test whether the process is an equilibrium. The default simply
        checks whether the simulation time exceeds the maximum given
        by :meth:`setMaximumTime`, which defaults to an arbitrary
        value given by :attr:`DEFAULT_MAX_TIME`.  Sub-classes may
        override this to provide a more sensible definition: in many
        cases it makes sense to keep calling this method as part of
        any more advanced test, so as to cut-off runaway processes.

        :param t: the current simulation time
        :returns: True if the proceess is now at equilibrium

        """
        return (t >= self.maximumTime())

    def results(self) -> Dict[str, Any]:
        """Create and return an empty dict to be filled with experimental
        results.  Sub-classes should extend this method to add results
        to the dict.

        :returns: an empty dict for experimental results
        """
        return dict()


    # ---------- Accessing and evolving the network ----------

    def addNode(self, n: Node, **kwds):
        """Add a node to the working network. Any keyword arguments added as node attributes

        :param n: the new node
        :param kwds: (optional) node attributes"""
        self.network().add_node(n, **kwds)

    def addNodesFrom(self, ns: Iterable[Node], **kwds):
        """Add all the nodes in the given iterable to the working network. Any
        keyword arguments are added as node attributes. This works by
        calling :meth:`addNode` for each element of the iterable.

        :param ns: an iterable collection of nodes
        :param kwds: (optional) node attributes

        """
        for n in ns:
            self.addNode(n, **kwds)

    def removeNode(self, n: Node):
        """Remove a node from the working network.

        :param n: the node"""
        self.network().remove_node(n)

    def removeNodesFrom(self, ns: Iterable[Node]):
        """Remove all the nodes in the given iterable from the working
        network. This works by iteratively calling :meth:`removeNode`
        for each element of the iterable collection.

        :param ns: an iterable collection of nodes

        """
        for n in ns:
            self.removeNode(n)

    def addEdge(self, n: Node, m: Node, **kwds):
        """Add an edge between nodes. Any keyword arguments are added as edge
        attributes.  If the endpoint nodes do not already exist then
        an exception is raised.

        :param n: the start node
        :param m: the end node
        :param kwds: (optional) edge attributes

        """
        g = self.network()
        if n not in g:
            raise Exception('No node {n} in network'.format(n=n))
        if m not in g:
            raise Exception('No node {n} in network'.format(n=m))
        g.add_edge(n, m, **kwds)

    def addEdgesFrom(self, es: Iterable[Edge], **kwds):
        """Add all the edges in the given iterable to the working network. Any
        keyword arguments are added as node attributes. This works by
        calling :meth:`addEdge` for each element of the iterable.

        :param es: an iterable collection of edges
        :param kwds: (optional) node attributes

        """
        for e in es:
            (n, m) = e
            self.addEdge(n, m, **kwds)

    def removeEdge(self, n: Node, m: Node):
        """Remove an edge from the working network.

        :param n: the start node
        :param m: the end node"""
        self.network().remove_edge(n, m)

    def removeEdgesFrom(self, es: Iterable[Edge]):
        """Remove all the edges in the given iterable collection from the
        working network. This works by iteratively calling
        :meth:`removeEdge` for each edge in the iterable.

        :param es: an iterable collection of edges

        """
        for e in es:
            self.removeEdge(*e)


    # ---------- Probabilistic events ----------

    def addLocus(self, n: str, l: 'Locus' = None) -> 'Locus':
        """Add a named locus.

        :param n: the locus name
        :param l: the locus (defaults to a simple set-based locus)
        :returns: the locus"""
        return self._dynamics.addLocus(self, n, l)

    def loci(self) -> Dict[str, 'Locus']:
        '''Return the names of the loci that this process added.

        :returns: a dict from names to loci'''
        return self._dynamics.lociForProcess(self)

    def locus(self, n: str) -> 'Locus':
        '''Return the named locus.

        :param n: the locus name
        :returns: the locus'''
        return self.loci()[n]

    def addEventPerElement(self, l: Union[str, 'Locus'], pr: float,
                           ef: EventFunction, name: Optional[str] = None):
        """Add a probabilistic event at a locus, occurring with a particular
        (fixed) probability for each element of the locus, and calling
        the :term:`event function` when it is selected.

        The optional name is used in conjunction with
        :ref:`event taps <event-taps>` when calling :meth:`eventFired`.

        :param l: the locus or locus name
        :param pr: the event probability
        :param ef: the event function
        :param name: (optional) meaningful name of the event

        """
        if isinstance(l, str):
            l = self.locus(l)
        self._perElementEvents.append((l, pr, ef, name))

    def perElementEventDistribution(self, t: float) -> EventDistribution:
        """Return the distribution of per-element events at the given time.
        By default the distribution is time-independent.

        Note that this method returns the *probability* of events, not their
        expected *rates*, for which use :meth:`perElementEventRateDistribution`.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        return self._perElementEvents

    def perElementEventRateDistribution(self, t: float) -> EventDistribution:
        """Return the rates of per-element events at the given time.
        By default the distribution is time-independent.

        Note that this is method returns event *rates*, not their *probabilities*
        as returned by :meth:`perElementEventDistribution`. The rate is simply
        an event's probability multiplied by the size of the locus on which it occurs,
        giving the expected number of events occurring from that locus in unit time.

        :param t: the simulation time
        :returns: a list of (locus, rate, event function) triples"""
        return [(l, pr * len(l), ef, name) for (l, pr, ef, name) in self.perElementEventDistribution(t)]

    def addFixedRateEvent(self, l: Union[str, 'Locus'], pr: float,
                          ef: EventFunction, name: Optional[str] = None):
        """Add a probabilistic event at a locus, occurring with a particular
        (fixed) probability, and calling the :term:`event function`
        when it is selected. The locus may be a :class:`Locus` object
        or a string, which is taken to be the name of a locus of this
        process. This is a helper method that calls :meth:`Dynamics.addFixedRateEvent`
        on the dynamics running the process.

        Unlike fixed rate events added by :meth:`addEventPerElement`,
        a fixed probability event happens with the same probability
        regardless of how many elements are in the locus.

        :param l: the locus or locus name
        :param pr: the event probability
        :param ef: the event function
        :param name: (optional) meaningful name of the event

        """
        if isinstance(l, str):
            l = self.locus(l)
        self._perLocusEvents.append((l, pr, ef, name))

    def fixedRateEventDistribution(self, t: float) -> EventDistribution:
        """Return the distribution of fixed-rate events at the given time.
        By default the distribution is time-independent.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        return self._perLocusEvents


    # ---------- Posted events ----------
    # These are helper methods that delegate to the dynamics

    def postEvent(self, t: float, e: Any,
                  ef: EventFunction, name: Optional[str] = None) -> int:
        """Post an event that calls the :term:`event function` at time t.
        This is a helper method that calls :meth:`Dynamics.postEvent`
        on the dynamics running the process.

        :param t: the time to fire the event
        :param e: the element (node or edge) on which the event occurs
        :param ef: the event function
        :param name: (optional) meaningful name of the event

        """
        return self._dynamics.postEvent(t, self, e, ef, name)

    def unpostEvent(self, id: int, fatal: bool = True) -> Optional[float]:
        """Un-post the given event.
        This is a helper method that calls :meth:`Dynamics.postEvent`
        on the dynamics running the process.

        A KeyError will normally be raised if the event
        is not queued, which typically means it's been fired already
        (*i.e.*, its posting time lies in the past relative to the current
        simulation time): set fatal to False to avoid this.

        :param id: the event id
        :param fatal: whether to raise KeyError for missing events (defaults to True)
        :returns: the time for which the event was posted, or None

        """
        return self._dynamics.unpostEvent(id, fatal)

    def pendingEventTime(self, id: int) -> float:
        '''Return the time for which the given event is posted. This is
        a helper event trhat calls :meth:`Dynamics.pendingEventTime`. A KeyError
        will be raised if the event is not queued, which typically means it's been fired already
        (*i.e.*, its posting time lies in the past relative to the current
        simulation time).

        :parfam, id: the event
        :returns: the event's posted simulation time'''
        return self._dynamics.pendingEventTime(id)

    def postRepeatingEvent(self, t: float, dt: float, e: Any,
                           ef: EventFunction, name: Optional[str] = None):
        """Post an event that starts at time t and re-occurs at interval dt.
        This is a help[er methoid that calls :meth:`Dynamics.postRepeatingEvent`
        on the dynamics running the process.

        :param t: the start time
        :param dt: the interval
        :param e: the element (node or edge) on which the event occurs
        :param ef: the element function
        :param name: (optional) meaningful name of the event

        """
        self._dynamics.postRepeatingEvent(t, dt, self, e, ef, name)
