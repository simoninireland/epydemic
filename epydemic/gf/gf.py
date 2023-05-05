# Base class generating functions
#
# Copyright (C) 2021--2023 Simon Dobson
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

from functools import lru_cache


class GF:
    '''Base class for generating functions.

    A generating function represents a formal power series. In network
    science they are usually, but not exclusively, used to represent
    probability distributions, for example of node degrees. Computing
    with the generating functions then provides a way of working with
    entire distributions, from which the individual probabilities can
    later be extracted.

    Generating functions can be treated in three ways:

    1. As arrays of coefficients that can be extracted
    2. As functions that can be called
    3. As functions to be differentiated one or more times

    In the first approach, use the array interface, for example:

    .. code-block:: python

       p_2 = gf[2]

    In the second, use the calling interface, for example:

    .. code-block:: python

       p_0 = gf(0)

    In the third, use the :meth:`dx` method, for example:

    .. code-block:: python

       gf_prime_prime = gf.dx(2)

    All three cases are memoised to improve performance, relying on
    the fact that the generating function class is immutable.

    '''

    def __init__(self):
        pass


    # ---------- Subclass API ----------

    def getCoefficient(self, i: int) -> float:
        '''Return the i'th coefficient, that is the coefficient of the
        term in :math:`x^i`.

        This method should be overridden by sub-classes.

        :param i: the index
        :returns: the i'th coefficient'''
        raise NotImplementedError('GF.getCoefficient() must be overridden by sub-classes')

    def evaluate(self, x: float) -> float:
        '''Evaluate the generating function at x. This is always a number
        on the range :math:`[0, 1]`.

        This method must be overridden by sub-classes.

        :param x: the argument
        :returns: the value of the generating function'''
        raise NotImplementedError('GF.evaluate() must be overridden by sub-classes')

    def derivative(self, order: int = 1) -> 'GF':
        '''Return a new generating function representing the derivative
        (to any order, the first by default).

        This method should be overridden by sub-classes.

        :param order: (optional) the order of derivative (defaults to 1)
        :returns: the deerivative of the generating function'''
        raise NotImplementedError('GF.derivative() must be overridden by sub-classes')

    def __mul__(self, n):
        '''Multiply the generating function by a constant.

        :param n: the number
        :returns: the new generating function'''
        raise NotImplementedError('GF.__mul_() must be overridden by sub-classes')

    def __truediv__(self, n):
        '''Divide the generating function by a constant.
        This is implemented by inverting the constant and multiplying.

        :param n: the number
        :returns: the new generating function'''
        return self * (1 / n)


    # ---------- Client API ----------

    @lru_cache(maxsize=None)
    def __getitem__(self, i: int) -> float:
        '''Return the i'th coefficient. This uses :meth:`getCoefficient`
        but with an array-like interface.

        :param i: the index
        :returns: the i'th coefficient'''
        return self.getCoefficient(i)

    @lru_cache(maxsize=None)
    def __call__(self, x: float) -> float:
        '''Evaluate the generating function. This uses :meth:`evaluate`
        but with a call interface.

        :param x: the argument
        :returns: the value of the generating function'''
        return self.evaluate(x)

    @lru_cache(maxsize=None)
    def dx(self, order: int = 1):
        '''Return the derivative of the generating function to the desired order.

        :param order: (optional) the order of derivative (defaults to 1)
        :returns: the derivative of the generating function'''
        return self.derivative(order)
