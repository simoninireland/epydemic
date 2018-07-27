# Create the doc/cookbook-powerlaw-cutoff.png diagram comparing the two
# different degree distributions
#
# Copyright (C) 2017--2018 Simon Dobson
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

import math
import numpy
from scipy.special import zeta
from mpmath import polylog as Li
import matplotlib
import matplotlib.pyplot as plt
import seaborn


def make_powerlaw(alpha):
    '''Create a model function for a powerlaw distribution.

    :param alpha: the exponent of the distribution
    :returns: a model function'''
    C = 1.0 / zeta(alpha, 1)

    def p(k):
        return C * pow((k + 0.0), -alpha)
    return p

def make_powerlaw_with_cutoff(alpha, kappa):
    '''Create a model function for a powerlaw distribution with exponential cutoff.

    :param alpha: the exponent of the distribution
    :param kappa: the degree cutoff
    :returns: a model function'''
    C = Li(alpha, math.exp(-1.0 / kappa))

    def p(k):
        return (pow((k + 0.0), -alpha) * math.exp(-(k + 0.0) / kappa)) / C
    return p

alpha = 2
kappa = 10

fig = plt.figure(figsize = (5, 5))

xs = numpy.linspace(1, 100)
powerlaw = make_powerlaw(alpha)
powerlaw_cutoff = make_powerlaw_with_cutoff(alpha, kappa)

plt.xlabel('$\\log \\, k$')
plt.ylabel('$\\log \\, p_k$')
plt.title('Powerlaw with and without cutoff ($\\alpha = {a}$)'.format(a = alpha))
plt.plot(xs, [ powerlaw(x) for x in xs ], 'g-', label='powerlaw')
plt.plot(xs, [ powerlaw_cutoff(x) for x in xs ], 'r-',
         label='powerlaw with cutoff at $\\kappa = {k}$'.format(k = kappa))
plt.loglog()
plt.legend()
plt.savefig('doc/cookbook/powerlaw-cutoff.png')
