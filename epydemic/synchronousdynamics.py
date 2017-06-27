# Synchronous dynamics base class
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

from epydemic import *

import epyc
import networkx
import numpy
from copy import copy

class SynchronousDynamics(Dynamics):
    '''A dynamics that runs synchronously in discrete time, applying local
    rules to each node in the network. These are simple to understand and
    simple to code for many cases, but can be statistically inexact and slow
    for large systems.'''

    # additional metadata
    TIMESTEPS_WITH_EVENTS = 'timesteps_with_events'  #: Metadata element holding the number timesteps that actually had events occur within them

    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given prototype
        network.
        
        :param g: prototype network to run over (optional)'''
        super(SynchronousDynamics, self).__init__(g)

    def eventDistribution( self, t ):
        '''Return the event distribution, a sequence of (l, p, f) triples
        where l is the locus for the event, p is the probability of an
        event occurring, and f is the event function called to make it
        happen. This method must be overridden in sub-classes.
        
        It is perfectly fine for an event to have a zero probability.

        :param t: current time
        :returns: the event distribution'''
        raise NotYetImplementedError('eventDistribution()')

    def dynamics( self, t, params ):
        '''Run a single step of the model over the network.

        Event functions may return False to indicate that the event didn't fire,
        which the dynamics treats as identical to not having selecetd that particular
        element of the locus for an event.
        
        :param t: the current timestep
        :param params: the parameters of the simulation
        :returns: the number of dynamic events that happened in this timestep'''
        g = self.network()
        events = 0
        
        # retrieve all the events, their loci, probabilities, and event functions
        dist = self.eventDistribution(t)

        # run through all the events
        for (l, p, f) in dist:
            # run through every possible element on which this event may occur
            for e in copy(l.elements()):
                # test for occurrance of the event on this element
                if numpy.random.random() < p:
                    # yes, perform the event
                    happened = f(t, g, e)
                    if happened:
                        # event happened, update the event count
                        events = events + 1

        return events
    
    def do( self, params ):
        '''Synchronous dynamics. We apply :meth:`dynamics` at each timestep
        and then check for completion using :meth:`at_equilibrium`.
        
        :param params: the parameters of the simulation
        :returns: a dict of experimental results'''

        # run the dynamics
        t = 0
        events = 0
        timestepEvents = 0
        while not self.at_equilibrium(t):
            # run a step
            nev = self.dynamics(t, params)
            if nev > 0:
                events = events + nev
                timestepEvents = timestepEvents + 1

            # advance to the next timestep
            t = t + 1

        # add some more metadata
        (self.metadata())[self.TIME] = t
        (self.metadata())[self.EVENTS] = events
        (self.metadata())[self.TIMESTEPS_WITH_EVENTS] = timestepEvents

        # report results
        rc = self.experimentalResults()
        return rc
