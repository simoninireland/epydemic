# Opinion dynamics
#
# Copyright (C) 2021 Liberty Askew
# Integrated into main codebase by Simon Dobson
#
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published byf
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
from networkx import Graph
from typing import Dict, Any, List
if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final
from epydemic import CompartmentedModel, Node, Element, Locus, CompartmentedLocus, CompartmentedEdgeLocus


class MultiCompartmentedEdgeLocus(CompartmentedEdgeLocus):
    '''A compartmented locus that allows multiple compartments at one end
    of its edges. The left edge always has one compartment; the right
    edge can be one of a number. This is useful for linking one
    compartment to one or more others -- at a cost of being slightly
    slower than :class:`CompartmentedEdgeLocus`.

    :param name: the locus name
    :param l: the compartment on the left
    :param rs: the compartments on the right

    '''

    def __init__(self, name: str, l: str, rs: List[str]):
        super(CompartmentedLocus, self).__init__(name)
        self._left = l
        self._rights = set(rs)

    def compartments(self) -> List[str]:
        '''Return the compartments of the node endpoints we monitor.

        :returns: the compartments'''
        return list(self._rights.union(set(self._left)))

    def matches(self, g: Graph, n: Node, m: Node) -> int:
        '''Test whether the given edge has the correct compartment endpoints for
        this locus. Unlike :class:`CompartmentedEdgeLocus` we
        match one compartment on the left to one of several on
        the right

        The method returns 1 if the edge has the correct compartments in
        the orientation (n, m), -1 if it has the correct compartments in
        orientation (m, n), and 0 otherwise.

        :param g: the network
        :param n: the first node
        :param m: the second node
        :returns: match status -1, 0, or 1

        '''
        p = self.process()
        cn = p.getCompartment(n)
        cm = p.getCompartment(m)
        if (cn == self._left) and (cm in self._rights):
            return 1
        elif (cn in self._rights) and (cm == self._left):
            return -1
        else:
            return 0


class Opinion(CompartmentedModel):
    """Model for opinion spreading dynamics.

    This model is based on the work of Moreno *et alia*
    :cite:`RumourSpreadingComplexNetworks`, in which a single rumour
    is spread using an epidemic-like process, with compartments
    consisting of those ignorant of the rumour (:attr:`IGNORANT`),
    those who have heard the rumour and can spread it
    (:attr:`SPREADER`), and those who have heard the rumour and now do
    not believe it (or at least do not spread it (:attr:`STIFLER`).
    The difference between this process and :class:`SIR` is that
    "spreaders" become "stiflers" at a rate proportional to their
    contact with stiflers *and* spreaders.
    """

    # Experimental parameters
    P_AFFECTED: Final[float] = 'epydemic.opinion.pAffected'  #: Parameter for probability of initially being affected at start.
    P_AFFECT: Final[float] = 'epydemic.opinion.pAffect'      #: Parameter for probability of affect on contact.
    P_STIFLE: Final[float] = 'epydemic.opinion.pStifle'      #: Parameter for probability of becoming stifler on contact.

    # Compartments
    IGNORANT: Final[str] = 'epydemic.opinion.G'              #: Compartment for nodes ignorant of the rumour.
    SPREADER: Final[str] = 'epydemic.opinion.P'              #: Compartment for nodes spreading the rumour.
    STIFLER: Final[str] = 'epydemic.opinion.T'               #: Compartment for nodes now stifling the rumour.
    GP: Final[str] = 'epydemic.opinion.GP'                   #: Compartment for edges able to transmit the rumour.
    PPT: Final[str] = 'epydemic.opinion.PPT'                 #: Compartment for edges able to stifle the rumour.

    def __init__(self):
        super().__init__()

    def build(self, params: Dict[str, Any]):
        """
        Build the opinion model.

        :param params: the experimental parameters
        """
        super().build(params)

        pAffected = params[self.P_AFFECTED]
        pAffect = params[self.P_AFFECT]
        pStifle = params[self.P_STIFLE]

        self.addCompartment(self.IGNORANT, 1 - float(pAffected))
        self.addCompartment(self.SPREADER, pAffected)
        self.addCompartment(self.STIFLER, 0.0)

        self.trackNodesInCompartment(self.IGNORANT)
        self.trackNodesInCompartment(self.SPREADER)
        self.trackNodesInCompartment(self.STIFLER)
        self.trackEdgesBetweenCompartments(self.IGNORANT, self.SPREADER, name=self.GP)
        self.trackEdgesBetweenMultipleCompartments(self.SPREADER, [self.SPREADER, self.STIFLER], name=self.PPT)

        self.addEventPerElement(self.GP, pAffect, self.affect)
        self.addEventPerElement(self.PPT, pStifle, self.stifle)

    def trackEdgesBetweenMultipleCompartments(self, l: str, rs: List[str], name: str) -> Locus:
        """
        Add a locus to track edges with endpoint nodes in the given compartments.

        :param l: the compartment of the left node
        :param rs: the compartments of the right node
        :param name: (optional) the name of the locus (defaults to a combination of the two compartment names)
        :returns: the locus used to track the nodes
        """
        locus = MultiCompartmentedEdgeLocus(name, l, rs)
        return self.addLocus(name, locus)

    def atEquilibrium(self, t: float) -> bool:
        """The process is at equilibrium if there are no more GP or
        PPT edges remaining.

        :param t: the simulation time
        :returns: True if the process is at equilibrium"""
        return (len(self.locus(self.GP)) == 0 and len(self.locus(self.PPT)) == 0) or super().atEquilibrium(t)

    def affect(self, t: float, e: Element):
        """Performs affect event. Changes the compartment of the ignorant-end
        node to :attr:`SPREADER`.

        :param t: the simulation time
        :param e: the edge transmitting the infection, ignorant -> spreader

        """
        (n, _) = e
        self.changeCompartment(n, self.SPREADER)

    def stifle(self, t: float, e: Element):
        """Performs a stifle event. This changes the compartment of a
        :attr:`SPREADER` node to :attr:`STIFLER`.

        :param t: the simulation time (unused)
        :param e: the edge, spreader -> (spreader or stifler)

        """
        (n, _) = e
        self.changeCompartment(n, self.STIFLER)
