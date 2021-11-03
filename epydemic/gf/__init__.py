# Initialisation for epydemic generating functions library
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

# base class
from .gf import GF

# classes of generating function
from .function_gf import FunctionGF
from .discrete_gf import DiscreteGF
from .continuous_gf import ContinuousGF

# public interface
from .interface import gf_from_series, gf_from_coefficients, gf_from_network
from .standard_gfs import gf_er, gf_powerlaw, gf_plc
