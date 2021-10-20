# Create the doc/cookbook/sir-progress-*.png graphs
#
# Copyright (C) 2017--2020 Simon Dobson
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

import numpy
from epyc import Experiment
from epydemic import SIR, Monitor, ProcessSequence, ERNetwork, PLCNetwork, StochasticDynamics
import matplotlib
import matplotlib.pyplot as plt
import seaborn
matplotlib.style.use('seaborn')


# random number generator for later
rng = numpy.random.default_rng()


def make_sir(alpha, beta):
    '''Return functions for changes in the susceptible, infected, and recovered
    sub-populations for particular rates of recovery and infection.

    :param alpha: rate of recovery
    :param beta: rate of infection
    :returns: triple of change functions for dS, dI, and dR'''

    def dS(S, I, R):
        return -beta * I * S

    def dI(S, I, R):
        return beta * I * S - alpha * I

    def dR(S, I, R):
        return alpha * I

    return (dS, dI, dR)

# epidemic parameters
pRecover = 0.002
pInfect = 0.02
pInfected = 0.01
T = 1000

# initial sizes of compartments
sss = [1.0 - pInfected]    # susceptible: all except those initially infected
iis = [pInfected]          # infected
rrs = [0.0]                # recovered: none to start with

# build the infinitesimal functions
(dS, dI, dR) = make_sir(pRecover, pInfect)

# push the state of ther system through the ODEs
for t in range(0, T):
    sss.append(sss[t] + dS(sss[t], iis[t], rrs[t]))
    iis.append(iis[t] + dI(sss[t], iis[t], rrs[t]))
    rrs.append(rrs[t] + dR(sss[t], iis[t], rrs[t]))

# figure 1: plot the ODE solution
fig = plt.figure(figsize=(5, 5))
ax = fig.gca()

# plot the time series for the three compartments
plt.plot(sss, 'y', label='susceptible')
plt.plot(iis, 'r', label='infected')
plt.plot(rrs, 'g', label='removed')

plt.title(f'Progress of an infection $(\\alpha = {pRecover}, \\beta = {pInfect})$')
plt.xlabel('time')
ax.set_xlim([0, T])
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
plt.legend(loc='upper right')
plt.savefig('doc/cookbook/sir-progress-dt.png')


class MonitoredSIR(SIR):
    '''An SIR model that captures all its components, not just I and SI.'''

    def build(self, params):
        '''Build the process, adding additional loci to be monitored.

        :param params: the parameters'''
        super().build(params)

        # add loci for the other compartments
        self.trackNodesInCompartment(SIR.SUSCEPTIBLE)
        self.trackNodesInCompartment(SIR.REMOVED)

# network topological parameters (ER network)
N = 10000
kmean = 3

params = dict()
params[ERNetwork.N] = N
params[ERNetwork.KMEAN] = kmean
params[SIR.P_INFECT] = pInfect
params[SIR.P_REMOVE] = pRecover
params[SIR.P_INFECTED] = pInfected
params[Monitor.DELTA] = 10

e = StochasticDynamics(ProcessSequence([MonitoredSIR(), Monitor()]), ERNetwork())
e.process().setMaximumTime(T)
rc = e.set(params).run()

res = rc[Experiment.RESULTS]
ts = res[Monitor.OBSERVATIONS]
er_sss = list(map(lambda v: v / N, res[Monitor.timeSeriesForLocus(SIR.SUSCEPTIBLE)]))
er_iis = list(map(lambda v: v / N, res[Monitor.timeSeriesForLocus(SIR.INFECTED)]))
er_rrs = list(map(lambda v: v / N, res[Monitor.timeSeriesForLocus(SIR.REMOVED)]))

# figure 2: same epidemic on ER network
fig = plt.figure(figsize = (5, 5))
ax = fig.gca()

plt.plot(ts, er_sss, 'y', label='susceptible')
plt.plot(ts, er_iis, 'r', label='infected')
plt.plot(ts, er_rrs, 'g', label='removed')

plt.title(f'Progress over an ER network \n $(N = {N}, \\langle k \\rangle = {kmean}, \\alpha = {pRecover}, \\beta = {pInfect})$')
plt.xlabel('time')
ax.set_xlim([0, T])
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
plt.legend(loc = 'upper right')
plt.savefig('doc/cookbook/sir-progress-er.png')

# network topological parameters (PLC network)
kappa = 10
alpha = 2

params[PLCNetwork.N] = N
params[PLCNetwork.EXPONENT] = alpha
params[PLCNetwork.CUTOFF] = kappa

e = StochasticDynamics(ProcessSequence([MonitoredSIR(), Monitor()]), PLCNetwork())
e.process().setMaximumTime(T)
rc = e.set(params).run()
res = rc[Experiment.RESULTS]
ts = res[Monitor.OBSERVATIONS]
plc_sss = list(map(lambda v: v / N, res[Monitor.timeSeriesForLocus(SIR.SUSCEPTIBLE)]))
plc_iis = list(map(lambda v: v / N, res[Monitor.timeSeriesForLocus(SIR.INFECTED)]))
plc_rrs = list(map(lambda v: v / N, res[Monitor.timeSeriesForLocus(SIR.REMOVED)]))

# figure 3: same epidemicon PLC network
fig = plt.figure(figsize = (5, 5))
ax = fig.gca()

plt.plot(ts, plc_sss, 'y', label='susceptible')
plt.plot(ts, plc_iis, 'r', label='infected')
plt.plot(ts, plc_rrs, 'g', label='removed')

plt.title(f'Progress over a human contact network \n $(N = {N}, \\kappa = {kappa}, \\alpha = {pRecover}, \\beta = {pInfect})$')
plt.xlabel('time')
ax.set_xlim([0, T])
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
plt.legend(loc='upper right')
plt.savefig('doc/cookbook/sir-progress-plc.png')
