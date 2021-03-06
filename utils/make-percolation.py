# Create the percolation diagrams for the Newman-Ziff algorithm
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

from epydemic import BondPercolation, SitePercolation, PLCNetwork
from epyc import Experiment
import matplotlib.pyplot as plt

N = 10000
alpha = 2.0
kappa = 20

params = dict()
params[PLCNetwork.N] = N
params[PLCNetwork.EXPONENT] = alpha
params[PLCNetwork.CUTOFF] = kappa

g = PLCNetwork().set(params).generate()

e = BondPercolation(g)
rcs = e.set(params).run()

fig = plt.figure(figsize = (5, 5))

xs = [rc[Experiment.RESULTS][BondPercolation.P] for rc in rcs]
ys = [rc[Experiment.RESULTS][BondPercolation.GCC] / N for rc in rcs]

plt.xlabel('fraction of occupied bonds $\phi$')
plt.ylabel('size of giant component $S$')
plt.title('Bond percolation on PLC network ($N = {n}, \alpha = {a}, \kappa={k}$)'.format(n=N, a=alpha, k=kappa))
plt.plot(xs, ys, 'g-')
plt.savefig('doc/cookbook/bond-percolation-plc.png')

e = SitePercolation(g)
rcs = e.set(params).run()

fig = plt.figure(figsize = (5, 5))

xs = [rc[Experiment.RESULTS][SitePercolation.P] for rc in rcs]
ys = [rc[Experiment.RESULTS][SitePercolation.GCC] / N for rc in rcs]

plt.xlabel('fraction of occupied sites $\phi$')
plt.ylabel('size of giant component $S$')
plt.title('Site percolation on PLC network ($N = {n}, \alpha = {a}, \kappa={k}$)'.format(n=N, a=alpha, k=kappa))
plt.plot(xs, ys, 'g-')
plt.savefig('doc/cookbook/site-percolation-plc.png')
