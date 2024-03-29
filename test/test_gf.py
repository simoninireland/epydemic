# Test generating functions
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

from epydemic import *
from epydemic.gf import *
from collections import Counter
import unittest
import networkx
from math import factorial

class GFTest(unittest.TestCase):

    # Helper functions

    def _histogram(self, g):
        '''Return the degree distribution fractions histogram.

        :param g: the network
        :returns: the degree distribution histogram'''
        N = g.order()
        return [nk / N for nk in networkx.degree_histogram(g)]

    # Discrete distributions extracted from networks

    def testDiscreteProbabilities(self):
        '''Test that the coefficients of a discrete GF sum to 1.'''
        g = networkx.gnp_random_graph(5000, 0.005)
        gf = DiscreteGF(g=g)
        self.assertAlmostEqual(gf(1.0), 1.0, places=2)

    def testDiscreteHistogram(self):
        '''Test we get the coefficients matching the histogram.'''
        g = networkx.gnp_random_graph(5000, 0.005)

        # check coefficient for degree 4 matches the network
        ns = []
        for n in g.nodes:
            if len(list(g.neighbors(n))) == 4:
                ns.append(n)
        gf = DiscreteGF(g=g)
        N = g.order()
        self.assertAlmostEqual(gf[4], len(ns) / N, places=2)

        # delete all nodes of degree 8 or less
        ns = []
        for n in g.nodes:
            if len(list(g.neighbors(n))) <= 8:
                ns.append(n)
        g.remove_nodes_from(ns)
        gf = DiscreteGF(g=g)
        for k in range(9):
            self.assertEqual(gf[k], 0)

    def testNetworkDerivative(self):
        '''Test differentiation for networks.'''
        g = networkx.gnp_random_graph(5000, 0.005)
        gf = gf_from_network(g)
        gfprime = gf.dx()
        self.assertAlmostEqual(gfprime(1), (5000 * 0.005), delta=1)

    def testNetworkCoefficientsByDifferentiation(self):
        '''Test that coefficients are retrieved correctly by differentiation.'''
        g = networkx.fast_gnp_random_graph(10000, 0.005)
        gf = gf_from_network(g)

        cs = self._histogram(g)
        gcs = [(gf.dx(k))(0) / factorial(k) for k in range(len(cs))]
        for k in range(len(cs)):
            self.assertAlmostEqual(cs[k], gf[k], places=1)

    def testFromCoefficients(self):
        '''Test we can create a generating function from explicit coefficients.'''
        coeffs = [0, 0.05, 0.7, 0.25]
        gf = gf_from_coefficients(coeffs)
        self.assertEqual(gf(1.0), 1.0)
        for k in range(len(coeffs)):
            self.assertEqual(coeffs[k], gf[k])
        self.assertEqual(gf[k + 1], 0.0)

    def testFromFunction(self):
        '''Test we can create a generating function from a function returning the coefficients.'''
        coeffs = [0, 0.05, 0.7, 0.25]

        def f(k):
            if k < len(coeffs):
                return coeffs[k]
            else:
                return 0

        gf = gf_from_coefficient_function(f)
        self.assertEqual(gf(1.0), 1.0)
        for k in range(len(coeffs)):
            self.assertEqual(coeffs[k], gf[k])
        self.assertEqual(gf[k + 1], 0.0)

    def testNoParametersDiscreteGF(self):
        '''Test we detect no valid parameters passed to build a discrete generating function.'''
        with self.assertRaises(TypeError):
            _ = DiscreteGF()

    def testDiffCoeff(self):
        '''Test we can differentiate coefficients.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])

        d = gf1.dx()
        self.assertEqual(d[0], 2)
        self.assertEqual(d[1], 6)
        self.assertEqual(d[2], 0)
        self.assertEqual(d[3], 4)
        self.assertEqual(d[4], 0)

    def testDiffCoeffTwice(self):
        '''Test we can differentiate coefficients twice.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])

        d = gf1.dx(2)
        self.assertEqual(d[0], 6)
        self.assertEqual(d[1], 0)
        self.assertEqual(d[2], 12)

    def testDiffCoeffTwiceLinear(self):
        '''Test differentiation over coefficients is linear.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])

        d1 = gf1.dx(2)
        d2 = gf1.dx().dx()
        for i in range(5):
            self.assertEqual(d1[i], d2[i])

    def testDiffCoeffTwiceToZero(self):
        '''Test we can differentiate coefficients of a low-order GF twice, yielding zero.'''
        gf1 = gf_from_coefficients([0, 2])

        d = gf1.dx(2)
        self.assertEqual(d[0], 0)
        self.assertEqual(d[1], 0)

    # Continuous series distributions

    def testHighDegreeExtraction(self):
        '''Test we can extract a range of coefficients, including very large ones.'''
        gf = gf_er(50000, kmean=200)

        # extract high-degree coefficients
        # This relies on being able to do high-precision computation. We
        # don't care about the results, just that they don't cause exceptions
        for k in [0, 5, 10, 100, 200, 400, 1000, 5000, 10000]:
            gf[k]

    def testSeriesDerivative(self):
        '''Test differentiation for series.'''
        gf = gf_er(5000, phi=0.005)
        gfprime = gf.dx()
        self.assertAlmostEqual(gfprime(1), (5000 * 0.005), places=2)


    # Standard distributions

    def testNoParametersER(self):
        '''Test we detect no valid parameters for an ER network.'''
        with self.assertRaises(TypeError):
            gf = gf_er(10000)

    def testERProbabilities(self):
        '''Test that the ER GF evaluates to 1.'''
        gf = gf_er(5000, 0.005)
        self.assertAlmostEqual(gf(1.0), 1.0, places=2)

    def testERnormalised(self):
        '''Test the ER GF sums to 1.'''
        gf = gf_er(5000, phi=0.005)
        kmean = int(5000 * 0.005)
        v = 0.0
        for k in range(2 * kmean):
            v += gf[k]
        self.assertAlmostEqual(v, 1.0, places=2)

    def testERdistribution(self):
        '''Test that the ER distribution matches its generating function.'''
        g = networkx.gnp_random_graph(5000, 0.005)
        gf = gf_er(5000, phi=0.005)

        cs = self._histogram(g)
        gcs = [gf[k] for k in range(len(cs))]
        for k in range(len(cs)):
            self.assertAlmostEqual(cs[k], gf[k], places=1)

    def testERmean(self):
        '''Test extraction of the mean degree for ER networks.'''
        N = 5000
        phi = 0.005
        kmean = N * phi

        g = networkx.gnp_random_graph(N, phi)
        gf = gf_er(N, phi=0.005)
        gf_prime = gf.dx()

        self.assertAlmostEqual(gf_prime(1), kmean, delta=1)

        degrees = [d for (_, d) in g.degree()]
        kmean_empirical = sum(degrees) / N
        self.assertAlmostEqual(gf_prime(1), kmean_empirical, delta=1)

    def testPLProbabilities(self):
        '''Test that the powerlaw GF evaluates to 1.'''
        gf = gf_powerlaw(3.0)
        self.assertAlmostEqual(gf(1.0), 1.0, places=2)

    # def testPLmean(self):
    #     '''Test extraction of the mean degree for powerlaw neworks.'''
    #     N = 10000
    #     M = 2

    #     g = networkx.barabasi_albert_graph(N, M)
    #     gf = gf_powerlaw(3)
    #     gf_prime = gf.dx()

    #     degrees = [d for (_, d) in g.degree()]
    #     kmean_empirical = sum(degrees) / N
    #     self.assertAlmostEqual(gf_prime(1.0), kmean_empirical, delta=1)

    def testBADistribution(self):
        '''Test the degree distribution of the BA network.'''
        N = 5000
        M = 4

        params = dict()
        params[BANetwork.N] = N
        params[BANetwork.M] = M
        g = BANetwork().set(params).generate()
        gf = gf_ba(M)
        cs = self._histogram(g)
        for k in range(M + 10, len(cs)):
            self.assertAlmostEqual(cs[k], gf[k], places=2)

    def testPLCProbabilities(self):
        '''Test that the PLC GF evaluates to 1.'''
        gf = gf_plc(3.0, 60)
        self.assertAlmostEqual(gf(1.0), 1.0, places=2)

    def testPLCnormalised(self):
        '''Test that the PLC GF sums to 1.'''
        gf = gf_plc(2.0, 60)
        v = 0.0
        for k in range(60):
            v += gf[k]
        self.assertAlmostEqual(v, 1.0, places=2)

    def testPLCdistribution(self):
        '''Test that the PLC distribution matches its generating function.'''
        params = dict()
        params[PLCNetwork.N] = 5000
        params[PLCNetwork.EXPONENT] = 2.0
        params[PLCNetwork.CUTOFF] = 20
        g = PLCNetwork().set(params).generate()
        gf = gf_plc(params[PLCNetwork.EXPONENT], params[PLCNetwork.CUTOFF])

        cs = self._histogram(g)
        gcs = [gf[k] for k in range(len(cs))]
        for k in range(len(cs)):
            self.assertAlmostEqual(cs[k], gf[k], places=1)

    def testPLCmean(self):
        '''Test extraction of the mean degree for PLC neworks.'''
        param = dict()
        param[PLCNetwork.N] = 5000
        param[PLCNetwork.EXPONENT] = 3.0
        param[PLCNetwork.CUTOFF] = 25
        g = PLCNetwork().set(param).generate()
        gf = gf_plc(3.0, 25)
        gf_prime = gf.dx()

        degrees = [d for (_, d) in g.degree()]
        kmean_empirical = sum(degrees) / 5000
        self.assertAlmostEqual(gf_prime(1), kmean_empirical, delta=1)


    # ---------- Operators ----------

    def testMulContinuous(self):
        '''Test we can multiply a continuous GF by a constant.'''
        gf = gf_er(10000, 20)
        gf4 = gf * 4
        for i in range(1, 20):
            self.assertEqual(gf4[i], 4 * gf[i])

    def testDivContinuous(self):
        '''Test we can divide a continuous GF by a constant.'''
        gf = gf_er(10000, 20)
        gf4 = gf / 4
        for i in range(1, 20):
            self.assertAlmostEqual(gf4[i], gf[i] / 4, places=3)

    def testMulFunction(self):
        '''Test we can multiply a function GF by a constant.'''
        gf = gf_ba(3)
        gf4 = gf * 4
        for i in range(1, 20):
            self.assertEqual(gf4[i], 4 * gf[i])

    def testDivFunction(self):
        '''Test we can divide a function GF by a constant.'''
        gf = gf_ba(3)
        gf4 = gf / 4
        for i in range(1, 20):
            self.assertAlmostEqual(gf4[i], gf[i] / 4, places=3)

    def testMulNetwork(self):
        '''Test we can multiply a measured empirical GF by a constant.'''
        N = 10000
        kmean = 20
        phi = kmean / N

        g = networkx.gnp_random_graph(N, phi)
        gf = gf_from_network(g)
        gf4 = gf * 4
        for i in range(1, 20):
            self.assertEqual(gf4[i], 4 * gf[i])

    def testDivNetwork(self):
        '''Test we can divide a measured empirical GF by a constant.'''
        N = 10000
        kmean = 20
        phi = kmean / N

        g = networkx.gnp_random_graph(N, phi)
        gf = gf_from_network(g)
        gf4 = gf / 4
        for i in range(1, 20):
            self.assertAlmostEqual(gf4[i], gf[i] / 4, places=3)

    def testProductSimple(self):
        '''Test we can do simple multiplication of GFs.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        p = gf1 * gf2
        self.assertEqual(p[0], 0)
        self.assertEqual(p[1], 6)
        self.assertEqual(p[2], 4)
        self.assertEqual(p[3], 6)
        self.assertEqual(p[4], 0)
        self.assertEqual(p[5], 2)

    def testProductTwo(self):
        '''Test we can do more complex multiplication of GFs.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([1, 2])

        p = gf1 * gf2
        self.assertEqual(p[0], 3)
        self.assertEqual(p[1], 8)
        self.assertEqual(p[2], 7)
        self.assertEqual(p[3], 6)
        self.assertEqual(p[4], 1)
        self.assertEqual(p[5], 2)

    def testProductTwoAssociate(self):
        '''Test that the product of GFs associates.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        p1 = gf1 * gf2
        p2 = gf2 * gf1
        for i in range(5):
            self.assertEqual(p2[i], p2[i])

    def testProductConst(self):
        '''Test that two products formed in different ways are the same.'''
        c = 2
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([c])

        p1 = gf1 * gf2
        p2 = gf1 * c
        for i in range(5):
            self.assertEqual(p1[i], p2[i])

    def testProductScale(self):
        '''Test we can scale a multiplication of GFs.'''
        c = 4
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([1, 2])

        p1 = gf1 * gf2
        p2 = p1 * c
        for i in range(5):
            self.assertEqual(p2[i], p1[i] * c)

    def testProductScaleAssociate(self):
        '''Test that multiplication of a product by a constant associates.'''
        c = 4
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([1, 2])

        p1 = gf1 * gf2
        p2 = gf2 * gf1
        for i in range(5):
            self.assertEqual(p2[i], p2[i])

    def testAddConstant(self):
        '''Test we can add a constant to a GF.'''
        c = 2
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])

        s = gf1 + c
        self.assertEqual(s[0], gf1[0] + c)
        for i in range(1, 5):
            self.assertEqual(s[i], gf1[i])

    def testAddTwo(self):
        '''Test we can do the sum of GFs.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([1, 2])

        s = gf1 + gf2
        self.assertEqual(s[0], 4)
        self.assertEqual(s[1], 4)
        self.assertEqual(s[2], 3)
        self.assertEqual(s[3], 0)
        self.assertEqual(s[4], 1)
        self.assertEqual(s[5], 0)

    def testSubConstant(self):
        '''Test we can subtract a constant from a GF.'''
        c = 2
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])

        s = gf1 - c
        self.assertEqual(s[0], gf1[0] - c)
        for i in range(1, 5):
            self.assertEqual(s[i], gf1[i])

    def testSubTwo(self):
        '''Test we can subtract two GFs.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([1, 2])

        s = gf1 - gf2
        self.assertEqual(s[0], 2)
        self.assertEqual(s[1], 0)
        self.assertEqual(s[2], 3)
        self.assertEqual(s[3], 0)
        self.assertEqual(s[4], 1)
        self.assertEqual(s[5], 0)

    def testSumProd(self):
        '''Test we can get sums in two ways.'''
        c = 2
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([c])

        p = gf1 * gf2
        s = gf1 + gf1
        for i in range(6):
            self.assertEqual(s[i], p[i])

    def testSumScale(self):
        '''Test we can scale a sum.'''
        c = 2
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        s = (gf1 + gf2) * c
        self.assertEqual(s[0], 3 * c)
        self.assertEqual(s[1], 4 * c)
        self.assertEqual(s[2], 3 * c)
        self.assertEqual(s[3], 0)
        self.assertEqual(s[4], c)
        self.assertEqual(s[5], 0)

    def testDiffSumOnce(self):
        '''Test we can differentiate a sum once.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        d = (gf1 + gf2).dx()
        self.assertEqual(d[0], 4)
        self.assertEqual(d[1], 6)
        self.assertEqual(d[2], 0)
        self.assertEqual(d[3], 4)
        self.assertEqual(d[4], 0)

    def testDiffSumTwice(self):
        '''Test we can differentiate a sum twice.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        d = (gf1 + gf2).dx(2)
        self.assertEqual(d[0], 6)
        self.assertEqual(d[1], 0)
        self.assertEqual(d[2], 12)
        self.assertEqual(d[3], 0)
        self.assertEqual(d[4], 0)

    def testDiffSumTwiceLinear(self):
        '''Test that differentiating a sum twice is linear..'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        d1 = (gf1 + gf2).dx(2)
        d2 = (gf1 + gf2).dx().dx()
        for i in range(5):
            self.assertEqual(d1[i], d2[i])

    def testDiffProdOnce(self):
        '''Test we can differentiate a product once.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        d = (gf1 * gf2).dx()
        self.assertEqual(d[0], 6)
        self.assertEqual(d[1], 8)
        self.assertEqual(d[2], 18)
        self.assertEqual(d[3], 0)
        self.assertEqual(d[4], 10)
        self.assertEqual(d[5], 0)

    def testDiffProdTwice(self):
        '''Test we can differentiate a product once.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        d = (gf1 * gf2).dx(2)
        self.assertEqual(d[0], 8)
        self.assertEqual(d[1], 36)
        self.assertEqual(d[2], 0)
        self.assertEqual(d[3], 40)
        self.assertEqual(d[4], 0)

    def testDiffProdTwiceLinear(self):
        '''Test differention of products is linear.'''
        gf1 = gf_from_coefficients([3, 2, 3, 0, 1])
        gf2 = gf_from_coefficients([0, 2])

        d1 = (gf1 * gf2).dx(2)
        d2 = (gf1 * gf2).dx().dx()
        for i in range(6):
            self.assertEqual(d1[i], d2[i])


if __name__ == '__main__':
    unittest.main()
