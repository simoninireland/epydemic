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
<<<<<<< HEAD
from epydemic.gf import GF
from networkx import Graph


class DiscreteGF(GF):
=======
from networkx import Graph
from epydemic.gf import FunctionGF


class DiscreteGF(FunctionGF):
    '''A discrete generating function.

    This is a generating function represented as an explicit list of
    coefficients. These can created either by providing a list of real
    numbers or by providing a network from which the coefficients are
    extracted as the fraction of nodes with the given degree.

    :param g: (optional) a network
    :param coefficients: (optional) a list of coefficients

    '''

    def __init__(self, g: Graph = None, coefficients: List[float] = None):

        # check we have one of the approaches we need
        ps = len([p for p in [g, coefficients] if p is not None])
        if ps == 0:
            raise ValueError('Must provide one of a network or a list of coefficients')
        elif ps > 1:
            raise ValueError('Ambbiguous parameters')

        if g is not None:
            # extract the coefficients from the degree distribution
            coefficients = self._coefficientsFromNetwork(g)

        # we have a list of coefficients, wrap a function around them
        generator = self._coefficientsWrapper(coefficients)

        # create the generating function
        super().__init__(generator, len(coefficients) + 1)

    def _coefficientsFromNetwork(self, g: Graph) -> List[float]:
        '''Compute the degree histogram.

        :param g: the network
        :returns: the fractional occurrence of each degree'''
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
        cs = [hist[i] / N for i in range(maxk + 1)]
        return cs

    def _coefficientsWrapper(self, cs: List[float]):
        '''Wrap a list of coefficients in a function.

        :param cs: the coeffcients
        :returns: a function from term to coefficient'''

        def wrap(i: int) -> float:
            return cs[i] if i < len(cs) else 0

        return wrap
