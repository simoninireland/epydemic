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

from typing import Callable
from epydemic.gf import GF


class FunctionGF(GF):
    '''A generating function whose coefficients are given by a function.
    The function must be total on the range :math:`[0, n]`.

    :param generator: a function that generates coefficients
    :param n: (optional) the largest term in the generating function (defaults to 300)
    '''

    def __init__(self, generator: Callable[[int], float], n: int = None):
        super().__init__()
        self._coefficients: Callable[[int], float] = generator
        self._maxTerm = 300 if n is None else 300

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

    def _differentiate(self, f: Callable[[int], float], order: int) -> Callable[[int], float]:
        '''Return a coefficient function representing the n'th
        order derivative of the function given.

        :param f: the coefficient function
        :param order: the order or derivative
        :returns: the derivative coefficient function'''

        def df(i: int) -> float:
            # low-order terms fall away
            if i < order:
                return 0

            # high-order terms are transformed
            m = f(i + order)
            for j in range(1, order + 1):
                m *= (i + j)
            return m

        return df

    def derivative(self, order: int = 1) -> GF:
        '''Return the requested derivative. This creates a new
        generating function over the same underlying coefficients,
        shifted and scaled.

        :param order: (optional) order of derivative (defaults to 1)
        :returns: a generating function'''
        df = self._differentiate(self._coefficients, order)
        return FunctionGF(df, self._maxTerm)
