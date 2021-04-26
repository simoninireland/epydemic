# Utility for profiling simulations
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

import cProfile
from pstats import Stats, SortKey
from epydemic import SIR, ERNetwork, StochasticDynamics

profile = "profile.pstats"

N = int(1e5)
kmean = 10

params = dict()
params[SIR.P_INFECT] = 0.05
params[SIR.P_REMOVE] = 0.01
params[SIR.P_INFECTED] = 0.001
params[ERNetwork.N] = N
params[ERNetwork.KMEAN] = kmean

e = StochasticDynamics(SIR(), ERNetwork())
cProfile.run('e.set(params).run()', profile)

p = Stats(profile)
p.sort_stats(SortKey.TIME).print_stats(10)
