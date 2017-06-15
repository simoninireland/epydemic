# SIS simulator with synchronous dynamics
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


class SISSynchronousDynamics(SIRSynchronousDynamics):
    '''An SIS synchronous dynamics.'''
    
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
