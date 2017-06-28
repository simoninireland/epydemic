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
    (Gillespie) simulation dynamics.'''

    # Additional metadata elements
    TIME = 'simulation_time'      #: Metadata element holding the logical simulation end-time.
    EVENTS = 'simulation_events'  #: Metadata element holding the number of events that happened.

    # the default maximum simulation time
    DEFAULT_MAX_TIME = 20000      #: Default maximum simulation time.
    
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given network.
        The network (if provided) is treated as a prototype that is copied before
        each individual simulation experiment.
        
        :param g: prototype network (optional)'''
        super(Dynamics, self).__init__()
        self._graphPrototype = g
        self._graph = None
        self._maxTime = self.DEFAULT_MAX_TIME
        self._posted = []

    def network( self ):
        '''Return the network this dynamics is running over.

        :returns: the network'''
        return self._graph

    def setNetworkPrototype( self, g ):
        '''Set the network the dynamics will run over. This will be
        copied for each run of an individual experiment.

        :param g: the network'''
        self._graphPrototype = g

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

    def setUp( self, params ): 
        '''Before each experiment, create a working copy of the prototype network.

        :param params: parameters of the experiment'''

        # perform the default setup
        super(Dynamics, self).setUp(params)

        # make a copy of the network prototype
        self._graph = self._graphPrototype.copy()

        # empty the queue of posted events
        self._posted = []

    def tearDown( self ):
        '''At the end of each experiment, throw away the copy.'''

        # perform the default tear-down
        super(Dynamics, self).tearDown()

        # throw away the worked-on model
        self._graph = None
        
    def postEvent( self, t, g, e, ef ):
        '''Post an event to happen at time t. The :term:`event function` should
        take the simulation time, network, and element for the event. At time t
        it is called with the given network and element.

        :param t: the current time
        :param g: the network
        :param e: the element (node or edge) on which the event occurs
        :param ef: the event function'''
        heappush(self._posted, (t, (lambda: ef(t, g, e))))

    def pendingEvents( self, t ):
        '''Retrieve any :term:`posted event` pending to be executed at or
        before time t.  The pending events are returned in the form of
        zero-argument functions that can simply be called to execute
        the events. The events are returned as a list, with the
        earliest-posted event first.

        It may be easier to use :meth:`runPendingEvents` to automatically
        run all pending events.

        :param t: the current time
        :returns: a (possibly empty) list of pending event functions'''
        pending = []
        while len(self._posted) > 0:
            (et, pef) = heappop(self._posted)
            if et <= t:
                # event should have occurred, store it
                pending.append(pef)
            else:
                # this and further events are in the future, put it back
                heappush(self._posted, (et, pef))
                break

        # return the pending events, if any
        return pending

    def runPendingEvents( self, t):
        '''Retrieve and fire any pending events at time t.

        :param t: the current time
        :returns: the number of events fired'''
        pefs = self.pendingEvents(t)
        n = len(pefs)
        for i in range(n):
            pef = pefs[i]
            pef()
        return n
