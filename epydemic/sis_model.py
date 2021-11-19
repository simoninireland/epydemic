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

import sys
from typing import Dict, Any
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final
from epydemic import CompartmentedModel, Node, Edge


class SIS(CompartmentedModel):
    '''The Susceptible-Infected-Susceptible :term:`compartmented model of
    disease`.  Susceptible nodes are infected by infected neighbours,
    and recover back to the susceptible state (which allows future
    re-infection, unlike for :class:`SIR`.

    Because SIS allows re-infection, it's useful to store additional
    information as part of the simulation. By default the process
    records the numbber of times a node has been infected (using the
    :attr:`SIS.N_INFECTED` node attribute) and the number of time the
    infection has been passed over an edge (using the
    :attr:`SIS.N_OCCUPIED` edge attribute). These are not returned in
    results in any way, but can be used by sub-classes wanting to
    analyse the behaviour of the epidemic.

    '''

    # Node and edge attributes
    N_INFECTED: Final[int] = 'nInfected'               #: Node attribute storing the number of times the node was infected.
    N_OCCUPIED: Final[int] = 'nOccupied'               #: Edge attribute storing the number of times the edge was occupied (i.e., used to transmit the infection).

    # Model  parameters
    P_INFECTED: Final[str] = 'epydemic.sis.pInfected'  #: Parameter for probability of initially being infected.
    P_INFECT: Final[str] = 'epydemic.sis.pInfect'      #: Parameter for probability of infection on contact.
    P_RECOVER: Final[str] = 'epydemic.sis.pRecover'    #: Parameter for probability of recovery (returning to susceptible).

    # Possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE: Final[str] = 'epydemic.sis.S'         #: Compartment for nodes susceptible to infection.
    INFECTED: Final[str] = 'epydemic.sis.I'            #: Compartment/event name for nodes infected.

    # Event names
    RECOVERED: Final[str] = 'epydemic.sis.R'       #: Event name for nodes that become susceptible again.

    # Locus containing the edges at which dynamics can occur
    SI: Final[str] = 'epydemic.sis.SI'                 #: Edge able to transmit infection.

    def __init__(self):
        super().__init__()

    def build(self, params: Dict[str, Any]):
        '''Build the SIS model.

        :param params: the model parameters'''
        super().build(params)

        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRecover = params[self.P_RECOVER]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)

        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)
        self.trackNodesInCompartment(self.INFECTED)

        self.addEventPerElement(self.INFECTED, pRecover, self.recover, name=self.RECOVERED)
        self.addEventPerElement(self.SI, pInfect, self.infect, name=self.INFECTED)

    def countOccupied(self, e: Edge) -> int:
        '''Update the count of the number of times an edge has passed
        the infection.

        :param e: the edge
        :returns: the number of infection events passing over this edge'''
        g = self.network()
        (n, m) = e
        data = g.get_edge_data(n, m)
        if self.N_INFECTED in data.keys():
            data[self.N_OCCUPIED] += 1
        else:
            data[self.N_OCCUPIED] = 1
        return data[self.N_OCCUPIED]

    def countInfected(self, n: Node) -> int:
        '''Update the count of the number of times a node has become infected.

        :param n: the node
        :returns: the number of infection events at this node'''
        g = self.network()
        data = g.nodes[n]
        if self.N_INFECTED in data.keys():
            data[self.N_INFECTED] += 1
        else:
            data[self.N_INFECTED] = 1
        return data[self.N_INFECTED]

    def infect(self, t: float, e: Edge):
        '''Perform an infection event. This changes the compartment of
        the susceptible-end node to :attr:`INFECTED`. It also marks the edge
        traversed as occupied, records the hitting time for the node
        if it is the first, and the number of times a node has been infected,

        :param t: the simulation time
        :param e: the edge transmitting the infection, susceptible-infected'''
        (n, _) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)
        self.markHit(n, t, firstOnly=True)    # record only the first hitting time

    def recover(self, t: float, n: Node):
        '''Perform a recovery event. This changes the compartment of
        the node back to :attr:`SUSCEPTIBLE`, allowing re-infection.

        :param t: the simulation time (unused)
        :param n: the node'''
        self.changeCompartment(n, self.SUSCEPTIBLE)
