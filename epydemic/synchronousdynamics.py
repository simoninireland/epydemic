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

    def dynamics( self, t, params ):
        '''Run one step of the discrete-time dynamics. This method must
        be overridden by sub-classes.

        :param t: the current simulation time
        :param params: the simulation parameters
        :returns: the number of events that happened in the timestep'''
        raise NotYetImplemented('dynamics()')
    
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
