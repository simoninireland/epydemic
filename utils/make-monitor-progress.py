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

import networkx
import math
import numpy
import epyc
import epydemic
from mpmath import polylog as Li
import matplotlib
import matplotlib.pyplot as plt
import seaborn

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
ax.set_xlim([0, T])
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
plt.plot(sss, 'y', label = 'susceptible')
plt.plot(iis, 'r', label = 'infected')
plt.plot(rrs, 'g', label = 'removed')
plt.legend(loc = 'upper right')
plt.savefig('doc/cookbook/sir-progress-dt.png')

class MonitoredSIR(epydemic.SIR, epydemic.Monitor):

    def __init__(self):
        super(MonitoredSIR, self).__init__()

    def build(self, params):
        '''Build the process, adding additional loci to be monitored.
           
        :param params: the parameters'''
        super(MonitoredSIR, self).build(params)

        # add loci for the other compartments 
        self.trackNodesInCompartment(epydemic.SIR.SUSCEPTIBLE)
        self.trackNodesInCompartment(epydemic.SIR.REMOVED)

N = 10000

kmean = 3
phi = kmean / N
er_g = networkx.erdos_renyi_graph(N, phi)

params = dict()
params[epydemic.SIR.P_INFECT] = pInfect
params[epydemic.SIR.P_REMOVE] = pRecover
params[epydemic.SIR.P_INFECTED] = pInfected
params[epydemic.Monitor.DELTA] = 10

e = epydemic.StochasticDynamics(MonitoredSIR(), g = er_g)
e.process().setMaximumTime(T)
rc = e.set(params).run()

fig = plt.figure(figsize = (5, 5))
ax = fig.gca()
plt.title('Progress over an ER network \n $(N = {n}, \\langle k \\rangle = {k}, \\alpha = {a}, \\beta = {b})$'.format(n = N, k = kmean, a = pRecover, b = pInfect))
plt.xlabel('time')
ax.set_xlim([0, T])
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
timeseries = rc[epyc.Experiment.RESULTS][epydemic.Monitor.TIMESERIES]
ts = timeseries[epydemic.Monitor.OBSERVATIONS]
er_sss = list(map(lambda v: v / er_g.order(), timeseries[epydemic.SIR.SUSCEPTIBLE]))
er_iis = list(map(lambda v: v / er_g.order(), timeseries[epydemic.SIR.INFECTED]))
er_rrs = list(map(lambda v: v / er_g.order(), timeseries[epydemic.SIR.REMOVED]))
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

def generateFrom(N, p, maxdeg=100):
    # construct degrees according to the distribution given
    # by the model function
    ns = []
    t = 0
    for i in range(N):
        while True:
            k = rng.integers(1, maxdeg)
            if rng.random() < p(k):
                ns.append(k)
                t += k
                break

    # the final sequence of degrees has to sum to an even number, as
    # each edge has two endpoints
    # if the sequence is odd, remove an element and draw another from
    # the distribution, repeating until the overall sequence is even
    while t % 2 != 0:
        # pick a node at random
        i = rng.integers(0, len(ns) - 1)

        # remove it from the sequence and from the total
        t -= ns[i]
        del ns[i]
            
        # draw a new degree from the distribution
        while True:
            k = rng.integers(1, maxdeg)
            if rng.random() < p(k):
                # add new node to the sequence
                ns.append(k)
                t += k
                break

    # populate the network using the configuration
    # model with the given degree distribution
    g = networkx.configuration_model(ns, create_using=networkx.Graph())
    return g

kappa = 10
alpha = 2
plc_g = generateFrom(N, makePowerlawWithCutoff(alpha, kappa))

e = epydemic.StochasticDynamics(MonitoredSIR(), g = plc_g)
e.process().setMaximumTime(T)
rc = e.set(params).run()

fig = plt.figure(figsize = (5, 5))
ax = fig.gca()
plt.title('Progress over a human contact network \n $(N = {n}, \\kappa = {k}, \\alpha = {a}, \\beta = {b})$'.format(n = N, k = kappa, a = pRecover, b = pInfect))
plt.xlabel('time')
ax.set_xlim([0, T])
plt.ylabel('fraction of population that is...')
ax.set_ylim([0.0, 1.0])
timeseries = rc[epyc.Experiment.RESULTS][epydemic.Monitor.TIMESERIES]
ts = timeseries[epydemic.Monitor.OBSERVATIONS]
plc_sss = list(map(lambda v: v / er_g.order(), timeseries[epydemic.SIR.SUSCEPTIBLE]))
plc_iis = list(map(lambda v: v / er_g.order(), timeseries[epydemic.SIR.INFECTED]))
plc_rrs = list(map(lambda v: v / er_g.order(), timeseries[epydemic.SIR.REMOVED]))
plt.plot(ts, plc_sss, 'y', label = 'susceptible')
plt.plot(ts, plc_iis, 'r', label = 'infected')
plt.plot(ts, plc_rrs, 'g', label = 'removed')
plt.legend(loc = 'upper right')
plt.savefig('doc/cookbook/sir-progress-plc.png')
