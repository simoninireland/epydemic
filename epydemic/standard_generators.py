# Standard generators
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

from epydemic import NetworkGenerator
from networkx import Graph, fast_gnp_random_graph, barabasi_albert_graph
import sys
if sys.version_info >= (3, 8):
    from typing import Any, Dict, Optional, Final
else:
    # backport compatibility with older typing
    from typing import Any, Dict, Optional
    from typing_extensions import Final

class FixedNetwork(NetworkGenerator):
    '''A network generator that always returns a copy of the same network.

    :param g: the prototype network
    :param limit: (optional) maximum number of identical instances to generate'''

    def __init__(self, g: Graph, limit: Optional[int] = None):
        super().__init__(limit=limit)
        self._graphPrototype: Graph = g

    def topology(self) -> str:
        '''Return the topoology flag for this generator.

        :returns: the topology marker ("Arbitrary")'''
        return 'Arbitrary'

    def _generate(self, params: Dict[str, Any]) -> Graph:
        '''Return a copy of the prototype network.

        :param params: experimental parameters (ignored)
        :returns: a network instance'''
        return self._graphPrototype.copy()


class ERNetwork(NetworkGenerator):
    '''Generate Erdos-Renyi (ER) networks from a given order (:attr:`N`) and one of an edge occupation
    probability (:attr:`PHI`) or a mean degree (:attr:`KMEAN`). These parameters are taken from the
    experimental parameters.

    An ER network has nodes with Poisson-distributed independent degrees. The construction process
    can be thought of as taking a set of :math:`N` nodes and then adding an edge between every pair
    with independent probability :math:`\\phi`. This process gives a discrete normal (Poisson) distribution
    of the node degrees with mean degree :math:`\\langle k \\rangle = N \\phi`. The node degrees will
    be uncorrelated.

    The actual construction of ER networks uses the `networkx.fast_gnp_random_graph()` function.

    :param params: (optional) experiment parameters
    :param limit: (optional) meximum  number of instances to generate'''

    # Experimental parameters
    N: Final[str] = 'N'         #: Experimental parameter for the size (order) of the network.
    PHI: Final[str] = 'phi'     #: Experimental parameter for the occupation probability of edges.
    KMEAN: Final[str] = 'kmean' #: Experimental parameter for the mean degree of the network.

    def __init__(self, params: Dict[str, Any] = None, limit: Optional[int] = None):
        super().__init__(params, limit)

    def topology(self) -> str:
        '''Return the topoology flag for this generator.

        :returns: the topology marker ("ER")'''
        return 'ER'

    def _generate(self, params: Dict[str, Any]) -> Graph:
        '''Generate an ER network from an order (represented by the parameter :attr:`N`)
        and one of an edge occupation probability (:attr:`PHI`) or mean degree (:attr:`KMEAN`).

        :param params: experimental parameters
        :returns: the ER network'''

        # extract the parameters
        N = params[self.N]
        if self.PHI in params:
            phi = params[self.PHI]
        elif self.KMEAN in params:
            kmean = params[self.KMEAN]
            phi = (kmean + 0.0) / N
        else:
            raise AttributeError('Need one of occupation probability or mean degree')

        # build the network
        g = fast_gnp_random_graph(N, phi)
        return g


class BANetwork(NetworkGenerator):
    '''Generate Barabasi-Albert (BA) networks from a given order (:attr:`N`) and rate of attachment
    (:attr:`M`) taken from the experimental parameters.

    A BA network has node degrees distributed according to a powerlaw distribution. The construction process
    can be thought of as taking an initial set of :math:`M` nodes and then adding additional nodes
    one at a time, adding adges between the new node and :math:`M` other nodes chosen at random. This
    continues until the network has :math:`N` nodes. This process favours attachment to nodes that are
    in the network early, leading to "hubs" with very high degree. The node degrees will
    be uncorrelated.

    The actual construction of BA networks uses the `networkx.barabasi_albert_graph()` function.

    :param params: (optional) experiment parameters
    :param limit: (optional) meximum  number of instances to generate'''

    # Experimental parameters
    N: Final[str] = 'N'         #: Experimental parameter for the size (order) of the network.
    M: Final[str] = 'MperNode'  #: Experimental parameter for the number of edges added per node.

    def __init__(self, params: Dict[str, Any] = None, limit: Optional[int] = None):
        super().__init__(params, limit)

    def topology(self) -> str:
        '''Return the topoology flag for this generator.

        :returns: the topology marker ("BA")'''
        return 'BA'

    def _generate(self, params: Dict[str, Any]) -> Graph:
        '''Generate a BA network from an order (represented by the parameter :attr:`N`)
        and attachment rate (:attr:`M`).

        :param params: experimental parameters
        :returns: the BA network'''

        # extract the parameters
        N = params[self.N]
        M = params[self.M]

        # build the network
        g = barabasi_albert_graph(N, M)
        return g
