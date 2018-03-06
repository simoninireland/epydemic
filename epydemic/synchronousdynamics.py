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
    for large systems.

    :param g: prototype network to run over (optional)'''

    # additional metadata
    TIMESTEPS_WITH_EVENTS = 'timesteps_with_events'  #: Metadata element holding the number timesteps that actually had events occur within them

    def __init__( self, g = None ):
        super(SynchronousDynamics, self).__init__(g)

    def do( self, params ):
        '''Synchronous dynamics.
        
        :param params: the parameters of the simulation
        :returns: a dict of experimental results'''
        
        # run the dynamics
        g = self.network()
        t = 0
        events = 0
        timestepEvents = 0
        while not self.at_equilibrium(t):
            # fire any events posted for at or before this time
            nev = self.runPendingEvents(t)
            
            # retrieve all the events, their loci, probabilities, and event functions
            dist = self.eventDistribution(t)

            # run through all the events in the distribution
            for (l, p, ef) in dist:
                if p > 0.0:
                    # run through every possible element on which this event may occur
                    for e in copy(l.elements()):
                        # test for occurrance of the event on this element
                        if numpy.random.random() <= p:
                            # yes, perform the event
                            ef(self, t, g, e)
                            
                            # update the event count
                            nev = nev + 1

            # add the events to the count
            events = events + nev
            if nev > 0:
                # we had events happen in this timestep
                timestepEvents = timestepEvents + 1

            # advance to the next timestep
            t = t + 1

        # run any events posted for before the maximum simulation time
        self.runPendingEvents(self._maxTime)

        # add some more metadata
        (self.metadata())[self.TIME] = t
        (self.metadata())[self.EVENTS] = events
        (self.metadata())[self.TIMESTEPS_WITH_EVENTS] = timestepEvents

        # report results
        rc = self.experimentalResults()
        return rc
