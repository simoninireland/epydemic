# Test basic process functions
#
# Copyright (C) 2020 Simon Dobson
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
import unittest
import networkx

class ProcessTest(unittest.TestCase):

    def setUp(self):
        self._g = networkx.Graph()
        self._p = Process()
        self._dyn = Dynamics(self._p)
        self._p.reset()
        self._p.setNetwork(self._g)
        self._p.build(dict())
        self._p.setUp(dict())

    def testAddNode(self):
        '''Test all node addition methods pass-though correctly.'''

        # test single addition
        self._p.addNode(1)
        self.assertCountEqual(self._g.nodes(), [ 1 ])

        # test bulk addition
        self._p.addNodesFrom([ 2, 3, 4 ])
        self.assertCountEqual(self._g.nodes(), [ 1, 2, 3, 4 ])

        # test repeated addiion does nothing
        self._p.addNode(1)
        self.assertCountEqual(self._g.nodes(), [ 1, 2, 3, 4 ])

        # test attributes are stored correctly
        self._p.addNode(5, test=1)
        self.assertCountEqual(self._g.nodes(), [ 1, 2, 3, 4, 5 ])
        self.assertEqual(self._g.nodes[5]['test'], 1)
        self._p.addNodesFrom([ 6, 7 ], test=5)
        self.assertEqual(self._g.nodes[6]['test'], 5)
        self.assertEqual(self._g.nodes[7]['test'], 5)

    def testAddEdge(self):
        '''Test all the ewdge addition methods pass-through correctly.'''
        self._p.addNodesFrom([ 1, 2, 3, 4, 5 ])

        # test single addition
        self._p.addEdge(1, 2)
        self.assertCountEqual(self._g.edges(), [ (1, 2) ])

        # test bulk addition
        self._p.addEdgesFrom([ (1, 3), (3, 4), (4, 5) ])
        self.assertCountEqual(self._g.edges(), [ (1, 2), (1, 3), (3, 4), (4, 5) ])

        # test repeated addition does nothing
        self._p.addEdge(1, 2)
        self.assertCountEqual(self._g.edges(), [ (1, 2), (1, 3), (3, 4), (4, 5) ])

        # test attributes are stored correctly
        self._p.addEdge(1, 5, test=1)
        self.assertCountEqual(self._g.edges(), [ (1, 5), (1, 2), (1, 3), (3, 4), (4, 5) ])
        self.assertEqual(self._g.edges[1, 5]['test'], 1)
        self._p.addEdgesFrom([ (2, 5), (3, 5) ], test=5)
        self.assertEqual(self._g.edges[2, 5]['test'], 5)
        self.assertEqual(self._g.edges[3, 5]['test'], 5)

        # test adding an edge with a missing endpoint fails
        with self.assertRaises(Exception):
            self._p.addEdge(1, 7)
        with self.assertRaises(Exception):
            self._p.addEdge(7, 1)

    def testInstanceIds(self):
        '''Test instances ids are unique.'''
        p1 = Process()
        p2 = Process()
        self.assertNotEqual(p1.instanceId(), p2.instanceId())

    def testRunIds(self):
        '''Test that two runs of the same process have different run ids.'''
        p = Process()
        g = networkx.fast_gnp_random_graph(10000, 0.001)
        e = StochasticDynamics(p, g)

        rc1 = e.run(fatal=True)
        r1 = p.runId()
        rc2 = e.run(fatal=True)
        r2 = p.runId()
        self.assertNotEqual(r1, r2)


if __name__ == '__main__':
    unittest.main()
