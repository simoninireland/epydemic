# Test the modular ER network generator
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

from epydemic import rng, ModularNetwork
from epyc import Experiment
import unittest
import networkx

class ModularTests(unittest.TestCase):

    def setUp(self):
        self._params = dict()
        self._params[ModularNetwork.N_core] = 1000
        self._params[ModularNetwork.PHI_core] = 0.01
        self._params[ModularNetwork.SATELLITES] = 4   # 1 core and 4 satellites
        self._params[ModularNetwork.N_sat] = 500
        self._params[ModularNetwork.PHI_sat] = 0.02

        self._gen = ModularNetwork(self._params)
        self._g = self._gen.generate()

    def testParameters(self):
        '''Check we generate the modules correctly.'''

        # check N and PHI for core
        core_ns = len([n for n in self._g.nodes() if self._g.nodes[n][ModularNetwork.ORIGIN] == 0])
        self.assertAlmostEqual(core_ns, self._params[ModularNetwork.N_core], delta=1)
        core_es = len([e for e in self._g.edges() if (self._g.nodes[e[0]][ModularNetwork.ORIGIN] == 0 and
                                                  self._g.nodes[e[1]][ModularNetwork.ORIGIN] == 0)])
        self.assertAlmostEqual(core_es / (core_ns * (core_ns - 1) / 2),
                               self._params[ModularNetwork.PHI_core], places=1)

        # check N and PHI for all satellites
        for i in range(1, self._params[ModularNetwork.SATELLITES] + 1):
            sat_ns = len([n for n in self._g.nodes() if self._g.nodes[n][ModularNetwork.ORIGIN] == i])
            self.assertAlmostEqual(sat_ns, self._params[ModularNetwork.N_sat], delta=1)
            sat_es = len([e for e in self._g.edges() if (self._g.nodes[e[0]][ModularNetwork.ORIGIN] == i and
                                                         self._g.nodes[e[1]][ModularNetwork.ORIGIN] == i)])
            self.assertAlmostEqual(sat_es / (sat_ns * (sat_ns - 1) / 2),
                               self._params[ModularNetwork.PHI_sat], places=1)

        # check there is exactly one edge from each satellite to the core,
        # and that the endpoints are correctly labelled
        for i in range(1, self._params[ModularNetwork.SATELLITES] + 1):
            core_sat_es = [e for e in self._g.edges() if ((self._g.nodes[e[0]][ModularNetwork.ORIGIN] == i and
                                                           self._g.nodes[e[1]][ModularNetwork.ORIGIN] == 0) or
                                                          (self._g.nodes[e[0]][ModularNetwork.ORIGIN] == 0 and
                                                           self._g.nodes[e[1]][ModularNetwork.ORIGIN] == i))]
            self.assertEqual(len(core_sat_es), 1)
            e = core_sat_es[0]
            self.assertTrue(self._g.nodes[e[0]][ModularNetwork.CORE_LINK])
            self.assertTrue(self._g.nodes[e[1]][ModularNetwork.CORE_LINK])

        # check all other nodes are correctly labelled
        ns = [n for n in self._g.nodes() if self._g.nodes[n][ModularNetwork.ORIGIN] == 0]
        self.assertEqual(len([n for n in ns if self._g.nodes[n][ModularNetwork.CORE_LINK]]),
                         self._params[ModularNetwork.SATELLITES])
        for i in range(1, self._params[ModularNetwork.SATELLITES] + 1):
            ns = [n for n in self._g.nodes() if self._g.nodes[n][ModularNetwork.ORIGIN] == i]
            self.assertEqual(len([n for n in ns if self._g.nodes[n][ModularNetwork.CORE_LINK]]),
                             1)

        # check that there are no edges between satellites
        for e in self._g.edges():
            self.assertTrue((self._g.nodes[e[0]][ModularNetwork.ORIGIN] == self._g.nodes[e[1]][ModularNetwork.ORIGIN]) or
                            (self._g.nodes[e[0]][ModularNetwork.ORIGIN] == 0 or
                             self._g.nodes[e[1]][ModularNetwork.ORIGIN] == 0))

    def testExtraction(self):
        '''Test we can extract the core and satellites.'''

        # core
        c = ModularNetwork.coreSubNetwork(self._g)
        self.assertEqual(self._params[ModularNetwork.N_core], c.order())
        core_es = [e for e in self._g.edges() if (self._g.nodes[e[0]][ModularNetwork.ORIGIN] == 0 and
                                                  self._g.nodes[e[1]][ModularNetwork.ORIGIN] == 0)]
        self.assertEqual(len(c.edges()), len(core_es))
        for e in c.edges():
            self.assertIn(e, core_es)

        # satellites
        for i in range(1, self._params[ModularNetwork.SATELLITES] + 1):
            p = ModularNetwork.satelliteSubNetwork(self._g, i)
            self.assertEqual(self._params[ModularNetwork.N_sat], p.order())
            per_es = [e for e in self._g.edges() if (self._g.nodes[e[0]][ModularNetwork.ORIGIN] == i and
                                                     self._g.nodes[e[1]][ModularNetwork.ORIGIN] == i)]
            self.assertEqual(len(p.edges()), len(per_es))
            for e in per_es:
                self.assertTrue(p.has_edge(e[0], e[1]))

            # test there is exactly one linked node
            self.assertEqual(len([n for n in p.nodes() if p.nodes[n][ModularNetwork.CORE_LINK]]), 1)


    def testFailExtraction(self):
        '''Test we spot the lack of structure markers on at least one node.'''

        # remove structure annotation from one random node
        n = rng.choice(list(self._g.nodes()))
        attr = self._g.nodes[n]
        del attr[ModularNetwork.ORIGIN]

        with self.assertRaises(ValueError):
            c = ModularNetwork.coreSubNetwork(self._g)

    def testFailWrongNetworkType(self):
        '''Test we fail when passed a non-modular network.'''
        g = networkx.fast_gnp_random_graph(500, 0.01)
        with self.assertRaises(ValueError):
            c = ModularNetwork.coreSubNetwork(g)


if __name__ == '__main__':
    unittest.main()
