# Initialisation for epydemic
#
# Copyright (C) 2017 Simon Dobson
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

'''`epydemic` is a library for performing simulations over networks
for a range of epidemic spreeading (and other) processes. It provides
classes to perform synchronous and stochastic (Gillespie) simulation
over arbitrary networks defined using the Python `networkx` library.
'''
 
# networks with dynamical processes
from .networkdynamics import Dynamics
from .synchronousdynamics import SynchronousDynamics
from .stochasticdynamics import StochasticDynamics

# SIR processes under different dynamics
from .sirsynchronousdynamics import SIRSynchronousDynamics
from .sirstochasticdynamics import SIRStochasticDynamics

# SIS processes under different dynamics
from .sissynchronousdynamics import SISSynchronousDynamics
from .sisstochasticdynamics import SISStochasticDynamics
