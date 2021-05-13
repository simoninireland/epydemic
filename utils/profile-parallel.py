# Utility for profiling parallel execution using PyPy compute cluster
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

from epyc import ClusterLab, LabNotebook, RepeatedExperiment
from epydemic import SIR, ERNetwork, StochasticDynamics
from numpy import linspace

N = int(1e5)
kmean = 10

nb = LabNotebook()
lab = ClusterLab(nb, profile='epyctest')
lab[SIR.P_INFECT] = linspace(0.01, 0.10, num=25)
lab[SIR.P_REMOVE] = 0.01
lab[SIR.P_INFECTED] = 0.001
lab[ERNetwork.N] = N
lab[ERNetwork.KMEAN] = kmean

e = RepeatedExperiment(StochasticDynamics(SIR(), ERNetwork()), 4)
lab.runExperiment(e)
lab.wait()
