# Discrete generating functions created from actual networks
#
# Copyright (C) 2021 Simon Dobson
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

from collections import Counter
from typing import List
from epydemic.gf import GF
from networkx import Graph


class DiscreteGF(GF):
    '''A discrete generating function.

    This is a generating function represented as an explicit list of
    coefficients. These can created either by providing a list of real
    numbers or by providing a network from which the coefficients are
    extracted as the fraction of nodes with the given degree.

    If the generating function is intended to be a probability generating
    function then the coefficients must sum to 1, and also the value
    of the generating function at 1 must be 1.

    :param network: (optional) a network
    :param coefficients: (optional) a list of coefficients

    '''

    def __init__(self, network: Graph = None, coefficients: List[float] = None):
        super().__init__()

        self._coefficients: List[float] = []
        if coefficients is None:
            if network is not None:
                # a network, extract its degree histogram
                self._setCoefficientsFromNetwork(network)
            else:
                # empty GF, do nothing
                pass
        else:
            if network is None:
                # list of coefficients
                self._coefficients = coefficients.copy()
            else:
                # both options provided
                raise ValueError('Only one of network and coefficients can be provided')

    def _setCoefficientsFromNetwork(self, g: Graph):
        '''Compute the degree histogram and use it to set the
        coefficients of the generating function.

        :param g: the network'''
        N = g.order()
        seq = sorted([d for (_, d) in g.degree()])
        hist = Counter(seq)
        maxk = max(seq)
        self._collections = []
        for i in range(maxk + 1):
            self._coefficients.append(hist[i] / N)

    def getCoefficient(self, i:int) -> float:
        '''Return the i'th coefficient.

        :param i: the index
        :returns: the coefficient of x^i'''
        if i >= len(self._coefficients):
            return 0
        else:
            return self._coefficients[i]

    def evaluate(self, x: float) -> float:
        '''Evaluate the generating function.

        :param x: the argument
        :returns: the value of the generating function'''
        v = 0
        for i in range(len(self._coefficients)):
            v += self[i] * x**i
        return v
