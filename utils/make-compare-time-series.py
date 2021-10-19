# Create the doc/cookbook/sir-time-series.png graph
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

nb = HDF5LabNotebook('sir-time-series.h5')
lab = ParallelLab(nb, cores=-2)

N = int(1e5)
kmean = 50

if not nb.already('er'):
    lab[ERNetwork.N] = N
    lab[ERNetwork.KMEAN] = kmean
    lab[SIR.P_INFECTED] = 0.001
    lab[SIR.P_INFECT] = 0.0001
    lab[SIR.P_REMOVE] = 0.001
    lab[Monitor.DELTA] = 1
    lab['repetitions'] = range(10)

    e = StochasticDynamics(ProcessSequence([SIR(), Monitor()]), ERNetwork())
    lab.runExperiment(e)

fig = plt.figure(figsize=(7, 5))

df = lab.dataframe()
ts = df.loc[(df[Monitor.OBSERVATIONS].apply(len) == df[Monitor.OBSERVATIONS].apply(len).max())].iloc[0][Monitor.OBSERVATIONS]
infecteds = DataFrame(df[Monitor.timeSeriesForLocus(SIR.INFECTED)].values.tolist()).rename(columns=lambda i: ts[i])

infectedMeans = list(infecteds.mean())
infectedErrors = list(infecteds.std())

plt.errorbar(ts[:5000:200], [I / N for I in infectedMeans[:5000:200]],
             yerr=[e / N for e in infectedErrors[:5000:200]],
             color='blue', marker='.',
             ecolor='red', capsize=2)

plt.ylabel('$I(t)$')
plt.xlabel('$t$')
plt.title(f'Mean infected fraction of population over time (with error bars)\n$(N = {N}, \\langle k \\rangle = {kmean})$')

plt.savefig('doc/cookbook/sir-time-series.png')

fig = plt.figure(figsize=(7, 5))

for i in range(len(infecteds)):
    cs = list(infecteds.iloc[i])
    plt.scatter(ts[:5000:200], [I / N for I in cs[:5000:200]],
                color='lightblue', marker='.',
                label='raw' if i == 0 else None)

plt.plot(ts[:5000:200], [I / N for I in infectedMeans[:5000:200]],
         color='blue', marker='.',
         label='mean')

plt.ylabel('$I(t)$')
plt.xlabel('$t$')
plt.legend(loc='upper right')
plt.title(f'Mean infected fraction of population over time (with raw data)\n$(N = {N}, \\langle k \\rangle = {kmean})$')

plt.savefig('doc/cookbook/sir-time-series-raw.png')
