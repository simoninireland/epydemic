# SIR as a compartmented model
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

import random


class SIR(CompartmentedModel):

    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'    #: Compartment for nodes susceptible to infection
    INFECTED = 'I'       #: Compartment for nodes infected
    REMOVED = 'R'        #: Compartment for nodes recovered/removed    

    # the edges at which dynamics can occur
    SI = 'SI'            #: Edge able to transmit infection

    def __init__( self ):
        super(SIR, self).__init__()

    def build( self, g, params ):
        pInfected = params['pInfected']
        pInfect = params['pInfect']
        pRecover = params['pRecover']

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)

        self.addLocus(self.SUSCEPTIBLE, self.INFECTED, name = self.SI)
        self.addLocus(self.INFECTED)

        self.addEvent(self.INFECTED, pRecover, lambda t, g: self.remove(g))
        self.addEvent(self.SI, pInfect, lambda t, g: self.infect(g))

        # initialise nodes according to the initial compartment probability distribution
        dist = self.initialCompartmentDistribution()
        self.checkDistributionIsNormalised(dist)
        for (n, data) in g.nodes_iter(data = True):
            # label node with its compartment
            c = self.drawFromDistribution(dist)
            data[self.COMPARTMENT] = c

            # store node in locus
            self.addToLocus(c, n)

        # initialise edge loci
        for (n, m, data) in g.edges_iter(data = True):
            # mark edge as unocupied by the dynamics
            data[self.OCCUPIED] = False
            
            # store edge in locus
            if (g.node[n][self.COMPARTMENT] == self.SUSCEPTIBLE) and (g.node[m][self.COMPARTMENT] == self.INFECTED):
                self.addToLocus(self.SI, (n, m))
            else:
                if (g.node[n][self.COMPARTMENT] == self.INFECTED) and (g.node[m][self.COMPARTMENT] == self.SUSCEPTIBLE):
                    self.addToLocus(self.SI, (m, n))

        #print 'I {i}'.format(i = len(self._loci[self.INFECTED]))
        #print 'SI {si}'.format(si = len(self._loci[self.SI]))
                                    
    def infect( self, g ):
        #print 'infect'
        
        # choose an SI edge at random
        (n, m) = self.drawFromLocus(self.SI)
        print 'infect {n}-{m}'.format(n = n, m = m)

        # mark the edge as occupied
        data = g.get_edge_data(n, m)
        data[self.OCCUPIED] = True
        
        # remove any edges in SI depending on n in being SUSCEPTIBLE
        es = set([ (n, m) for (_, m) in g.edges_iter(n) if (n, m) in self._loci[self.SI] ])
        print 'losing SI edges {es}'.format(es = es)
        self.removeFromLocus(self.SI, es)

        # move compartment
        print 'infect {n}'.format(n = n)
        g.node[n][self.COMPARTMENT] = self.INFECTED

        # add to INFECTED locus
        self.addToLocus(self.INFECTED, n)

        # add any edges that are now SI
        es = set([ (m, n) for (_, m) in g.edges_iter(n) if g.node[m][self.COMPARTMENT] == self.SUSCEPTIBLE ])
        print 'new SI edges {es}'.format(es = es)
        self.addToLocus(self.SI, es)

    def remove( self, g ):
        #print 'remove'
        
        # choose an INFECTED node edge at random
        n = self.drawFromLocus(self.INFECTED)
        print n
        
        # remove any edges in SI depending on n in being INFECTED
        es = set([ (m, n) for (_, m) in g.edges_iter(n) if g.node[m][self.COMPARTMENT] == self.SUSCEPTIBLE ])
        print 'losing SI edges {es}'.format(es = es)
        self.removeFromLocus(self.SI, es)

        # move compartment
        print 'remove {n}'.format(n = n)
        g.node[n][self.COMPARTMENT] = self.REMOVED

                
                
   
