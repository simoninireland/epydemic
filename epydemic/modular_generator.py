# Modular ER network generator
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
                      set_node_attributes, compose, connected_components)
from epydemic import rng, NetworkGenerator


class ModularNetwork(NetworkGenerator):
    '''A generator of modular ER networks as described by
    Hebert-Dufresne and Allard :cite:`PercolationSmearedPhaseTransition`.
    These consist of several ER networks, a "core" and several "satellites",
    having different sizes and edge densities, with each satellite linked
    to the core by a single edge.

    :param params: experimental parameters
    :param limit: (optional) limit on number of networks that can be generated
    '''

    # Network parameters
    N_core: Final[str] = 'modular.centre.N-core'       #: Experimental parameter holding the size of the core network.
    PHI_core: Final[str] = 'modular.centre.phi-core'   #: Experimental parameter holding the edge probability of the core network.
    SATELLITES: Final[str] = 'modular.satellites'      #: Experimental parameter holding the number of satellite networks.
    N_sat: Final[str] = 'modular.satellite.N-sat'      #: Experimental parameter holding the size of the satellite networks.
    PHI_sat: Final[str] = 'modular.satellite.phi-sat'  #: Experimental parameter holding the edge probability of the satellite networks.

    # Node attributes
    ORIGIN: Final[str] = "origin"                      #: State variable holding a node's network of origin (0 being the core, other indices being the satellites).
    CENTRE_LINK: Final[str] = "centre-link"            #: State variable that is True for nodes that are the endpoints of links from a satellite to the core.


    def topology(self) -> str:
        '''Return the topology marker string.

        :returns: the topology marker'''
        return 'ER-modular'

    def _generate(self, params):
        '''Generate a modular ER network.

        :param params: the experimental parameters
        :returns: the network'''

        # create the centre network
        N_centre = params[self.N_core]
        phi_centre = params[self.PHI_core]
        g_centre = fast_gnp_random_graph(N_centre, phi_centre)
        g_centre = g_centre.subgraph(max(connected_components(g_centre), key=len)).copy()
        g_centre = convert_node_labels_to_integers(g_centre, first_label=0)
        set_node_attributes(g_centre, name=self.ORIGIN, values=0)   # centre has origin == 0
        g = g_centre.copy()

        # generate the satellite networks
        satellites = params[self.SATELLITES]
        N_sat = params[self.N_sat]
        phi_sat = params[self.PHI_sat]
        g_sats = []
        l = N_centre
        for i in range(satellites):
            g_sat = fast_gnp_random_graph(N_sat, phi_sat)
            g_sat = g_sat.subgraph(max(connected_components(g_sat), key=len)).copy()
            g_sat = convert_node_labels_to_integers(g_sat, first_label=l)
            l += N_sat
            set_node_attributes(g_sat, name=self.ORIGIN, values=i + 1)  # satellites have origin > 0
            g = compose(g, g_sat)
            g_sats.append(g_sat)

        # join the satellites to the centre with a single link
        # between random nodes
        set_node_attributes(g, name=self.CENTRE_LINK, values=False)
        ns_centre = list(g_centre.nodes())
        for i in range(satellites):
            # choose a random node in the centre
            m = rng.choice(ns_centre)

            # choose a random node from the satellite
            ns_sat = list(g_sats[i].nodes())
            n = rng.choice(ns_sat)

            # mark the nodes as linked
            g.nodes[n][self.CENTRE_LINK] = True
            g.nodes[m][self.CENTRE_LINK] = True

            # add the edge
            g.add_edge(n, m)

        return g
