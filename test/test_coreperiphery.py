# Test the core-periphery network generator
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

from epydemic import rng, CorePeripheryNetwork
from epyc import Experiment
import unittest
import networkx

class CorePeripheryTests(unittest.TestCase):

    def setUp(self):
        self._params = dict()
        self._params[CorePeripheryNetwork.N_core] = 1000
        self._params[CorePeripheryNetwork.PHI_core] = 0.01
        self._params[CorePeripheryNetwork.N_per] = 1000
        self._params[CorePeripheryNetwork.PHI_per] = 0.005

        self._gen = CorePeripheryNetwork(self._params)
        self._g = self._gen.generate()

    def testParameters(self):
        '''Check we generate core and periphery correctly.'''

        # check N and PHI for core
        core_ns = len([n for n in self._g.nodes() if self._g.nodes[n][CorePeripheryNetwork.ORIGIN] == 0])
        self.assertAlmostEqual(core_ns, self._params[CorePeripheryNetwork.N_core], delta=1)
        core_es = len([e for e in self._g.edges() if (self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] == 0 and
                                                  self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN] == 0)])
        self.assertAlmostEqual(core_es / (core_ns * (core_ns - 1) / 2),
                               self._params[CorePeripheryNetwork.PHI_core], places=1)

        # check N and PHI for periphery
        per_ns = len([n for n in self._g.nodes() if self._g.nodes[n][CorePeripheryNetwork.ORIGIN] == 1])
        self.assertAlmostEqual(per_ns, self._params[CorePeripheryNetwork.N_per], delta=1)
        per_es = len([e for e in self._g.edges() if (self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] == 1 and
                                                  self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN] == 1)])
        self.assertAlmostEqual(per_es / (per_ns * (per_ns - 1) / 2),
                               self._params[CorePeripheryNetwork.PHI_per], places=1)

        # check density between core and periphery is that of periphery
        link_es = len([e for e in self._g.edges() if self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] != self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN]])
        self.assertAlmostEqual(link_es / ((core_ns + per_ns) * ((core_ns + per_ns) - 1) / 2),
                               self._params[CorePeripheryNetwork.PHI_per], places=1)

    def testExtraction(self):
        '''Test we can extract the core and periphery.'''

        # core
        c = CorePeripheryNetwork.coreSubNetwork(self._g)
        self.assertEqual(self._params[CorePeripheryNetwork.N_core], c.order())
        core_es = [e for e in self._g.edges() if (self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] == 0 and
                                                  self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN] == 0)]
        self.assertEqual(len(c.edges()), len(core_es))
        for e in c.edges():
            self.assertIn(e, core_es)

        # periphery
        p = CorePeripheryNetwork.peripherySubNetwork(self._g)
        self.assertEqual(self._params[CorePeripheryNetwork.N_per], p.order())
        per_es = [e for e in self._g.edges() if (self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] == 1 and
                                                 self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN] == 1)]
        self.assertEqual(len(p.edges()), len(per_es))
        for e in per_es:
            self.assertTrue(p.has_edge(e[0], e[1]))

    def testFailExtraction(self):
        '''Test we spot the lack of structure markers on at least one node.'''

        # remove structure annotation from one random node
        n = rng.choice(list(self._g.nodes()))
        attr = self._g.nodes[n]
        del attr[CorePeripheryNetwork.ORIGIN]

        with self.assertRaises(ValueError):
            c = CorePeripheryNetwork.coreSubNetwork(self._g)

    def testFailWrongNetworkType(self):
        '''Test we fail when passed a non-ore-periphery network.'''
        g = networkx.fast_gnp_random_graph(500, 0.01)
        with self.assertRaises(ValueError):
            c = CorePeripheryNetwork.coreSubNetwork(g)


if __name__ == '__main__':
    unittest.main()
