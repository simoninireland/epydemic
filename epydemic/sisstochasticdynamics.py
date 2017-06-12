# SIS simulator with stochastic (Gillespie) dynamics
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
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.#

from epydemic import *
import epyc
import networkx
import numpy


class SISStochasticDynamics(SIRStochasticDynamics):
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
 
