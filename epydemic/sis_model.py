# SIS as a compartmented model
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

class SIS(CompartmentedModel):
    '''The Susceptible-Infected-Susceptible :term:`compartmented model of disease`.
    Susceptible nodes are infected by infected neighbours, and recover back
    to the susceptible state (which allows future re-infection, unlike for
    :class:`SIR`.'''

    # the model parameters
    P_INFECTED = 'pInfected'  #: Parameter for probability of initially being infected.
    P_INFECT = 'pInfect'      #: Parameter for probability of infection on contact.
    P_REMOVE = 'pRemove'      #: Parameter for probability of removal (recovery).
    
    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'         #: Compartment for nodes susceptible to infection.
    INFECTED = 'I'            #: Compartment for nodes infected.

    # the edges at which dynamics can occur
    SI = 'SI'                 #: Edge able to transmit infection.

    def __init__( self ):
        super(SIS, self).__init__()

    def build( self, params ):
        '''Build the SIS model.

        :param params: the model parameters'''
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)

        self.addLocus(self.SUSCEPTIBLE, self.INFECTED, name = self.SI)
        self.addLocus(self.INFECTED)

        self.addEvent(self.INFECTED, pRemove, lambda d, t, g, e: self.remove(d, t, g, e))
        self.addEvent(self.SI, pInfect, lambda d, t, g, e: self.infect(d, t, g, e))

    def infect(self, dyn, t, g, n, m):
        '''Perform an infection event. This changes the compartment of
        the susceptible-end node to :attr:`INFECTED`. It also marks the edge
        traversed as occupied.

        :param dyn: the dynamics
        :param t: the simulation time (unused)
        :param g: the network
        :param e: the edge transmitting the infection, susceptible-infected'''
        self.changeCompartment(g, n, self.INFECTED)
        self.markOccupied(g, (n, m))

    def remove( self, dyn, t, g, n ):
        '''Perform a removal event. This changes the compartment of
        the node back to :attr:`SUSCEPTIBLE`, allowing re-infection.

        :param dyn: the dynamics
        :param t: the simulation time (unused)
        :param g: the network
        :param n: the node'''
        self.changeCompartment(g, n, self.SUSCEPTIBLE)
    
                
   
