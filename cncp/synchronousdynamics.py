# Synchronous dynamics base class
#
# Copyright (C) 2014-2017 Simon Dobson
# 
# This file is part of Complex networks, complex processes (CNCP).
#
# CNCP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CNCP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CNCP. If not, see <http://www.gnu.org/licenses/gpl.html>.

import cncp
import epyc
import networkx


class SynchronousDynamics(cncp.Dynamics):
    '''A dynamics that runs synchronously in discrete time, applying local
    rules to each node in the network. These are simple to understand and
    simple to code for many cases, but can be statistically inexact and slow
    for large systems.'''
        
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given prototype
        network.
        
        :param g: prototype network to run over (optional)'''
        super(SynchronousDynamics, self).__init__(g)
        
    def model( self, n, params ):
        '''The dynamics function that's run over the network. This
        is a placeholder to be re-defined by sub-classes.
        
        :param params: the parameters of the simulation
        :param n: the node being simulated'''
        raise NotYetImplementedError('model()')

    def dynamics( self, t, params ):
        '''Run a single step of the model over the network.
        
        :param t: the current timestep
        :param params: the parameters of the simulation
        :returns: the number of dynamic events that happened in this timestep'''
        g = self.network()
        events = 0
        for n in g.node.keys():
            events = events + self.model(n, params)
        return events

    def do( self, params ):
        '''Synchronous dynamics. We apply dynamics() at each timestep
        and then check for completion using at_equilibrium().
        
        :param params: the parameters of the simulation
        :returns: a dict of simulation properties'''
        rc = dict()

        t = 0
        events = 0
        timestepEvents = 0
        while not self.at_equilibrium(t):
            t = t + 1

            # run a step
            nev = self.dynamics(t, params)
            if nev > 0:
                events = events + nev
                timestepEvents = timestepEvents + 1
        
        # return the simulation-level results
        rc['timesteps'] = t
        rc['events'] = events
        rc['timesteps_with_events'] = timestepEvents
        rc['node_types'] = self.populations()
        return rc

