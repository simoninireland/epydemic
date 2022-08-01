# SEIR as a compartmented model
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


class SEIR(CompartmentedModel):
    '''The Susceptible-Exposed-Infected-Removed :term:`compartmented model of disease`.
    A susceptible node becomes exposed when infected by either an exposed or an infected
    neighbour. Exposed nodes become infected (symptomatic) to infected and then recover
    to removed.

    In contrast to the more familiar :class:`SIR` model, SEIR has two
    compartments that can pass infection. The utility of the model from two aspects:
    exploring what fraction of the contract tree arises from infected individuals
    *versus* exposed individuals, capturing the significance of asymptomatic infection;
    and allowing countermeasures to be applied to symptomatic individuals whose presence
    could be more easily detected than those who are exposed by asymptomatic.

    The SEIR model in `epydemic` is very flexible, allowing different infection probabilities
    for susceptible-exposed or susceptible-infected interactions. The initial seed population
    is placed into :attr:`EXPOSED`, rather than into :attr:`INFECTED` as happens
    for :class:`SIR`.'''

    # Model parameters
    P_EXPOSED: Final[str] = 'epydemic.seir.pExposed'                  #: Parameter for probability of initially being exposed.
    P_INFECT_ASYMPTOMATIC: Final[str] = 'epydemic.seir.pInfectAsymp'  #: Parameter for probability of infection on contact with an exposed individual
    P_INFECT_SYMPTOMATIC: Final[str] = 'epydemic.seir.pInfect'        #: Parameter for probability of infection on contact with a symptomatic individual.
    P_SYMPTOMS: Final[str] = 'epydemic.seir.pSymptoms'                #: Parameter for probability of becoming symptomatic after exposure.
    P_REMOVE: Final[str] = 'epydemic.seir.pRemove'                    #: Parameter for probability of removal (recovery).

    # Possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE: Final[str] = 'epydemic.seir.S'     #: Compartment for nodes susceptible to infection.
    EXPOSED: Final[str] = 'epydemic.seir.E'         #: Compartment/event name for nodes exposed and infectious.
    INFECTED: Final[str] = 'epydemic.seir.I'        #: Compartment for nodes symptomatic and infectious.
    REMOVED: Final[str] = 'epydemic.seir.R'         #: Compartment/event name for nodes recovered/removed.

    # Event names
    INFECTED_SYMPTOMATIC: Final[str] = 'epydemic.seir.IS' #: Event name for infections from symptomatic (:attr:`INFECTED`) individuals)
    INFECTED_ASYMPTOMATIC: Final[str] = 'epydemic.seir.IA' #: Event name for infections from asymptomatic (:attr:`EXPOSED`) individuals)

    # Loci containing the edges at which dynamics can occur
    SE: Final[str] = 'SEIR.SE'                #: Edge able to transmit infection from an exposed individual.
    SI: Final[str] = 'SEIR.SI'                #: Edge able to transmit infection from an infected individual.

    def __init__(self):
        super().__init__()

    def build(self, params: Dict[str, Any]):
        '''Build the SEIR model.

        :param params: the model parameters'''
        super().build(params)

        pExposed = params[self.P_EXPOSED]
        pInfectA = params[self.P_INFECT_ASYMPTOMATIC]
        pInfect = params[self.P_INFECT_SYMPTOMATIC]
        pSymptoms = params[self.P_SYMPTOMS]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.SUSCEPTIBLE, 1.0 - pExposed)
        self.addCompartment(self.EXPOSED, pExposed)
        self.addCompartment(self.INFECTED, 0.0)
        self.addCompartment(self.REMOVED, 0.0)

        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.EXPOSED, name=self.SE)
        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)
        self.trackNodesInCompartment(self.EXPOSED)
        self.trackNodesInCompartment(self.INFECTED)

        self.addEventPerElement(self.SE, pInfectA, self.infectAsymptomatic, name=self.INFECTED_ASYMPTOMATIC)
        self.addEventPerElement(self.SI, pInfect, self.infect, name=self.INFECTED_SYMPTOMATIC)
        self.addEventPerElement(self.EXPOSED, pSymptoms, self.symptoms, name=self.INFECTED)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove, name=self.REMOVED)

    def infectAsymptomatic(self, t: float, e: Edge):
        '''Perform an infection event when an :attr:`EXPOSED` individual infects
        a neighbouring :attr:`SUSCEPTIBLE`, rendering them :attr:`EXPOSED` in turn.
        The default calls :meth:`infect` so that infections by way of exposed or
        symptomatic individuals are treated in the same way. Sub-classes can override this
        to, for example, record that the infection was passed asymptomatically.

        :param t: the simulation time
        :param e: the edge transmitting the infection'''
        self.infect(t, e)

    def infect(self, t: float, e: Edge):
        '''Perform an infection event when an :attr:`INFECTED` individual infects
        a neighbouring :attr:`SUSCEPTIBLE`, rendering them :attr:`EXPOSED` in turn.

        :param t: the simulation time
        :param e: the edge transmitting the infection'''
        (n, _) = e
        self.changeCompartment(n, self.EXPOSED)
        self.markOccupied(e, t, firstOnly=True)
        self.markHit(n, t, firstOnly=True)

    def symptoms(self, t: float, n: Node):
        '''Perform the symptoms-developing event. This changes the compartment of
        the node to :attr:`INFECTED`.

        :param t: the simulation time
        :param n: the node'''
        self.changeCompartment(n, self.INFECTED)

    def remove(self, t: float, n: Node):
        '''Perform a removal event. This changes the compartment of
        the node to :attr:`REMOVED`.

        :param t: the simulation time
        :param n: the node'''
        self.changeCompartment(n, self.REMOVED)
