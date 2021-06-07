# Continuous generating functions
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
import numpy
from mpmath import factorial
from epydemic.gf import GF


class ContinuousGF(GF):
    '''A continuous generating function.

    These generating functions are constructed from power series provided
    by functions, optionally differentiated some number of times.

    Note that computing the coefficients of a continuous generating
    function uses Cauchy's method, so the function needs to be able to
    handle complex numbers in its arguments. Typically this means
    using functions from ``numpy`` or ``cmath``, rather than simply
    from ``math``. These calculations also lead to large intermediate
    results, so functions from ``mpmath`` can also be useful. This
    approach is however able to extract coefficients of high degree.

    :param f: the function defining the power series
    :param order: (optional) the order of derivative represented (defaults to 0)
    '''

    def __init__(self, f: Callable[[float], float], order: int = 0):
        super().__init__()
        self._f = f
        self._order = order

        # make sure the function vectorises
        if not isinstance(self._f, numpy.vectorize):
            self._f = numpy.vectorize(self._f)

    def _differentiate(self, z: float, n: int = 1, r: float = 1.0, dx: float = 1e-2) -> complex:
        '''Compute the n'th derivative of f at z using
        a Cauchy contour integral of radius r.

        :param z: point at which to find the derivative
        :param n: order of derivative (defaults to 1)
        :param r: radius of contour (defaults to 1.0)
        :param dx: step size (defaults to 1e-2)'''

        # increase the requested order of derivative by whatever we have intrinsically
        n += self._order

        # simple evaluation if we've got no derivatives to compute
        if n == 0:
            return self._f(z)

        # perform the Cauchy contour integral
        x = r * numpy.exp(2j * numpy.pi * numpy.arange(0, 1, dx))
        return factorial(n) * numpy.mean(self._f(z + x) / x**n)

    def getCoefficient(self, i: int) -> float:
        '''Return the i'th coefficient.

        :param i: the index
        :returns: the coefficient of x^i'''
        return float((self._differentiate(0.0, i) / factorial(i)).real)

    def evaluate(self, x: float) -> float:
        '''Evaluate the generating function.

        :param x: the argument
        :returns: the value of the generating function'''
        return self._differentiate(x, 0).real

    def derivative(self, order: int = 1) -> GF:
        '''Return the requested derivative. This creates a new
        generating function over the same underlying series.

        :param order: (optional) order of derivative (defaults to 1)
        :returns: a generating function'''
        return ContinuousGF(self._f, self._order + order)
