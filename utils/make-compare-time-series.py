# Create the time series graphs wiith error bars and raw data
#
# Copyright (C) 2017--2021 Simon Dobson
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

from epydemic import SIR, Monitor, ProcessSequence, ERNetwork, StochasticDynamics
from epyc import ParallelLab, HDF5LabNotebook
from pandas import DataFrame
import matplotlib
import matplotlib.pyplot as plt
import seaborn
matplotlib.style.use('seaborn')

# put the results into a persistent resultset so we can
# tweak thhe presentation without re-doing the simulations.
nb = HDF5LabNotebook('sir-time-series.h5')

# a lab on a multicore workstaion, leaving two cores free
lab = ParallelLab(nb, cores=-2)

# network topological parameters (for an ER network)
N = int(1e5)
kmean = 50

if not nb.already('er'):
    # run the simulations
    lab[ERNetwork.N] = N
    lab[ERNetwork.KMEAN] = kmean
    lab[SIR.P_INFECTED] = 0.001
    lab[SIR.P_INFECT] = 0.0001
    lab[SIR.P_REMOVE] = 0.001
    lab[Monitor.DELTA] = 1
    lab['repetitions'] = range(10)

    e = StochasticDynamics(ProcessSequence([SIR(), Monitor()]), ERNetwork())
    lab.runExperiment(e)

# figure 1: mean I size with error bars
fig = plt.figure(figsize=(7, 5))

# sub-sampling in time and space
maxt = 5000
step = 200

# wrangle the time series fore observations and infected component size
df = lab.dataframe()
ts = df.loc[(df[Monitor.OBSERVATIONS].apply(len) == df[Monitor.OBSERVATIONS].apply(len).max())].iloc[0][Monitor.OBSERVATIONS]
infecteds = DataFrame(df[Monitor.timeSeriesForLocus(SIR.INFECTED)].values.tolist()).rename(columns=lambda i: ts[i])

# summary statistics
infectedMeans = list(infecteds.mean())
infectedErrors = list(infecteds.std())

# plot the summary, with error bars
plt.errorbar(ts[:maxt:step], [I / N for I in infectedMeans[:maxt:step]],
             yerr=[e / N for e in infectedErrors[:maxt:step]],
             color='blue', marker='.',
             ecolor='red', capsize=2)

plt.ylabel('$I(t)$')
plt.xlabel('$t$')
plt.title(f'Mean infected fraction of population over time (with error bars)\n$(N = {N}, \\langle k \\rangle = {kmean})$')
plt.savefig('doc/cookbook/sir-time-series.png')

# figure 2: mean I size with raw data
fig = plt.figure(figsize=(7, 5))

# plot all the raw results
for i in range(len(infecteds)):
    cs = list(infecteds.iloc[i])
    plt.scatter(ts[:maxt:step], [I / N for I in cs[:maxt:step]],
                color='lightblue', marker='.',     # light shading
                label='raw' if i == 0 else None)   # only label the first series

# plot the mean (no error bars this time)
plt.plot(ts[:maxt:step], [I / N for I in infectedMeans[:maxt:step]],
         color='blue', marker='.',   # darker shade than the raw data
         label='mean')

plt.ylabel('$I(t)$')
plt.xlabel('$t$')
plt.legend(loc='upper right')
plt.title(f'Mean infected fraction of population over time (with raw data)\n$(N = {N}, \\langle k \\rangle = {kmean})$')
plt.savefig('doc/cookbook/sir-time-series-raw.png')
