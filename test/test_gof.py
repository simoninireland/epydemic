# Test goodness-of-fit for various distributions
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

import unittest
from collections import Counter
from scipy.stats import chisquare
from mpmath import gammainc
from numpy import exp
from epydemic import *
from epydemic.gf import *


class CaptureNetwork(Process):

    def __init__(self):
        super().__init__()
        self._finalNetwork = None

    def finalNetwork(self):
        return self._finalNetwork

    def setUp(self, params):
        super().setUp(params)
        self._finalNetwork = None

    def results(self):
        rc = super().results()
        self._finalNetwork = self.network()
        return rc


class GFTest(unittest.TestCase):

    SIGNIFICANCE = 0.05    #: P-value at which to reject the null hypothesis (5%).
    REPETITIONS = 5        #: Number of random networks to repeat against.

    def _significance(self, g, gf):
        '''Test whether the degree distribution of the given network
        conforms to the given probability generating function.

        :param g: the network
        :param gf: the generating function
        :returns: True if the network matches the distribution'''

        # construct the degree histogram of the network
        N = g.order()
        seq = sorted([d for (_, d) in g.degree()])
        hist = Counter(seq)
        maxk = max(seq)
        d_network = [hist[i] for i in range(maxk + 1)]

        # construct the expected degree frequency table for the
        # distribution from its generating function
        d_theory = [int(gf[k] * N) for k in range(maxk + 1)]

        # remove any expected-zero degrees
        # sd: this seems like it could go wrong in some instances,
        # but scipy requires that there are no zeros in the expected
        # distribution
        remove = []
        for k in range(maxk + 1):
            if d_theory[k] == 0:
                remove.append(k - len(remove))
        for k in remove:
            del d_network[k]
            del d_theory[k]

        # perform a chi-squared test on the samples
        (_, p) = chisquare(d_network, d_theory)
        #print(p)

        # for a goodness-of-fit test we reject the null hypothesis (that
        # the samples come from the expected distribution) for p-values
        # less that the chosen significance value
        return (p > self.SIGNIFICANCE)

    # ---------- Network generators ----------

    def _testSignificance(self, gen, gf, reps = None):
        '''Perform repeated tests against random networks. We pass if the
        majority pass.

        :param gen: the network generator
        :param gf: the generating function
        :param reps: (optional) number of repetiions'''
        if reps is None:
            reps = self.REPETITIONS
        passes = 0
        for _ in range(reps):
            g = gen.generate()
            if self._significance(g, gf):
                passes += 1
            if passes > reps / 2:
                return

        # if we get here we didn't pass enough tests
        self.assertTrue(False, f'only passed {passes} tests')

    def testERDistribution(self):
        '''Test the ER network generator constructs the right degree distribution.'''
        param = dict()
        param[ERNetwork.N] = 20000
        param[ERNetwork.KMEAN] = 20
        gen = ERNetwork().set(param)
        gf = gf_er(param[ERNetwork.N], kmean=param[ERNetwork.KMEAN])
        self._testSignificance(gen, gf)

    def testPLCDistribution(self):
        '''Test the PLC network generator constructs the right degree distribution.'''
        param = dict()
        param[PLCNetwork.N] = 20000
        param[PLCNetwork.EXPONENT] = 2.0
        param[PLCNetwork.CUTOFF] = 20
        gen = PLCNetwork().set(param)
        gf = gf_plc(param[PLCNetwork.EXPONENT], param[PLCNetwork.CUTOFF])
        self._testSignificance(gen, gf)


    # ---------- Addition-deletion process ----------

    def _make_addition_deletion_gf(self, c):
        '''Construct  the generating function of an addition-deletion process
        that adds nodes with a single fixed degree.

        :param c: the degree of new nodes
        :returns: the generating function'''

        def series(z):
            if z == 1:
                # avoid a division by zero by computing at nearly 0....
                z = 1e-19
            return (exp(c * z) / (1 - z)) * (gammainc(c + 1, c * z) - gammainc(c + 1, c))

        return gf_from_series(series)

    def testAddDeleteDistribution(self):
        '''Test the the addition-deletion process converges as predicted by the theory.'''
        param = dict()
        param[ERNetwork.N] = 20000
        param[ERNetwork.KMEAN] = 20
        gen = ERNetwork().set(param)
        network = gen.generate()
        process = AddDelete()
        process.setMaximumTime(2500)
        capture = CaptureNetwork()
        param[AddDelete.P_ADD] = 1
        param[AddDelete.P_DELETE] = 1
        param[AddDelete.DEGREE] = 10
        e = StochasticDynamics(ProcessSequence([process, capture]), network)
        rc = e.set(param).run(fatal=True)
        g = capture.finalNetwork()

        gf = self._make_addition_deletion_gf(param[AddDelete.DEGREE])
        self._significance(g, gf)


if __name__ == '__main__':
    unittest.main()
