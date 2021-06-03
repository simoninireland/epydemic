# Generating functions with a function for coefficients
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
from typing import Callable
from networkx import Graph
from epydemic.gf import GF


class FunctionGF(GF):
    '''A generating function whose coefficients are given by a function.
    The function must be total on the range :math:`[0, n]`.

    :param generator: a function that generates coefficients
    :param n: the largest term in the generating function
    '''

    def __init__(self, generator: Callable[[int], float], n: int):
        super().__init__()
        self._coefficients: Callable[[int], float] = generator
        self._maxTerm = n

    def getCoefficient(self, i: int) -> float:
        '''Return the i'th coefficient.

        :param i: the index
        :returns: the coefficient of x^i'''
        return self._coefficients(i)

    def evaluate(self, x: float) -> float:
        '''Evaluate the generating function.

        :param x: the argument
        :returns: the value of the generating function'''
        v = 0
        for i in range(self._maxTerm + 1):
            v += self[i] * x**i
        return v
