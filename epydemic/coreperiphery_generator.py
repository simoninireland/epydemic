# Core-periphery network generator
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

import sys
from typing import Any, Dict
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final
from networkx import (Graph,
                      fast_gnp_random_graph, convert_node_labels_to_integers,
                      compose, connected_components)
from epydemic import rng, NetworkGenerator


class CorePeripheryNetwork(NetworkGenerator):
    '''A generator of core-periphery networks as described by
    Hebert-Dufresne and Allard :cite:`PercolationSmearedPhaseTransition`.
    These consist of two ER networks of different sizes and internal
    edge densities, connected by edges with the density of the periphery
    (which is typically substantially less than that of the core).

    The resulting network is restricted to its largest connected component.

    :param params: experimental parameters
    :param limit: (optional) limit on number of networks that can be generated
    '''

    # Network parameters
    N_core: Final[str] = 'coreperiphery.N-core'         #: Experimental parameter holding the size of the core network.
    PHI_core: Final[str] = 'coreperiphery.phi-core'     #: Experimental parameter holding the edge probability of the core network.
    N_per: Final[str] = 'coreperiphery.N-periphery'     #: Experimental parameter holding the size of the peripheral network.
    PHI_per: Final[str] = 'coreperiphery.phi-periphery' #: Experimental parameter holding the edge probability of the peripheral network.

    # Node attributes
    ORIGIN: Final[str] = "origin"                       #: State variable holding a node's origin in the core (0) or periphery (1).

    @staticmethod
    def coreSubNetwork(g: Graph) -> Graph:
        '''Return the sub-network composing the core. This method
        will only work for networks created by this class, that have
        the :attr:`ORIGIN` property set correctly. An exception will
        be raised if the core can't be identified.

        :param g: the network
        :returns: the core sub-network'''
        try:
            ns = [n for n in g.nodes() if g.nodes[n][CorePeripheryNetwork.ORIGIN] == 0]
            return g.subgraph(ns)
        except KeyError:
            raise ValueError('Network does not have core-periphery structure marked')

    @staticmethod
    def peripherySubNetwork(g: Graph) -> Graph:
        '''Return the sub-network composing the periphery. This method
        will only work for networks created by this class, that have
        the :attr:`ORIGIN` property set correctly. An exception will
        be raised if the core can't be identified.

        :param g: the network
        :returns: the core sub-network'''
        try:
            ns = [n for n in g.nodes() if g.nodes[n][CorePeripheryNetwork.ORIGIN] == 1]
            return g.subgraph(ns)
        except KeyError:
            raise ValueError('Network does not have core-periphery structure marked')

    def topology(self) -> str:

        '''Return the topology marker string.

        :returns: the topology marker'''
        return 'ER-core-periphery'

    def _generate(self, params: Dict[str, Any]) -> Graph:
        '''Generate a core-periphery network.

        :param params: the experimental parameters
        :returns: the network'''

        # generate the core network
        N_core = params[self.N_core]
        phi_core = params[self.PHI_per]
        g_core = fast_gnp_random_graph(N_core, phi_core)

        # generate the periphery network
        N_per = params[self.N_per]
        phi_per = params[self.PHI_per]
        g_per = fast_gnp_random_graph(N_per, phi_per)

        # relabel the nodes into a single sequence
        g_core = convert_node_labels_to_integers(g_core, first_label=0)
        g_per = convert_node_labels_to_integers(g_per, first_label=N_core)

        # form both networks into a a single network, currently disconnected
        g = compose(g_core, g_per)

        # label all nodes with their origins
        for n in g_core.nodes():
            g.nodes[n][self.ORIGIN] = 0     # core nodes have origin == 0
        for m in g_per.nodes():
            g.nodes[m][self.ORIGIN] = 1     # periphery nodes have origin == 1

        # join the periphery to the core using the same density
        # as within the periphery itself
        for n in g_core.nodes():
            for m in g_per.nodes():
                if rng.random() <= phi_per:
                    g.add_edge(n, m)             # edges added to composed network

        # restrict to the LCC
        lcc = g.subgraph(max(connected_components(g), key=len)).copy()
        lcc = convert_node_labels_to_integers(lcc, first_label=0)

        return lcc
