# Synchronous dynamics base class
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp

import networkx
import time


class SynchronousDynamics(cncp.Dynamics):
    '''A dynamics that runs synchronously in discrete time, applying local
    rules to each node in the network.'''
        
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given network.
        
        g: network to run over (optional)'''
        Dynamics.__init__(self, g)
        
    def model( self, n ):
        '''The dynamics function that's run over the network. This
        is a placeholder to be re-defined by sub-classes.
        
        n: the node being simulated'''
        raise NotYetImplementedError('model()')

    def _dynamics_step( self ):
        '''Run a single step of the model over the network.
        
        returns: the number of dynamic events that happened in this timestep'''
        g = self.network()
        events = 0
        for i in g.node.keys():
            events = events + self.model(i)
        return events

    def _dynamics( self ):
        '''Synchronous dynamics. We apply _dynamics_step() at each timestep
        and then check for completion using at_equilibrium().
        
        returns: a dict of simulation properties'''
        rc = dict()

        self.before()
        t = 0
        events = 0
        eventDist = dict()
        timestepEvents = 0
        while True:
            # run a step
            nev = self._dynamics_step()
            if nev > 0:
                events = events + nev
                timestepEvents = timestepEvents + 1
                eventDist[t] = nev
        
            # test for termination
            if self.at_equilibrium(t):
                break
            
            t = t + 1
        self.after()
        
        # return the simulation-level results
        rc['timesteps'] = t
        rc['events'] = events
        rc['timesteps_with_events'] = timestepEvents
        rc['node_types'] = self.populations()
        return rc

