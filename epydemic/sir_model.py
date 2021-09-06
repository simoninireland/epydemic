# SIR as a compartmented model
#
# Copyright (C) 2017--2021 Simon Dobson
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

import sys
from typing import Dict, Any
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final
from epydemic import CompartmentedModel


class SIR(CompartmentedModel):
    '''The Susceptible-Infected-Removed :term:`compartmented model of disease`.
    Susceptible nodes are infected by infected neighbours, and recover to
    removed.'''

    # Model parameters
    P_INFECTED : Final[str] = 'pInfected'  #: Parameter for probability of initially being infected.
    P_INFECT : Final[str] = 'pInfect'      #: Parameter for probability of infection on contact.
    P_REMOVE : Final[str] = 'pRemove'      #: Parameter for probability of removal (recovery).

    # Possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE : Final[str] = 'SIR.S'         #: Compartment for nodes susceptible to infection.
    INFECTED : Final[str] = 'SIR.I'            #: Compartment for nodes infected.
    REMOVED : Final[str] = 'SIR.R'             #: Compartment for nodes recovered/removed.

    # Locus containing the edges at which dynamics can occur
    SI : Final[str] = 'SIR.SI'                 #: Edge able to transmit infection.

    def __init__(self):
        super().__init__()

    def build(self, params: Dict[str, Any]):
        '''Build the SIR model.

        :param params: the model parameters'''
        super().build(params)

        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)

        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)
        self.trackNodesInCompartment(self.INFECTED)

        self.addEventPerElement(self.SI, pInfect, self.infect)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove)

    def infect(self, t: float, e: Any):
        '''Perform an infection event. This changes the compartment of
        the susceptible-end node to :attr:`INFECTED`. It also records the
        first occupation time for the edge transmiting the infection,
        and the first hitting time for the infected node.

        :param t: the simulation time
        :param e: the edge transmitting the infection, susceptible-infected'''
        (n, _) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t, firstOnly=True)
        self.markHit(n, t, firstOnly=True)

    def remove(self, t: float, n: Any):
        '''Perform a removal event. This changes the compartment of
        the node to :attr:`REMOVED`.

        :param t: the simulation time (unused)
        :param n: the node'''
        self.changeCompartment(n, self.REMOVED)
