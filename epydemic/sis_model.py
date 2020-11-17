# SIS as a compartmented model
#
# Copyright (C) 2017--2020 Simon Dobson
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

from epydemic import CompartmentedModel
from typing import Dict, Any, Final


class SIS(CompartmentedModel):
    '''The Susceptible-Infected-Susceptible :term:`compartmented model of disease`.
    Susceptible nodes are infected by infected neighbours, and recover back
    to the susceptible state (which allows future re-infection, unlike for
    :class:`SIR`.'''

    # Model  parameters
    P_INFECTED : Final[str] = 'epydemic.SIS.pInfected'  #: Parameter for probability of initially being infected.
    P_INFECT : Final[str] = 'epydemic.SIS.pInfect'      #: Parameter for probability of infection on contact.
    P_RECOVER : Final[str] = 'epydemic.SIS.pRecover'    #: Parameter for probability of recovery (returning to susceptible).

    # Possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE : Final[str] = 'epydemic.SIS.S'         #: Compartment for nodes susceptible to infection.
    INFECTED : Final[str] = 'epydemic.SIS.I'            #: Compartment for nodes infected.

    # Locus containing the edges at which dynamics can occur
    SI : Final[str] = 'epydemic.SIS.SI'                 #: Edge able to transmit infection.

    def __init__(self):
        super(SIS, self).__init__()

    def build(self, params :Dict[str, Any]):
        '''Build the SIS model.

        :param params: the model parameters'''
        super(SIS, self).build(params)
        
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRecover = params[self.P_RECOVER]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)

        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name = self.SI)
        self.trackNodesInCompartment(self.INFECTED)

        self.addEventPerElement(self.INFECTED, pRecover, self.recover)
        self.addEventPerElement(self.SI, pInfect, self.infect)

    def infect(self, t : float, e : Any):
        '''Perform an infection event. This changes the compartment of
        the susceptible-end node to :attr:`INFECTED`. It also marks the edge
        traversed as occupied.

        :param t: the simulation time
        :param e: the edge transmitting the infection, susceptible-infected'''
        (n, _) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)

    def recover(self, t : float, n : Any):
        '''Perform a recovery event. This changes the compartment of
        the node back to :attr:`SUSCEPTIBLE`, allowing re-infection.

        :param t: the simulation time (unused)
        :param n: the node'''
        self.changeCompartment(n, self.SUSCEPTIBLE)
    
                
   
