# Create the percolation diagrams for the Newman-Ziff algorithm
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

from epydemic import BondPercolation, SitePercolation, ERNetwork, PLCNetwork
from epyc import Experiment
import matplotlib.pyplot as plt

# network topological parameters
N = 10000
kmean = 20
alpha = 2.0
kappa = 20

params = dict()
params[ERNetwork.N] = N
params[ERNetwork.KMEAN] = kmean
params[PLCNetwork.N] = N
params[PLCNetwork.EXPONENT] = alpha
params[PLCNetwork.CUTOFF] = kappa

# construct networks
g_er = ERNetwork().set(params).generate()
g_plc = PLCNetwork().set(params).generate()

# bond-percolate the networks
e_er = BondPercolation(g_er)
rc_er = e_er.set(params).run()
e_plc = BondPercolation(g_plc)
rc_plc = e_plc.set(params).run()

# figure 1a: the bond percolation behaviour of an ER network
fig = plt.figure(figsize=(5, 5))

xs = rc_er[Experiment.RESULTS][BondPercolation.P]
ys = [gcc / N for gcc in rc_er[Experiment.RESULTS][BondPercolation.GCC]]
plt.plot(xs, ys, 'g-')

plt.xlabel('fraction of occupied bonds $\phi$')
plt.ylabel('size of giant component $S$')
plt.title(f'Bond percolation on ER network ($N = {N}, \\langle k \\rangle = {kmean}$)', size='medium')
plt.savefig('doc/cookbook/bond-percolation-er.png')

# figure 1b: the bond percolation behaviour of a PLC network
fig = plt.figure(figsize=(5, 5))

xs = rc_plc[Experiment.RESULTS][BondPercolation.P]
ys = [gcc / N for gcc in rc_plc[Experiment.RESULTS][BondPercolation.GCC]]
plt.plot(xs, ys, 'g-')

plt.xlabel('fraction of occupied bonds $\phi$')
plt.ylabel('size of giant component $S$')
plt.title(f'Bond percolation on PLC network ($N = {N}, \\alpha = {alpha}, \\kappa={kappa}$)', size='medium')
plt.savefig('doc/cookbook/bond-percolation-plc.png')

# site-percolate the networks
e_er = SitePercolation(g_er)
rc_er = e_er.set(params).run()
e_plc = SitePercolation(g_plc)
rc_plc = e_plc.set(params).run()

# figurer 2a: site percolation behaviour for an ER network
fig = plt.figure(figsize=(5, 5))

xs = rc_er[Experiment.RESULTS][SitePercolation.P]
ys = [gcc / N for gcc in rc_er[Experiment.RESULTS][SitePercolation.GCC]]
plt.plot(xs, ys, 'g-')

plt.xlabel('fraction of occupied sites $\phi$')
plt.ylabel('size of giant component $S$')
plt.title(f'Site percolation on ER network ($N = {N}, \\langle k \\rangle = {kmean}$)', size='medium')
plt.savefig('doc/cookbook/site-percolation-er.png')

# figurer 2a: site percolation behaviour for a PLC network
fig = plt.figure(figsize=(5, 5))

xs = rc_plc[Experiment.RESULTS][SitePercolation.P]
ys = [gcc /  N for gcc in rc_plc[Experiment.RESULTS][SitePercolation.GCC]]
plt.plot(xs, ys, 'g-')

plt.xlabel('fraction of occupied sites $\phi$')
plt.ylabel('size of giant component $S$')
plt.title(f'Site percolation on PLC network ($N = {N}, \\alpha = {alpha}, \\kappa={kappa}$)', size='medium')
plt.savefig('doc/cookbook/site-percolation-plc.png')
