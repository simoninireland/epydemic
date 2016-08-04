# Synchronous dynamics base class
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp
import epyc
import networkx


class SynchronousDynamics(cncp.Dynamics):
    '''A dynamics that runs synchronously in discrete time, applying local
    rules to each node in the network.'''
        
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given network.
        
        g: prototype network to run over (optional)'''
        super(SynchronousDynamics, self).__init__(g)
        
    def model( self, n, params ):
        '''The dynamics function that's run over the network. This
        is a placeholder to be re-defined by sub-classes.
        
        params: the parameters of the simulation
        n: the node being simulated'''
        raise NotYetImplementedError('model()')

    def dynamics( self, params ):
        '''Run a single step of the model over the network.
        
        params: the parameters of the simulation
        returns: the number of dynamic events that happened in this timestep'''
        g = self.network()
        events = 0
        for n in g.node.keys():
            events = events + self.model(n, params)
        return events

    def do( self, params ):
        '''Synchronous dynamics. We apply dynamics() at each timestep
        and then check for completion using at_equilibrium().
        
        params: the parameters of the simulation
        returns: a dict of simulation properties'''
        rc = dict()

        t = 0
        events = 0
        timestepEvents = 0
        while not self.at_equilibrium(t):
            # run a step
            nev = self.dynamics(params)
            if nev > 0:
                events = events + nev
                timestepEvents = timestepEvents + 1
            t = t + 1
        
        # return the simulation-level results
        rc['timesteps'] = t
        rc['events'] = events
        rc['timesteps_with_events'] = timestepEvents
        rc['node_types'] = self.populations()
        return rc

