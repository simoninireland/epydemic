# Create the doc/cookbook/sir-progress-*.png graphs
#
# Copyright (C) 2017--2019 Simon Dobson
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

import networkx
import math
import numpy
import epyc
import epydemic
from mpmath import polylog as Li
import matplotlib
import matplotlib.pyplot as plt
import seaborn

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

pRecover = 0.002
pInfect = 0.02
pInfected = 0.01
T = 1000

sss = [ 1.0 - pInfected ]    # susceptible: all except those initially infected
iis = [ pInfected ]          # infected
rrs = [ 0.00 ]               # recovered: none to start with

(dS, dI, dR) = make_sir(pRecover, pInfect)

for t in range(0, T):
    sss.append(sss[t] + dS(sss[t], iis[t], rrs[t]))
    iis.append(iis[t] + dI(sss[t], iis[t], rrs[t]))
    rrs.append(rrs[t] + dR(sss[t], iis[t], rrs[t]))

fig = plt.figure(figsize = (5, 5))
ax = fig.gca()
plt.title('Progress of an infection $(\\alpha = {a}, \\beta = {b})$'.format(a = pRecover, b = pInfect))
plt.xlabel('time')
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
plt.plot(sss, 'y', label = 'susceptible')
plt.plot(iis, 'r', label = 'infected')
plt.plot(rrs, 'g', label = 'removed')
plt.legend(loc = 'upper right')
plt.savefig('doc/cookbook/sir-progress-dt.png')

class MonitoredSIR(epydemic.SIR):
    INTERVAL = 'interval'
    PROGRESS = 'progress'

    def setUp(self, params):
        '''Schedule the monitoring event.

        :param params: the simulation parameters'''
        super(MonitoredSIR, self).setUp(params)

        # add a monitoring event to fill-in the evolution of the process
        self._series = []
        self.postRepeatingEvent(0, params[self.INTERVAL], None, self.monitor)

    def monitor(self, t, e):
        '''Record the sizes of each compartment.

        :param t: the simulation time
        :param e: the element (ignored)'''
        s = dict()
        for k in [epydemic.SIR.SUSCEPTIBLE, epydemic.SIR.INFECTED, epydemic.SIR.REMOVED]:
            s[k] = len(self.compartment(k))
        self._series.append((t, s))

    def results(self):
        '''Add the time series to the results.

        :returns: a results dict including the monitored time series'''
        rc = super(MonitoredSIR, self).results()

        rc[self.PROGRESS] = self._series
        return rc

N = 10000

kmean = 3
phi = kmean / N
er_g = networkx.erdos_renyi_graph(N, phi)

params = dict()
params[epydemic.SIR.P_INFECT] = pInfect
params[epydemic.SIR.P_REMOVE] = pRecover
params[epydemic.SIR.P_INFECTED] = pInfected
params[MonitoredSIR.INTERVAL] = 10

e = epydemic.StochasticDynamics(MonitoredSIR(), g = er_g)
e.process().setMaximumTime(1000)
rc = e.set(params).run()

fig = plt.figure(figsize = (5, 5))
ax = fig.gca()
plt.title('Progress over an ER network \n $(N = {n}, \\langle k \\rangle = {k}, \\alpha = {a}, \\beta = {b})$'.format(n = N, k = kmean, a = pRecover, b = pInfect))
plt.xlabel('time')
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
ts = list(map(lambda tp: tp[0], rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
er_sss = list(map(lambda tp: tp[1][epydemic.SIR.SUSCEPTIBLE] / er_g.order(), rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
er_iis = list(map(lambda tp: tp[1][epydemic.SIR.INFECTED] / er_g.order(), rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
er_rrs = list(map(lambda tp: tp[1][epydemic.SIR.REMOVED] / er_g.order(), rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
plt.plot(ts, er_sss, 'y', label = 'susceptible')
plt.plot(ts, er_iis, 'r', label = 'infected')
plt.plot(ts, er_rrs, 'g', label = 'removed')
plt.legend(loc = 'upper right')
plt.savefig('doc/cookbook/sir-progress-er.png')

def makePowerlawWithCutoff(alpha, kappa):
    '''Create a model function for a powerlaw distribution with exponential cutoff.

    :param alpha: the exponent of the distribution
    :param kappa: the degree cutoff
    :returns: a model function'''
    C = Li(alpha, math.exp(-1.0 / kappa))
    def p( k ):
        return (pow((k + 0.0), -alpha) * math.exp(-(k + 0.0) / kappa)) / C
    return p

def generateFrom(N, p, maxdeg = 100):
    '''Generate a random graph with degree distribution described
    by a model function.

    :param N: number of numbers to generate
    :param p: model function
    :param maxdeg: maximum node degree we'll consider (defaults to 100)
    :returns: a network with the given degree distribution'''

    # construct degrees according to the distribution given
    # by the model function
    ns = []
    t = 0
    for i in range(N):
        while True:
            k = 1 + int (numpy.random.random() * (maxdeg - 1))
            if numpy.random.random() < p(k):
                ns = ns + [ k ]
                t = t + k
                break

    # if the sequence is odd, choose a random element
    # and increment it by 1 (this doesn't change the
    # distribution significantly, and so is safe)
    if t % 2 != 0:
        i = int(numpy.random.random() * len(ns))
        ns[i] = ns[i] + 1

    # populate the network using the configuration
    # model with the given degree distribution
    g = networkx.configuration_model(ns, create_using = networkx.Graph())
    g = g.subgraph(max(networkx.connected_components(g), key = len)).copy()
    g.remove_edges_from(list(g.selfloop_edges()))
    return g

kappa = 10
alpha = 2
plc_g = generateFrom(N, makePowerlawWithCutoff(alpha, kappa))

e = epydemic.StochasticDynamics(MonitoredSIR(), g = plc_g)
e.process().setMaximumTime(1000)
rc = e.set(params).run()

fig = plt.figure(figsize = (5, 5))
ax = fig.gca()
plt.title('Progress over a human contact network \n $(N = {n}, \\kappa = {k}, \\alpha = {a}, \\beta = {b})$'.format(n = N, k = kappa, a = pRecover, b = pInfect))
plt.xlabel('time')
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
ts = list(map(lambda tp: tp[0], rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
plc_sss = list(map(lambda tp: tp[1][epydemic.SIR.SUSCEPTIBLE] / plc_g.order(), rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
plc_iis = list(map(lambda tp: tp[1][epydemic.SIR.INFECTED] / plc_g.order(), rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
plc_rrs = list(map(lambda tp: tp[1][epydemic.SIR.REMOVED] / plc_g.order(), rc[epyc.Experiment.RESULTS][MonitoredSIR.PROGRESS]))
plt.plot(ts, plc_sss, 'y', label = 'susceptible')
plt.plot(ts, plc_iis, 'r', label = 'infected')
plt.plot(ts, plc_rrs, 'g', label = 'removed')
plt.legend(loc = 'upper right')
plt.savefig('doc/cookbook/sir-progress-plc.png')
