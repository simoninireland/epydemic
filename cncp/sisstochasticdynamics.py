# SIS simulator with stochastic (Gillespie) dynamics
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


class SISStochasticDynamics(cncp.SIRStochasticDynamics):
    '''An SIS stochastic dynamics. This is very like the SIR
    dynamics but recovered nodes become susceptible again, modelling
    recurrent disease where infection does not confer immunity. SIS also
    allows endemic diseases to form, existing indefinitely in the network
    at low levels.'''

    def __init__( self, g = None ):
        '''Generate an SIS dynamics with an optional prototype network.
        
        :param g: the graph to run over (optional)'''
        super(SISStochasticDynamics, self).__init__(g)

    def recover( self, t, params ):
        '''Cause a node to recover back to the susceptible state.

        :param t: the timestep
        :param params: the parameters of the experiment'''
        g = self.network()
        
        # choose an infected node at random
        i = int(numpy.random.random() * (len(self._infected) - 1))
        n = self._infected[i]
        
        # mark the node as recovered
        del self._infected[i]
        g.node[n][self.DYNAMICAL_STATE] = self.SUSCEPTIBLE
        
        # remove all edges in the SI list incident on this node
        self._si = [ (np, m, e) for (np, m, e) in self._si if np != n ]
 
