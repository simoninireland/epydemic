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
        for n in g.nodes_iter():
            # label node with its compartment
            c = self.drawFromDistribution(dist)
            self.moveCompartment(g, n, c)

            # store node in locus
            self.addToLocus(c, n)

        # initialise edge loci
        for (n, m) in g.edges_iter():
            # mark edge as unocupied by the dynamics
            self.markUnoccupied(g, n, m)
            
            # store edge in locus
            self.addEdgeToLocus(g, n, m, self.SI)

    def infect( self, g ):
        # choose an SI edge at random
        (n, m) = self.drawFromLocus(self.SI)

        # mark the edge as occupied
        self.markOccupied(g, n, m)
        
        # remove any edges in SI depending on n being SUSCEPTIBLE
        es = set([ (n, m) for (_, m) in g.edges_iter(n) if self.isInLocus(g, (n, m), self.SI) ])
        self.removeFromLocus(self.SI, es)

        # move compartment
        self.moveCompartment(g, n, self.INFECTED)

        # add to INFECTED locus
        self.addToLocus(self.INFECTED, n)

        # add any edges that are now SI
        es = set([ (m, n) for (_, m) in g.edges_iter(n) if self.isInCompartment(g, m, self.SUSCEPTIBLE) ])
        self.addToLocus(self.SI, es)

    def remove( self, g ):
        # choose an INFECTED node edge at random
        n = self.drawFromLocus(self.INFECTED)
        
        # remove any edges in SI depending on n in being INFECTED
        es = set([ (m, n) for (_, m) in g.edges_iter(n) if g.node[m][self.COMPARTMENT] == self.SUSCEPTIBLE ])
        self.removeFromLocus(self.SI, es)

        # move compartment
        self.moveCompartment(g, n, self.REMOVED)

                
                
   
