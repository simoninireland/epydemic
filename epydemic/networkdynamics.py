# Networks dynamics simulation base class
#
# Copyright (C) 2017 Simon Dobson
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

import epyc
import networkx
from heapq import *


class Dynamics(epyc.Experiment, object):
    '''A dynamical process over a network. This is the abstract base class
    for implementing different kinds of dynamics as computational experiments
    suitable for running under. Sub-classes provide synchronous and stochastic
    (Gillespie) simulation dynamics.

    The dynamics optionally takes a parameter providing a prototype network
    that will be used for each experimental run.

    :param g: prototype network (optional)'''

    # Additional metadata elements
    TIME = 'simulation_time'      #: Metadata element holding the logical simulation end-time.
    EVENTS = 'simulation_events'  #: Metadata element holding the number of events that happened.

    # the default maximum simulation time
    DEFAULT_MAX_TIME = 20000      #: Default maximum simulation time.
    
    def __init__( self, g = None ):
        super(Dynamics, self).__init__()
        self._graphPrototype = g                 # prototype copied for each run
        self._graph = None                       # working copy of prototype
        self._maxTime = self.DEFAULT_MAX_TIME    # time allowed until equilibrium
        self._posted = []                        # pri-queue of fixed-time events

    def network( self ):
        '''Return the network this dynamics is running over.

        :returns: the network'''
        return self._graph

    def setNetworkPrototype( self, g ):
        '''Set the network the dynamics will run over. This will be
        copied for each run of an individual experiment.

        :param g: the network'''
        self._graphPrototype = g

    def networkPrototype( self ):
        '''Return the prototype network used to create the working
        copy.

        :returns: the prototype network'''
        return self._graphPrototype
    
    def setMaximumTime( self, t ):
        '''Set the maximum default simulation time. The default is given
        by :attr:`DEFAULT_MAX_TIME`.

        param: t: the maximum time'''
        self._maxTime = t
        
    def at_equilibrium( self, t ):
        '''Test whether the model is an equilibrium. Override this method to provide
        alternative and/or faster simulations.
        
        :param t: the current simulation timestep
        :returns: True if we're done'''
        return (t >= self._maxTime)

    def setUpNetwork( self, params ):
        '''Set up the working copy of the network for this run of the
        experiment, as will be returned by :meth:`network`. By default
        this makes a copy of the prototype network, but the method may
        be overridden to create a network locally if desired, making use
        of the experimental parameters.

        :param params: the experiment parameters
        :returns: a working network'''
        return self.networkPrototype().copy()
    
    def setUp( self, params ): 
        '''Before each experiment, create a new network to work with.

        :param params: parameters of the experiment'''

        # perform the default setup
        super(Dynamics, self).setUp(params)

        # make a copy of the network prototype
        self._graph = self.setUpNetwork(params)

        # empty the queue of posted events
        self._posted = []

    def tearDown( self ):
        '''At the end of each experiment, throw away the copy.'''

        # perform the default tear-down
        super(Dynamics, self).tearDown()

        # throw away the worked-on model
        self._graph = None
        self._posted = []

    def eventDistribution( self, t ):
        '''Return the event distribution, a sequence of (l, p, f) triples
        where l is the :term:`locus` of the event, p is the probability of an
        event occurring, and f is the :term:`event function` called to make it
        happen. This method must be overridden in sub-classes.
        
        It is perfectly fine for an event to have a zero probability.

        :param t: current time
        :returns: the event distribution'''
        raise NotYetImplemented('eventDistribution()')

    def postEvent( self, t, g, e, ef ):
        '''Post an event to happen at time t. The :term:`event function` should
        take the dynamics, simulation time, network, and element for the event.
        At time t it is called with the given network and element.

        :param t: the current time
        :param g: the network
        :param e: the element (node or edge) on which the event occurs
        :param ef: the event function'''
        heappush(self._posted, (t, (lambda: ef(self, t, g, e))))

    def _nextPendingEventBefore( self, t ):
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
        
    def pendingEvents( self, t ):
        '''Retrieve any :term:`posted event` scheduled to be fired at or
        before time t. The pending events are returned in the form of
        zero-argument functions that can simply be called to fire
        the corresponding event. The events are returned as a list with the
        earliest-posted event first.

        Be aware that running the returned events in order may not be enough to
        accurately run the simulation in the case where firing an
        event causes another event to be posted before t. It may be
        easier to use :meth:`runPendingEvents` to run all pending
        events, which handles this case automatically.

        :param t: the current time
        :returns: a (possibly empty) list of pending event functions'''
        pending = []
        while True:
            pef = self._nextPendingEventBefore(t)
            if pef is None:
                # no more events pending, return those we've got
                return pending
            else:
                # store the pending event function
                pending.append(pef)

    def runPendingEvents( self, t):
        '''Retrieve and fire any pending events at time t. This method handles
        the case where firing an event posts another event that needs to be run
        before other already-posted events coming before time t: in other words,
        it ensures that the simulation order is respected.

        :param t: the current time
        :returns: the number of events fired'''
        n = 0
        while True:
            pef = self._nextPendingEventBefore(t)
            if pef is None:
                # no more pending events, return however many we've fired already
                return n
            else:
                # fire the event
                pef()
                n = n + 1
                
