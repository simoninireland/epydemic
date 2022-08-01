# A version of SIR where infectivity can vary per-edge
#
# Copyright (C) 2017--2022 Simon Dobson
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

from copy import copy
from typing import Dict, Any, Iterator
from epydemic import Process, CompartmentedModel, SIR, rng, Element, EventDistribution


class SingletonLocus:
    '''A locus containing a single element. This class supports only
    the essential functions of a locus, on the assumption that it'll
    only be used to construct event distributions.'''

    def __init__(self, p: Process, e: Element):
        self._process = p
        self._value = e

    def __len__(self) -> int:
        '''Length is always 1.

        :returns: 1'''
        return 1

    def draw(self) -> Element:
        '''Draw the only value.

        :returns: the value'''
        return self._value

    def process(self) -> Process:
        '''Return the process the locus is attached to.

        :returns: the process'''
        return self._process

    def __iter__(self) -> Iterator[Element]:
        '''Iterate over the one element.

        :returns: an iterator'''
        return iter([self._value])


class SIR_VariableInfection(SIR):
    '''A version of the SIR :term:`compartmented model of disease` where each
    edge can have a different infectivity. This is the basic machinery for
    supporting models with different populations of individuals, different
    environments, or different levels of contact.'''

    # Edge attribute for infectivity
    INFECTIVITY: str = None   #: State variable holding an edge's infectivity.


    def __init__(self):
        super().__init__()

        # state variables
        self.INFECTIVITY = self.stateVariable('infectivity')

    def build(self, params: Dict[str, Any]):
        '''Build the model. This adds a tracker for SI edges, but
        with no associated stochastic event.

        :param params: the simulation parameters'''
        CompartmentedModel.build(self, params)             # skip the base SIR.build()

        pInfected = params[self.P_INFECTED]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)

        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)
        self.trackNodesInCompartment(self.INFECTED)

        self.addEventPerElement(self.INFECTED, pRemove, self.remove, name=self.REMOVED)

    def setUp(self, params: Dict[str, Any]):
        '''Set up compartments and infectivites. Initial compartments are
        saet according to the usual approach for SIR using the parameter
        :attr:`SIR.P_INFECTED`. Per-edge infectivities are set using
        a call to :meth:`initialInfectivities`.

        :param params: the simulation parameters'''
        super().setUp(params)

        # set up the edge infectivities
        self.initialInfectivities()

    def initialInfectivities(self):
        '''Assign an infectivity to an edge. The default takes infectivities
        uniformly on the range :math:`[0.0, 1.0]`. Sub-classes may override this
        to provide different distributions.'''
        g = self.network()
        for (_, _, data) in g.edges(data=True):
            i = rng.random()
            data[self.INFECTIVITY] = i

    def perElementEventDistribution(self, t: float) -> EventDistribution:
        '''Construct the event distribution from the contents of the SI
        locus, combining each edge with its infection probability.

        :param t: the simulation time
        :returns: an event rate distribution'''

        # get the original distribution
        dist = copy(super().perElementEventDistribution(t))

        # add the infectivities on SI edges
        g = self.network()
        for e in self.locus(self.SI):
            pr = g.edges[e][self.INFECTIVITY]
            dist.extend([(SingletonLocus(self, e), pr, self.infect, self.INFECTED)])
        return dist
