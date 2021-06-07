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

from epydemic.gf import *
import unittest
import networkx


class GFTest(unittest.TestCase):

    def testDiscreteProbabilities(self):
        '''Test that the coefficients of a discrete GF sum to 1.'''
        g = networkx.gnp_random_graph(1000, 0.005)
        gf = DiscreteGF(network=g)
        self.assertAlmostEqual(gf(1.0), 1.0, places=1)

    def testDiscreteHistogram(self):
        '''Test we get the coefficients matching the histogram.'''
        g = networkx.gnp_random_graph(5000, 0.005)

        # check coefficient for degree 4 matches the network
        ns = []
        for n in g.nodes:
            if len(list(g.neighbors(n))) == 4:
                ns.append(n)
        gf = DiscreteGF(network=g)
        N = g.order()
        self.assertAlmostEqual(gf[4], len(ns) / N, places=1)

        # delete all nodes of degree 8 or less
        ns = []
        for n in g.nodes:
            if len(list(g.neighbors(n))) <= 8:
                ns.append(n)
        g.remove_nodes_from(ns)
        gf = DiscreteGF(network=g)
        for k in range(9):
            self.assertEqual(gf[k], 0)


if __name__ == '__main__':
    unittest.main()
