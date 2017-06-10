# Initialisation for "Complex networks, complex processes" package
#
# Copyright (C) 2014-2017 Simon Dobson
# 
# This file is part of Complex networks, complex processes (CNCP).
#
# CNCP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CNCP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CNCP. If not, see <http://www.gnu.org/licenses/gpl.html>.

# regular networks
from .lattice import lattice_graph, draw_lattice
from .ernetworks import erdos_renyi_graph_from_scratch

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


