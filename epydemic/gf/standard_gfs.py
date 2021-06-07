# Standard generating functions used in network science
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

import sys
from math import pow
from cmath import exp
from mpmath import polylog
from scipy.special import zeta
from epydemic.gf import GF, gf_from_series


def gf_er(N: int, kmean: float = None, phi: float = None) -> GF:
    '''Return the generating function for the Poisson degree distribution of
    an ER network of N nodes with the given mean degree or occupation
    probbability.

    :param N: the number of nodes in the network
    :param kmean: (optional) the mean degree
    :param phi: (optional) the occupation probability
    :returns: the generating function'''

    # check we have exactly one of kmean or phi
    ps = len([p for p in [kmean, phi] if p is not None])
    if ps != 1:
        raise ValueError('Must provide either a mean degree or an occupation probability')

    # get the mean degree if it wasn't provided
    if kmean is None:
        kmean = N * phi

    # return the generating function
    return gf_from_series(lambda x: exp(kmean * (x - 1)))

def gf_ba(exponent: float) -> GF:
    '''Return the generating function of the powerlaw
    degree distribution with the given exponent.

    :param exponent: the exponent of the distribution
    :returns: the generating function'''
    return gf_from_series(lambda x: polylog(exponent, x) / zeta(exponent, 1))

def gf_plc(exponent: float, cutoff: float) -> GF:
    '''Return the generating function of the powerlaw-with-cutoff
    degree distribution given its exponent and cutoff.

    :param exponent: the exponent of the distribution
    :param cutoff: the cutoff
    :returns: the generating function'''
    return gf_from_series(lambda x: polylog(exponent, x * exp(-1 / cutoff)) / polylog(exponent, exp(-1 / cutoff)))
