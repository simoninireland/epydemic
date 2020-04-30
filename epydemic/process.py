# Networks process base class
#
# Copyright (C) 2017--2020 Simon Dobson
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

from epydemic import Locus

class Process(object):
    """A process that runs over a network. This is the abstract base class for all network processes.
    It provides the essential routines to build, set-up, run, and extract results from a
    process. Sub-classes provide the actual behaviour by defining simulation events and
    attaching them to the network in different ways.

    A process defines is largely declarative, in the sense that it sets up event handlers
    and their probabilities. These are used by a process dynamics (a sub-class of :class:`Dynamics`)
    to actually run a simulation of the process.

    The process class includes an interface for interacting with the working network. The basic
    interface is extended and overridden in different sub-classes that interact with the network
    in different ways.
    """

    # defaults
    DEFAULT_MAX_TIME = 20000      #: Default maximum simulation time.

    def __init__(self):
        super(Process, self).__init__()

        # set the default maximum time, which persists across runs of the process
        self._maxTime = self.DEFAULT_MAX_TIME

        # reset this instance
        self.reset()


    # ---------- Setup and initialisation ----------

    def reset(self):
        """Reset the process ready to be built. This resets all the internal process state
        variables. Sub-classes should call the base method to make sure that the event
        sub-system is properly reset."""
        self._g = None

    def build(self, params):
        """Build the process model. This should be overridden by sub-classes, and should
        create the various elements of the model.

        :param params: the model parameters"""
        pass

    def setUp(self, params):
        """Set up the network under the given dynamics. The default does
        nothing: sub-classes should override it to initialise node states
        or establish other properties ready for the experiment.

        :param params: the simulation parameters"""
        pass

    def tearDown(self):
        """Tear down any structures built for this run of the process. The default does
        nothing."""
        pass

    def setNetwork(self, g):
        """Set the network the process is running over.

        :param g: the network"""
        self._g = g

    def network(self):
        """Return the network the process is running over.

        :returns: the network"""
        return self._g

    def setDynamics(self, d):
        '''Set the instance of :class:`Dynamics` that runs the process.

        :param d: the dynamics'''
        self._dynamics = d

    def dynamics(self):
        '''Return the instance of :class:`Dynamics` running this process.

        :returns: the dynamics'''
        return self._dynamics

    def setMaximumTime(self, t):
        """Set the maximum default simulation time. The default is given by :attr:`DEFAULT_MAX_TIME`.
        This is used by :meth:`atEquilibrium` as the default way to determine equilibrium.

        The maximum time may be slightly exceeded due to the ways in which events are drawn. 

        Setting the maximum time persists across runs of the process, and isn't reset to its
        default by calling :meth:`reset`.

        :param t: the maximum simulation time"""
        self._maxTime = t

    def maximumTime(self):
        """Return the maximum assumed simulation time.

        :returns: the maximum simulation time"""
        return self._maxTime


   # ---------- Termination and results ----------

    def atEquilibrium(self, t):
        """Test whether the process is an equilibrium. The default simply checks whether
        the simulation time exceeds the maximum given by :meth:`setMaximumTime`, which
        defaults to an arbitrary value given by :attr:`DEFAULT_MAX_TIME`.
        Sub-classes may override this to provide a more sensible definition: in many
        cases it makes sense to keep calling this method as part of any more advanced
        test, so as to cut-off runaway processes.

        :param t: the current simulation time
        :returns: True if the proceess is now at equilibrium"""
        return (t >= self.maximumTime())

    def results(self):
       """Create  and return an empty dict to be filled with experimental results.
       Sub-classes should extend this method to add results to the dict.

       :returns: an empty dict for experimental results"""
       return dict()


    # ---------- Accessing and evolving the network ----------

    def addNode(self, n, **kwds):
        """Add a node to the working network. Any keyword arguments added as node attributes

        :param n: the new node
        :param kwds: (optional) node attributes"""
        self.network().add_node(n, **kwds)

    def addNodesFrom(self, ns, **kwds):
        """Add all the nodes in the given iterable to the working network. Any keyword arguments are
        added as node attributes. This works by calling :meth:`addNode` for each
        element of the iterable.

        :param ns: an iterable collection of nodes
        :param kwds: (optional) node attributes"""
        for n in ns:
            self.addNode(n, **kwds)

    def removeNode(self, n):
        """Remove a node from the working network.

        :param n: the node"""
        self.network().remove_node(n)

    def removeNodesFrom(self, ns):
        """Remove all the nodes in the given iterable froim the working network. This works by
        iteratively calling :meth:`removeNode` for each element of the iterable collection.

        :param ns: an iterable collection of nodes"""
        for n in ns:
            self.removeNode(n)

    def addEdge(self, n, m, **kwds):
        """Add an edge between nodes. Any keyword arguments are added as edge attributes.
        If the endpoint nodes do not already exist then an exception is raised.

        :param n: the start node
        :param m: the end node
        :param kwds: (optional) edge attributes"""
        g = self.network()
        if n not in g:
            raise Exception('No node {n} in network'.format(n = n))
        if m not in g:
            raise Exception('No node {n} in network'.format(n = m))
        g.add_edge(n, m, **kwds)

    def addEdgesFrom(self, es, **kwds):
        """Add all the edges in the given iterable to the working network. Any keyword arguments are
        added as node attributes. This works by calling :meth:`addEdge` for each
        element of the iterable.

        :param es: an iterable collection of edges
        :param kwds: (optional) node attributes"""
        for e in es:
            (n, m) = e
            self.addEdge(n, m, **kwds)

    def removeEdge(self, n, m):
        """Remove an edge from the working network.

        :param n: the start node
        :param m: the end node"""
        self.network().remove_edge(n, m)

    def removeEdgesFrom(self, es):
        """Remove all the edges in the given iterable collection from the working network. This works
        by iteratively calling :meth:`removeEdge` for each edge in the iterable.

        :param es: an iterable collection of edges"""
        for e in es:
            self.removeEdge(*e)


    # ---------- Probabilistic and posted events ----------
    # These are helper methods that delegate to the dynamics

    def addLocus(self, n, l=None):
        """Add a named locus.

        :param n: the locus name
        :param l: the locus (defaults to a simple set-based locus)
        :returns: the locus"""
        return self._dynamics.addLocus(self, n, l)

    def loci(self):
        '''Return the names of the loci that this process added.

        :returns: a dict from names to loci'''
        return self._dynamics.lociForProcess(self)

    def locus(self, n):
        '''Return the named locus.

        :param n: the locus name
        :returns: the locus'''
        return self.loci()[n]

    def addEventPerElement(self, l, p, ef):
        """Add a probabilistic event at a locus, occurring with a particular (fixed)
        probability for each element of the locus, and calling the :term:`event function`
        when it is selected. The locus may be a :class:`Locus` object or a string, which
        is taken to be a locus of this process.

        Unlike fixed probability events added by :meth:`addFixedRateEvent`, a per-element
        event happens with the same probability to each element in the locus. This leads to
        larger loci giving rise to a higher rate of events.

        :param l: the locus or locus name
        :param p: the event probability
        :param ef: the event function"""
        self._dynamics.addEventPerElement(self, l, p, ef)

    def addFixedRateEvent(self, l, p, ef):
        """Add a probabilistic event at a locus, occurring with a particular (fixed)
        probability, and calling the :term:`event function`
        when it is selected. The locus may be a :class:`Locus` object or a string, which
        is taken to be the name of a locus of this process.

        Unlike fixed rate events added by :meth:`addEventPerElement`, a fixed probability
        event happens with the same probability regardless of how many elements are in
        the locus.

        :param l: the locus or locus name
        :param p: the event probability
        :param ef: the event function"""
        self._dynamics.addFixedRateEvent(self, l, p, ef)

    def postEvent(self, t, e, ef):
        """Post an event that calls the :term:`event function` at time t.

        :param t: the current time
        :param e: the element (node or edge) on which the event occurs
        :param ef: the event function"""
        self._dynamics.postEvent(t, e, ef)

    def postRepeatingEvent(self, t, dt, e, ef):
        """Post an event that starts at time t and re-occurs at interval dt.

        :param t: the start time
        :param dt: the interval
        :param e: the element (node or edge) on which the event occurs
        :param ef: the element function"""
        self._dynamics.postRepeatingEvent(t, dt, e, ef)


    # ---------- Event distributions ----------

    def perElementEventDistribution(self, t):
        """Return the distribution of per-element events at time t relevant to
        this process. The list only contains those loci that this process defined.

        The default is to use the distribution directly from the dynamics, which is
        time-independent. Sub-classes can extend this method to provide time dependency
        if needed.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        return self._dynamics.perElementEventDistribution(self)

    def fixedRateEventDistribution(self, t):
        """Return the distribution of fixed-rate events at time t. relevant to
        this process. The list only contains those loci that this process defined.

        The default is to use the distribution directly from the dynamics, which is
        time-independent. Sub-classes can extend this method to provide time dependency
        if needed.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        return self._dynamics.fixedRateEventDistribution(self)

    def eventRateDistribution(self, t):
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

        # convert per-element events to rates
        for (l, pr, ef) in self.perElementEventDistribution(t):
            rates.append((l, pr * len(l), ef))

        # add fixed-rate events for non-empty loci
        for (l, pr, ef) in self.fixedRateEventDistribution(t):
            if len(l) > 0:
                rates.append((l, pr, ef))
        return rates






