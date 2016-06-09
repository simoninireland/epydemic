# SIR simulator with synchronous dynamics
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import networkx
import numpy
import time

from .networkwithdynamics import GraphWithDynamics
from .synchronousdynamics import GraphWithSynchronousDynamics


class SIRSynchronousDynamics(GraphWithSynchronousDynamics):
    '''A graph with a particular SIR dynamics. We use probabilities
    to express infection and recovery per timestep, and run the system
    using synchronous dynamics.'''
    
    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    RECOVERED = 'R'
        
    def __init__( self, pInfect = 0.0, pRecover = 1.0, pInfected = 0.0, g = None ):
        '''Generate a graph with SIR dynamics for the given parameters.
        
        pInfect: infection probability (defaults to 0.0)
        pRecover: probability of recovery (defaults to 1.0)
        pInfected: initial infection probability (defaults to 0.0)
        g: the graph to copy from (optional)'''
        GraphWithSynchronousDynamics.__init__(self, g)

        # dynamics parameters
        self._pInfect = pInfect
        self._pRecover = pRecover
        self._pInfected = pInfected

        # list of infected nodes, the sites of all the dynamics
        self._infected = []

    def before( self ):
        '''Seed the network with infected nodes, and mark all edges
        as unoccupied by the dynamics.'''
        self._infected = []       # in case we re-run from a dirty intermediate state
        
        # seed the network with infected nodes, making all the other susceptible
        for n in self.node.keys():
            if numpy.random.random() <= self._pInfected:
                self._infected.insert(0, n)
                self.node[n][self.DYNAMICAL_STATE] = self.INFECTED
            else:
                self.node[n][self.DYNAMICAL_STATE] = self.SUSCEPTIBLE
                
        # mark all edges as unoccupied
        for (n, m, data) in self.edges_iter(data = True):
            data[self.OCCUPIED] = False

    def _dynamics_step( self ):
        '''Optimised per-step dynamics that only runs the dynamics at infected
        nodes, since they're the only places where state changes originate. At the
        end of each timestep we re-build the infected node list.
        
        returns: the number of events that happened in this timestep'''
        events = 0
        
        # run model dynamics on infected nodes only
        for n in self._infected:
            events = events + self.model(n)
    
        # remove any nodes that are no longer infected from the infected list
        self._infected = [ n for n in self._infected if self.node[n][self.DYNAMICAL_STATE] == self.INFECTED ]
        
        return events
            
    def model( self, n ):
        '''Apply the SIR dynamics to node n. From the re-definition of dynamics_step()
        we already know this node is infected.

        n: the node
        returns: the number of changes made'''
        events = 0
        
        # infect susceptible neighbours with probability pInfect
        for (_, m, data) in self.edges_iter(n, data = True):
            if self.node[m][self.DYNAMICAL_STATE] is self.SUSCEPTIBLE:
                if numpy.random.random() <= self._pInfect:
                    events = events + 1
                    
                    # infect the node
                    self.node[m][self.DYNAMICAL_STATE] = self.INFECTED
                    self._infected.insert(0, m)
                        
                    # label the edge we traversed as occupied
                    data[self.OCCUPIED] = True
    
        # recover with probability pRecover
        if numpy.random.random() <= self._pRecover:
            # recover the node
            events = events + 1
            self.node[n][self.DYNAMICAL_STATE] = self.RECOVERED
                
        return events
            
    def at_equilibrium( self, t ):
        '''SIR dynamics is at equilibrium if there are no more infected nodes
        left in the network or if we've hit the default equilibrium conditions.
        
        returns: True if the model has stopped'''
        if (len(self._infected) == 0):
            return True
        else:
            return GraphWithSynchronousDynamics.at_equilibrium(self, t)
            
    def dynamics( self ):
        '''Returns statistics of outbreak sizes. This skeletonises the
        network, so it can't have any further dynamics run on it.
        
        returns: a dict of statistical properties'''
        
        # run the basic dynamics
        rc = self._dynamics()
        
        # compute the limits and means
        cs = sorted(networkx.connected_components(self.skeletonise()), key = len, reverse = True)
        max_outbreak_size = len(cs[0])
        max_outbreak_proportion = (max_outbreak_size + 0.0) / self.order()
        mean_outbreak_size = numpy.mean([ len(c) for c in cs ])
        
        # add parameters and metrics for this simulation run
        rc['pInfected' ] = self._pInfected,
        rc['pRecover'] = self._pRecover,
        rc['pInfect'] = self._pInfect,
        rc['N'] = self.order(),
        rc['mean_outbreak_size'] = mean_outbreak_size,
        rc['max_outbreak_size'] = max_outbreak_size,
        rc['max_outbreak_proportion'] = max_outbreak_proportion
        return rc
    
