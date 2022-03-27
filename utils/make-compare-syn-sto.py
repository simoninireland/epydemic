# Create the progress of an epidemic under two different simulation dynamics
#
# Copyright (C) 2017--2022 Simon Dobson
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

from datetime import datetime, timedelta
from epydemic import SIR, Monitor, ProcessSequence, ERNetwork, StochasticDynamics, SynchronousDynamics
from epyc import Experiment, Lab, HDF5LabNotebook
from pandas import DataFrame
import matplotlib
import matplotlib.pyplot as plt
import seaborn
matplotlib.style.use('seaborn')


class MonitoredSIR(SIR):
    '''An SIR model that tracks all its compartments.'''

    def build(self, params):
        super().build(params)
        self.trackNodesInCompartment(SIR.SUSCEPTIBLE)
        self.trackNodesInCompartment(SIR.REMOVED)


def doFigure(rs, dyn, fn):
    '''Draw the monitored progress of a single simulation'''
    fig = plt.figure(figsize=(7, 5))

    lab.notebook().select(rs)
    df = lab.dataframe()
    ts = df[Monitor.OBSERVATIONS].iloc[0]
    ts = [t for t in ts if t < 10000]

    plt.plot(ts, df[Monitor.timeSeriesForLocus(SIR.SUSCEPTIBLE)].iloc[0][:len(ts)],
             'g-', label='Susceptible')
    plt.plot(ts, df[Monitor.timeSeriesForLocus(SIR.INFECTED)].iloc[0][:len(ts)],
             'r-', label='Infected')
    plt.plot(ts, df[Monitor.timeSeriesForLocus(SIR.REMOVED)].iloc[0][:len(ts)],
             'y-', label='Removed')

    plt.ylabel('Number of nodes that are...')
    plt.xlabel('$t$')
    plt.legend(loc='center right')
    plt.title(f'SIR epidemic under {dyn} ($N = {N}, \\langle k \\rangle = {kmean}$)')
    plt.savefig(fn)


# create a lab to hold the results
nb = HDF5LabNotebook('sir-dyn-sto.h5')
lab = Lab(nb)

# network topological parameters (for an ER network)
N = int(1e5)
kmean = 50

# set up the simulations
lab[ERNetwork.N] = N
lab[ERNetwork.KMEAN] = kmean
lab[SIR.P_INFECTED] = 0.001
lab[SIR.P_INFECT] = 0.0001
lab[SIR.P_REMOVE] = 0.001
lab[Monitor.DELTA] = 50

# run the simulations
p = ProcessSequence([MonitoredSIR(), Monitor()])
if not nb.already('sto'):
    e = StochasticDynamics(p, ERNetwork())
    lab.runExperiment(e)
if not nb.already('syn'):
    f = SynchronousDynamics(p, ERNetwork())
    lab.runExperiment(f)

# figure 1: stochastic dynamics
doFigure('sto', 'stochastic dynamics',
         'doc/implementation/sir-stochastic.png')

# figure 2: synchronous dynamics
doFigure('syn', 'synchronous dynamics',
         'doc/implementation/sir-synchronous.png')
