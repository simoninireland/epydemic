# Networks process base class
#
# Copyright (C) 2017--2019 Simon Dobson
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

from epydemic import *
from heapq import *
import six


class Process(object):
    '''A process that runs over a network. This is the abstract base class for all network processes.
    It provides the essential routines to build, set-up, run, and extract results from a
    process. Sub-classes provide the actual behaviour by defining simulation events and
    attaching them to the network in different ways.
    '''

    # defaults
    DEFAULT_MAX_TIME = 20000      #: Default maximum simulation time.


    def __init__( self ):
        super(Process, self).__init__()

        # set the default maximum time, which persists across runs of the process
        self._maxTime = self.DEFAULT_MAX_TIME

        # reset this instance
        self.reset()


    # ---------- Setup and initialisation ----------

    def reset( self ):
        '''Reset the process ready to be built.'''
        self._loci = dict()                          # loci for events
        self._g = None                               # working network
        self._perElementEvents = []                  # events that occur per-element
        self._perLocusEvents = []                    # events that occur per-locus
        self._posted = []                            # pri-queue of fixed-time events

    def build( self, params ):
        '''Build the process model. This must be overridden by sub-classes, and should
        call methods such as :meth:`addCompartment`, :meth:`addLocus`, and
        :meth:`addEvent` to create the various elements of the model.

        :param params: the model parameters'''
        raise NotImplementedError('build')

    def setUp(self, params):
        '''Set up the network under the given dynamics. The default does
        nothing: sub-classes should override it to initialise node states
        or establish other properties ready for the experiment.

        :param params: the simulation parameters'''
        pass

    def setNetwork(self, g):
        '''Set the network the process is running over.

        :param g: the network'''
        self._g = g

    def network(self):
        '''Return the network the process is running over.

        :returns: the network'''
        return self._g

    def setMaximumTime(self, t):
        '''Set the maximum default simulation time. The default is given by :attr:`DEFAULT_MAX_TIME`.
        This is used by :meth:`atEquilibrium` as the default way to determine equilibrium.

        Setting the maximum time persists across runs of the process, and isn't reset to its
        default by calling :meth:`reset`.

        :param t: the maximum simulation time'''
        self._maxTime = t

    def maximumTime(self):
        '''Return the maximum assumed simulation time.

        :returns: the maximum simulation time'''
        return self._maxTime


   # ---------- Termination and results ----------

    def atEquilibrium(self, t):
        '''Test whether the process is an equilibrium. The default simply checks whether
        the simulation time exceeds the maximum given by :meth:`setMaximumTime`, which
        defaults to an arbitrary value given by :attr:`DEFAULT_MAX_TIME`.
        Sub-classes may override this to provide a more sensible definition: in many
        cases it makes sense to keep calling this method as part of any more advanced
        test, so as to cut-off runaway processes.

        :param t: the current simulation time
        :returns: True if the proceess is now at equilibrium'''
        return (t >= self.maximumTime())

    def results(self):
       '''Create  and return an empty dict to be filled with experimental results.
       Sub-classes should extend this method to add results to the dict.

       :returns: an empty dict for experimental results'''
       return dict()


   # ---------- Loci for events ----------

    def addLocus(self, n, l = None):
        '''Add a named locus.

        :param n: the locus name
        :param l: the locus (defaults to a simple set-based locus)
        :returns: the locus'''
        if n in self._loci.keys():
            raise Exception("Trying to overwrite existing locus {n}".format(n = n))
        if l is None:
            l = Locus(n)
        self._loci[n] = l
        return l

    def __setitem__(self, n, l):
        '''Add a named locus. Equivalent to :meth:`addLocus`

        :param n: the locus name
        :param l: the locus
        :returns: the locus'''
        return self.addLocus(n, l)

    def locus(self, n):
        '''Return the named locus.

        :param n: the locus name
        :returns: the locus'''
        return self._loci[n]

    def __getitem__(self, n):
        '''Return the given locus. Equivalent to :meth:`locus`.

        :param n: the locus name
        :returns: the locus'''
        return self.locus(n)

    def __contains__(self, l):
        '''Check whether the given locus is defined for the process.

        :returns: the name of the loci'''
        return l in self._loci.keys()

    def __iter__(self):
        '''Return an iterator over the loci in the process.

        :returns: an iterator'''
        return iter(self._loci.keys())


    # ---------- Probabilistic events (occurring with some probability, either per-locus or per-element) ----------

    def addEventPerElement( self, l, p, ef ):
        '''Add a probabilistic event at a locus, occurring with a particular (fixed)
        probability for each element of the locus, and calling the :term:`event function`
        when it is selected. The locus may be a :class:`Locus` object or a string, which
        is taken to be a locus of this process.

        Unlike fixed probability events added by :meth:`addFixedRateEvent`, a per-element
        event happens with the same probability to each element in the locus. This leads to
        larger loci giving rise to a higher rate of events.

        :param l: the locus or locus name
        :param p: the event probability
        :param ef: the event function'''
        if isinstance(l, six.string_types):
            l = self.locus(l)
        self._perElementEvents.append((l, p, ef))

    def addFixedRateEvent( self, l, p, ef ):
        '''Add a probabilistic event at a locus, occurring with a particular (fixed)
        probability, and calling the :term:`event function`
        when it is selected. The locus may be a :class:`Locus` object or a string, which
        is taken to be the name of a locus of this process.

        Unlike fixed rate events added by :meth:`addEventPerElement`, a fixed probability
        event happens with the same probability regardless of how many elements are in
        the locus.

        :param l: the locus or locus name
        :param p: the event probability
        :param ef: the event function'''
        if isinstance(l, six.string_types):
            l = self.locus(l)
        self._perLocusEvents.append((l, p, ef))

    def perElementEventDistribution(self, t):
        """Return the distribution of per-element events at time t.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        return self._perElementEvents

    def fixedRateEventDistribution(self, t):
        """Return the distribution of fixed-rate events at time t.

        :param t: the simulation time
        :returns: a list of (locus, probability, event function) triples"""
        return self._perLocusEvents

    def eventRateDistribution(self, t):
        """Return the event distribution, a sequence of (l, r, f) triples
        where l is the locus where the event occurs, r is the rate at
        which an event occurs, and f is the event function called to
        make it happen.

        Note the distinction between a *rate* and a *probability*:
        the former can be obtained from the latter simply by
        multiplying the event probability by the number of times it's
        possible in the current network, which is the population
        of nodes or edges in a given state.

        It is perfectly fine for an event to have a zero rate. The process
        is assumed to have reached equilibrium if all events have zero rates.

        :param t: current time
        :returns: a list of (locus, rate, event function) triples"""
        rates = []

        # convert per-element events to rates
        for (l, p, ef) in self.perElementEventDistribution(t):
            rates.append((l, p * len(l), ef))

        # add fixed-rate events for non-empty loci
        for (l, p, ef) in self.fixedRateEventDistribution(t):
            if len(l) > 0:
                rates.append((l, p, ef))
        return rates


    # ---------- Posted events (ocurring at a fixed time ----------

    def postEvent(self, t, g, e, ef):
        '''Post an event to happen at time t. The :term:`event function` should
        take the dynamics, simulation time, network, and element for the event.
        At time t it is called with the given network and element.

        :param t: the current time
        :param g: the network
        :param e: the element (node or edge) on which the event occurs
        :param ef: the event function'''
        heappush(self._posted, (t, (lambda: ef(t, g, e))))

    def nextPendingEventBefore(self, t):
        '''Return the next pending event to occur at or before time t.

        :param t: the current time
        :returns: a pending event function or None'''
        if len(self._posted) > 0:
            # we have events, grab the soonest
            (et, pef) = heappop(self._posted)
            if et <= t:
                # event should have occurred, return it
                return pef
            else:
                # this (and therefore all further events) are in the future, put it back
                heappush(self._posted, (et, pef))
                return None
        else:
            # we don't have any events
            return None

    def pendingEvents(self, t):
        '''Retrieve any :term:`posted event` scheduled to be fired at or
        before time t. The pending events are returned in the form of
        zero-argument functions that can simply be called to fire
        the corresponding event. The events are returned as a list with the
        earliest-posted event first.

        Be aware that running the returned events in order may not be enough to
        accurately run the simulation in the case where firing an
        event causes another event to be posted before t. It may be
        easier to use :meth:`Dynamics.runPendingEvents` to run all pending
        events, which handles this case automatically.

        :param t: the current time
        :returns: a (possibly empty) list of pending event functions'''
        pending = []
        while True:
            pef = self.nextPendingEventBefore(t)
            if pef is None:
                # no more events pending, return those we've got
                return pending
            else:
                # store the pending event function
                pending.append(pef)





