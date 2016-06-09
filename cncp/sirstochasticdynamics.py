# SIR simulator with stochastic (Gillespie)  dynamics
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
from .stochasticdynamics import GraphWithStochasticDynamics


class SIRStochasticDynamics(GraphWithStochasticDynamics):
    '''An SIR dynamics with stochastic simulation.'''

    # keys for node and edge data
    DYNAMICAL_STATE = 'sir'   # dynamical state of a node
    
    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    RECOVERED = 'R'
    
    def __init__( self, pInfect = 0.0, pRecover = 1.0, pInfected = 0.0, g = None ):
        '''Generate a graph with dynamics for the given parameters.
        
        pInfect: infection probability (defaults to 0.0)
        pRecover: probability of recovery (defaults to 1.0)
        pInfected: initial infection probability (defaults to 0.0)
        g: the graph to copy from (optional)'''
        GraphWithStochasticDynamics.__init__(self, g)

        # dynamics parameters
        self._pInfect = pInfect
        self._pRecover = pRecover
        self._pInfected = pInfected

        # list of infected nodes, the sites of all the dynamics
        self._infected = []
    
        # list of SI edges connecting a susceptible to an infected node
        self._si = []

    def before( self ):
        '''Seed the network with infected nodes, extract the initial set of
        SI nodes, and mark all edges as unoccupied by the dynamics.'''
        self._infected = []       # in case we re-run from a dirty intermediate state
        self._si = []
        
        # infect nodes
        for n in self.node.keys():
            if numpy.random.random() <= self._pInfected:
                self._infected.insert(0, n)
                self.node[n][self.DYNAMICAL_STATE] = self.INFECTED
            else:
                self.node[n][self.DYNAMICAL_STATE] = self.SUSCEPTIBLE
                
        # extract the initial set of SI edges
        for (n, m, data) in self.edges_iter(self._infected, data = True):
            self._si.insert(0, (n, m, data))
        
        # mark all edges as unoccupied
        for (n, m, data) in self.edges_iter(data = True):
            data[self.OCCUPIED] = False
            
    def at_equilibrium( self, t ):
        '''SIR dynamics is at equilibrium if there are no more infected nodes left
        in the network, no susceptible nodes adjacent to infected nodes, or if we've
        exceeded the default simulation length.
        
        t: the current time
        returns: True if the model has stopped'''
        if t >= 20000:
            return True
        else:
            return (len(self._infected) == 0)
        
    def infect( self, t ):
        '''Infect a node chosen at random from the SI edges.'''
        
        # choose an SI edge
        i = int(numpy.random.random() * len(self._si))
        (n, m, data) = self._si[i]
        
        # infect the susceptible end
        self._infected.insert(0, m)
        self.node[m][self.DYNAMICAL_STATE] = self.INFECTED
        
        # label the edge we traversed as occupied
        data[self.OCCUPIED] = True
        
        # remove all edges in the SI list from an infected node to this one
        self._si = [ (np, mp, data) for (np, mp, data) in self._si if m != mp ]
        
        # add all the edges incident on this node connected to susceptible nodes
        for (_, mp, datap) in self.edges_iter(m, data = True):
            if self.node[mp][self.DYNAMICAL_STATE] == self.SUSCEPTIBLE:
                self._si.insert(0, (m, mp, datap))

    def recover( self, t ):
        '''Cause a node to recover.'''
        
        # choose an infected node at random
        i = int(numpy.random.random() * len(self._infected))
        n = self._infected[i]
        
        # mark the node as recovered
        del self._infected[i]
        self.node[n][self.DYNAMICAL_STATE] = self.RECOVERED
        
        # remove all edges in the SI list incident on this node
        self._si = [ (np, m, e) for (np, m, e) in self._si if np != n ]
        
    def transitions( self, t ):
        '''Return the transition vector for the dynamics.
        
        t: time (ignored)
        returns: the transition vector'''
        
        # transitions are expressed as rates, whereas we're specified
        # in terms of probabilities, so we convert the latter to the former.
        return [ (len(self._si) * self._pInfect,        lambda t: self.infect(t)),
                 (len(self._infected) * self._pRecover, lambda t: self.recover(t)) ]
            
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
