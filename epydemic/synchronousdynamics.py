# Synchronous dynamics base class
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

from epydemic import Dynamics

import epyc
import networkx
import numpy
from copy import copy

class SynchronousDynamics(Dynamics):
    '''A dynamics that runs synchronously in discrete time, applying local
    rules to each node in the network. These are simple to understand and
    simple to code for many cases, but can be statistically inexact and slow
    for large systems.

    :pafram p: the network process to run
    :param g: prototype network to run over (optional)'''

    # additional metadata
    TIMESTEPS_WITH_EVENTS = 'timesteps_with_events'  #: Metadata element holding the number timesteps that actually had events occur within them

    def __init__( self, p, g = None ):
        super(SynchronousDynamics, self).__init__(p, g)

    def do( self, params ):
        '''Execute the process under synchronous dynamics.
        
        :param params: the parameters of the simulation
        :returns: a dict of experimental results'''
        
        # run the dynamics
        proc = self.process()
        t = 0
        events = 0
        timestepEvents = 0
        while not proc.atEquilibrium(t):
            # fire any events posted for at or before this time
            nev = self.runPendingEvents(t)
            
            # run through all the events in the distribution
            dist = proc.perElementEventDistribution(t)
            for (l, p, ef) in dist:
                if (len(l) > 0) and (p > 0.0):
                    # run through every possible element on which this event may occur
                    for e in copy(l.elements()):
                        # test for occurrance of the event on this element
                        if numpy.random.random() <= p:
                            # yes, perform the event
                            ef(t, e)
                            nev = nev + 1

            # run through all the fixed-rate events for this timestep
            dist = proc.fixedRateEventDistribution(t)
            for (l, p, ef) in dist:
                if (len(l) > 0) and (p > 0.0):
                    if numpy.random.random() <= p:
                        # yes, perform the event on an element drawn at random
                        e = l.draw()
                        ef(t, e)
                        nev = nev + 1

            # add the events to the count
            events = events + nev
            if nev > 0:
                # we had events happen in this timestep
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
