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
import networkx
import math
import numpy
import collections


class FixedNetwork(NetworkGenerator):
    '''A network generator that always returns a copy of the same network.

    :param g: the prototype network
    :param limit: (optional) maximum number of identical instances to generate'''

    def __init__(self, g, limit=None):
        super(FixedNetwork, self).__init__(limit=limit)
        self._graphPrototype = g
    
    def _generate(self, params):
        '''Return a copy of the prototype network.

        :param params: experimental parameters (ignored)
        :returns: a network instance'''
        return self._graphPrototype.copy()


class ERNetwork(NetworkGenerator):
    '''Generate ER networks from a given order (:attr:`N`) and one of an edge occupation
    probability (:attr:`PHI`) or a mean degree (:attr:`KMEAN`). These parameters are taken from the
    experimental parameters.

    An ER network has nodes with Poisson-distributed independent degrees. The construction process
    can be thought of as taking a set of :math:`N` nodes and then adding an edge between every pair
    with independent probability :math:`\phi`. This process gives a discrete normal (Poisson) distribution
    of the node degrees with mean degree :math:`\\langle k \\rangle = N \phi`. The node degrees will
    be uncorrelated.

    The actual construction of ER networks uses the `networkx.fast_gnp_random_graph()` function.

    :param params: (optional) experiment parameters
    :param limit: (optional) meximum  number of instances to generate'''

    # Experimental parameters
    N = 'epydemic.generators.ERNetwork.N'         #: Experimental parameter for the size (order) of the network
    PHI = 'epydemic.generators.ERNetwork.PHI'     #: Experimental parameter for the occupation probability of edges
    KMEAN = 'epydemic.generators.ERNetwork.KMEAN' #: Experimental parameter for the mean degree of the network

    def __init__(self, params=None, limit=None):
        super(ERNetwork, self).__init__(params, limit)

    def _generate( self, params ):
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
        g = networkx.fast_gnp_random_graph(N, phi)
        return g
