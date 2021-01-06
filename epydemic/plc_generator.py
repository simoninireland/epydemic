# A generator for powerlaw-with-cutoff networks
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

from epydemic import NetworkGenerator
from networkx import Graph, configuration_model
from math import exp
from mpmath import polylog
import numpy
import sys
if sys.version_info >= (3, 8):
    from typing import Any, Dict, Optional, Callable, Final
else:
    # backport compatibility with older typing
    from typing import Any, Dict, Optional, Callable
    from typing_extensions import Final


class PLCNetwork(NetworkGenerator):
    '''A generator for networks with a powerlaw-with-cutoff degree distribution.

    PLC networks are commonly used to represent the basic structure of human contact
    networks, where we want to cutoff the degree to stop it becoming "too high" to
    be credible: :ref:`Newman <New02>` (and other works) use this topology extensively.
    It is characterised by two parameters, the exponent of the power law and the
    cutoff maximum degree after which the probability of finding nodes with larger degrees
    falls off exponentially. 

    :param params: (optional) experimental parameters
    :param limit: (optional) maximum number of independent networks to generate'''

    # Experimental parameters
    N : Final[str] = 'epydemic.generators.PLCNetwork.N'                 #: Experimental parameter for the order of the network.
    EXPONENT : Final[str] = 'epydemic.generators.PLCNetwork.exponent'   #: Experimental parameter for the exponent of the distribution.
    CUTOFF : Final[str] = 'epydemic.generators.PLCNetwork.cutoff'       #: Experimental parameter for the cutoff of the distribution.

    def __init__(self, params : Dict[str, Any] =None, limit : Optional[int] =None):
        super(PLCNetwork, self).__init__(params, limit)

    def _makePowerlawWithCutoff(self, alpha : float, kappa : float) -> Callable[[int], float]:
        '''Create a model function for a powerlaw distribution with exponential cutoff.

        :param alpha: the exponent of the distribution
        :param kappa: the degree cutoff
        :returns: a model function'''
        C = polylog(alpha, exp(-1.0 / kappa))
        def p( k : int ) -> float:
            return (pow((k + 0.0), -alpha) * exp(-(k + 0.0) / kappa)) / C
        return p

    def _generateFrom(self, N : int, p : Callable[[int], float], maxdeg : int =100):
        '''Generate a random graph with degree distribution described
        by a model function.

        :param N: number of numbers to generate
        :param p: model function
        :param maxdeg: maximum node degree we'll consider (defaults to 100)
        :returns: a network with the given degree distribution'''
        rng = numpy.random.default_rng()
        ns = []
        t = 0
        for i in range(N):
            while True:
                # draw a random degree
                k = rng.integers(1, maxdeg)
            
                # do we include a node with this degree?
                if rng.random() < p(k):
                    # yes, add it to the sequence; otherwise, draw again
                    ns.append(k)
                    t += k
                    break

        # the final sequence of degrees has to sum to an even
        # number, as each edge has two endpoints
        # if the sequence is odd, remove an element and draw
        # another from the distribution, repeating until the
        # overall sequence is even
        while t % 2 != 0:
            # pick a node at random
            i = rng.integers(0, len(ns) - 1)

            # remove it from the sequence and from the total
            t -= ns[i]
            del ns[i]
            
            # choose a new node to replace the one we removed
            while True:
                # draw a new degree from the distribution
                k = rng.integers(1, maxdeg)
            
                # do we include a node with this degree?
                if rng.random() < p(k):
                    # yes, add it to the sequence; otherwise, draw again
                    ns.append(k)
                    t += k
                    break

        # populate the network using the configuration
        # model with the given degree distribution
        g = configuration_model(ns, create_using=Graph())
        return g

    def _generate(self, params : Dict[str, Any]) -> Graph:
        '''Generate the human contact network.

        :param params: the experimental parameters
        :returns: a network'''
        N = params[self.N]
        alpha = params[self.EXPONENT]
        kappa = params[self.CUTOFF]
        return self._generateFrom(N, self._makePowerlawWithCutoff(alpha, kappa))

