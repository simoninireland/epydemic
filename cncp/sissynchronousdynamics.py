# SIS simulator with synchronous dynamics
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp
import epyc
import networkx
import numpy


class SISSynchronousDynamics(cncp.SIRSynchronousDynamics):
    '''An SIR synchronous dynamics.'''
    
    def __init__( self, g = None ):
        '''Generate an SIS dynamics over an (optional) prototype network.
        
        :param g: the graph to run over (optional)'''
        super(SISSynchronousDynamics, self).__init__(g)

        # list of infected nodes, the sites of all the dynamics
        self._infected = []

    def model( self, n, params ):
        '''Apply the SIS dynamics to node n. Nodes "recover" back to the
        susceptible state.

        :param params: the parameters of thje simulation
        :param n: the node
        :returns: the number of changes made'''
        g = self.network()
        pInfect = params['pInfect']
        pRecover = params['pRecover']
        events = 0
        
        # infect susceptible neighbours with probability pInfect
        for (_, m, data) in g.edges_iter(n, data = True):
            if g.node[m][self.DYNAMICAL_STATE] == self.SUSCEPTIBLE:
                # we've got a susceptible neighbour, do we infect them?
                if numpy.random.random() <= pInfect:
                    # yes we do!
                    events = events + 1
                    
                    # infect the node
                    g.node[m][self.DYNAMICAL_STATE] = self.INFECTED
                    self._infected.insert(0, m)
                        
                    # label the edge we traversed as occupied
                    data[self.OCCUPIED] = True
    
        # recover with probability pRecover
        if numpy.random.random() <= pRecover:
            # recover the node
            events = events + 1
            g.node[n][self.DYNAMICAL_STATE] = self.SUSCEPTIBLE   # note that this potentially allows 
                                                                 # re-infection in this timestep
     
        return events
