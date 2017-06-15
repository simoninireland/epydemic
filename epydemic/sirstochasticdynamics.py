# SIR simulator with stochastic (Gillespie) dynamics
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


class SIRStochasticDynamics(StochasticDynamics):
    '''A stochastic SIR dynamics.'''

    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'    #: Node dynamical state marking node as susceptible to infection
    INFECTED = 'I'       #: Node dynamical state marking node as infected
    RECOVERED = 'R'      #: Node dynamical state marking node as recovered/removed
    
    def __init__( self, g = None ):
        '''Generate an SIR dynamics.
        
        :param g: the graph to run over (optional)'''
        super(SIRStochasticDynamics, self).__init__(g)

        # list of infected nodes, the sites of all the dynamics
        self._infected = []
    
        # list of SI edges connecting a susceptible to an infected node
        self._si = []

    def setUp( self, params ):
        '''Seed the network with infected nodes, extract the initial set of
        SI nodes, and mark all edges as unoccupied by the dynamics.

        :param params: the paemeters of the experiment'''

        # perform the default setup
        super(SIRStochasticDynamics, self).setUp(params)

        g = self.network()
        pInfected = params['pInfected']

        # in case we re-run from a dirty intermediate state
        self._infected = []       
        self._si = []
        
        # infect nodes
        for n in g.node.keys():
            if numpy.random.random() <= pInfected:
                self._infected.insert(0, n)
                g.node[n][self.DYNAMICAL_STATE] = self.INFECTED
            else:
                g.node[n][self.DYNAMICAL_STATE] = self.SUSCEPTIBLE
                
        # extract the initial set of SI edges
        for (n, m, data) in g.edges_iter(self._infected, data = True):
            if g.node[m][self.DYNAMICAL_STATE] == self.SUSCEPTIBLE:
                self._si.insert(0, (n, m, data))
        
        # mark all edges as unoccupied
        for (n, m, data) in g.edges_iter(data = True):
            data[self.OCCUPIED] = False
            
    def at_equilibrium( self, t ):
        '''SIR dynamics is at equilibrium if there are no more infected nodes left
        in the network, no susceptible nodes adjacent to infected nodes, or if we've
        met the default termination conditions.
        
        :param t: the current time
        :returns: True if the model has stopped'''
        if len(self._infected) == 0:
            return True
        else:
            if len(self._si) == 0:
                return True
            else:
                return super(SIRStochasticDynamics, self).at_equilibrium(t)
         
    def infect( self, t, params ):
        '''Infect a node chosen at random from the SI edges.

        :param t: the timestep
        :param params: the parameters of the experiment'''
        g = self.network()
        
        # choose an SI edge
        i = int(numpy.random.random() * (len(self._si) - 1))
        (n, m, data) = self._si[i]
        
        # infect the susceptible end
        self._infected.insert(0, m)
        g.node[m][self.DYNAMICAL_STATE] = self.INFECTED
        
        # label the edge we traversed as occupied
        data[self.OCCUPIED] = True
        
        # remove all edges in the SI list from an infected node to the
        # node we just infected
        self._si = [ (np, mp, data) for (np, mp, data) in self._si if mp != m ]
        
        # add all the edges incident on this node connected to susceptible nodes
        for (_, mp, datap) in g.edges_iter(m, data = True):
            if g.node[mp][self.DYNAMICAL_STATE] == self.SUSCEPTIBLE:
                self._si.insert(0, (m, mp, datap))

    def recover( self, t, params ):
        '''Cause a node to recover.

        :param t: the timestep
        :param params: the parameters of the experiment'''
        g = self.network()
        
        # choose an infected node at random
        i = int(numpy.random.random() * (len(self._infected) - 1))
        n = self._infected[i]
        
        # mark the node as recovered
        del self._infected[i]
        g.node[n][self.DYNAMICAL_STATE] = self.RECOVERED
        
        # remove all edges in the SI list incident on this node
        self._si = [ (np, m, datap) for (np, m, datap) in self._si if np != n ]
        
    def transitions( self, t, params ):
        '''Return the transition vector for the dynamics. This consists of
        two entries, for the infection and recovery events.
        
        :param t: time (ignored)
        :param params: the parameters of the simulation
        :returns: the transition vector'''
        
        # transitions are expressed as rates, whereas we're specified
        # in terms of probabilities, so we convert the latter to the former.
        return [ (len(self._si) * params['pInfect'],        lambda t: self.infect(t, params)),
                 (len(self._infected) * params['pRecover'], lambda t: self.recover(t, params)) ]
            
    def do( self, params ):
        '''Returns statistics of outbreak sizes. This skeletonises the
        network, so it can't have any further dynamics run on it.
        
        :param params: the parameters of the experiment
        :returns: a dict of statistical properties'''
        g = self.network()
        
        # run the basic dynamics
        rc = super(SIRStochasticDynamics, self).do(params)
        
        # compute the limits and means
        cs = sorted(networkx.connected_components(self.skeletonise()), key = len, reverse = True)
        max_outbreak_size = len(cs[0])
        max_outbreak_proportion = (max_outbreak_size + 0.0) / g.order()
        mean_outbreak_size = numpy.mean([ len(c) for c in cs ])
        
        # add metrics for this simulation run
        rc['mean_outbreak_size'] = mean_outbreak_size,
        rc['max_outbreak_size'] = max_outbreak_size,
        rc['max_outbreak_proportion'] = max_outbreak_proportion
        return rc
