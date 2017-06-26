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

    # the model parameters
    P_INFECTED = 'pInfected'  #: Parameter for a not initially being infected
    P_INFECT = 'pInfect'      #: Parameter for infection on contact
    P_REMOVE = 'pRecover'     #: Parameter for recovery
    
    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'    #: Compartment for nodes susceptible to infection
    INFECTED = 'I'       #: Compartment for nodes infected
    REMOVED = 'R'        #: Compartment for nodes recovered/removed    

    # the edges at which dynamics can occur
    SI = 'SI'            #: Edge able to transmit infection

    def __init__( self ):
        super(SIR, self).__init__()

    def build( self, params ):
        '''Build the SIR model.

        :param params: the model parameters'''
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRecover = params[self.P_REMOVE]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)

        self.addLocus(self.SUSCEPTIBLE, self.INFECTED, name = self.SI)
        self.addLocus(self.INFECTED)

        self.addEvent(self.INFECTED, pRecover, lambda t, l, g, e: self.remove(l, g, e))
        self.addEvent(self.SI, pInfect, lambda t, l, g, e: self.infect(l, g, e))

    def infect( self, l, g, (n, m) ):
        self.changeCompartment(g, n, self.INFECTED)
        self.markOccupied(g, (n, m))

    def remove( self, l, g, n ):
        self.changeCompartment(g, n, self.REMOVED)
    
                
   
