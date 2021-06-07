# Generating function interface
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
from typing import List, Callable, Union
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final
from networkx import Graph
from epydemic.gf import GF, DiscreteGF, ContinuousGF


def gf_series(f: Callable[[float], float]) -> GF:
    '''Create a generating function from the function that defines
    the complete series.

    :param f: the series function
    :returns: the generating function'''
    return ContinuousGF(f)

def gf_from_coefficients(cs: Union[List[float], Callable[[int], float]]) -> GF:
    '''Create a generating function from a list of coefficients. These
    may be provided either as a list of values or as a function that
    maps the term exponent to the coefficient. In the latter case the
    function must return a value for *all* terms.

    :param cs: the coefficients, as a list or a function
    :returns: a generating function'''
    return DiscreteGF(coefficients=cs)

def gf_from_network(g: Graph) -> GF:
    '''Create a generating function representing the actual distribution
    of degrees in the given network.

    :param g: the network:returns: a generating function'''
    return DiscreteGF(g=g)
