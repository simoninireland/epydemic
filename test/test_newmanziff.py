# Test the Newman-Ziff percolation algorithms
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
from epyc import Experiment, Lab, RepeatedExperiment
import numpy
import unittest
from networkx import complete_graph, nodes

class SamplingBondPercolation(BondPercolation):
    '''Bond percolation that samples the number of edges in the working network.'''

    EDGES = 'edges'

    def sample(self, p):
        res = super().sample(p)
        res[self.EDGES] = len(self.network().edges)
        return res

class SamplingSitePercolation(SitePercolation):
    '''Site percolation that samples the number of nodes in the working network.'''

    NODES = 'nodes'

    def sample(self, p):
        res = super().sample(p)
        res[self.NODES] = self.network().order()
        return res


class NewmanZiffTest(unittest.TestCase):

    # ---------- Bond percolation ----------

    def testBondZero(self):
        '''Test we can do the basic bond percolation operations.'''
        g = complete_graph(5)
        e = BondPercolation(g)
        _ = e.run(fatal=True)

    def testBondTransition(self):
        '''Test the bond percolation transition on a PLC network.'''
        params = dict()
        params[PLCNetwork.N] = 1000
        params[PLCNetwork.EXPONENT] = 2.5
        params[PLCNetwork.CUTOFF] = 20
        e = BondPercolation(PLCNetwork())
        rc = e.set(params).run(fatal=True)

    def testResultLayout(self):
        '''Test the results land correctly in the notebook.'''
        lab = Lab()
        lab[PLCNetwork.N] = 1000
        lab[PLCNetwork.EXPONENT] = 2.5
        lab[PLCNetwork.CUTOFF] = 20
        e = BondPercolation(PLCNetwork(), samples=50)
        lab.runExperiment(e)
        df = lab.notebook().current().dataframe()
        self.assertEqual(len(df), 1)
        ps = df[BondPercolation.P][0]
        gccs = df[BondPercolation.GCC][0]
        self.assertEqual(len(ps), len(gccs))
        self.assertIn(0.0, ps)
        self.assertIn(1.0, ps)

    def testSamplePoints(self):
        '''Test we can set explicit sample points.'''
        lab = Lab()
        lab[PLCNetwork.N] = 1000
        lab[PLCNetwork.EXPONENT] = 2.5
        lab[PLCNetwork.CUTOFF] = 20
        samples = [0.0, 0.5, 1.0]
        e = BondPercolation(PLCNetwork(), samples=samples)
        lab.runExperiment(e)
        df = lab.notebook().current().dataframe()
        self.assertEqual(len(df), 1)
        ps = df[BondPercolation.P][0]
        gccs = df[BondPercolation.GCC][0]
        self.assertEqual(len(ps), len(gccs))
        self.assertEqual(len(gccs), 3)
        self.assertEqual(ps[0], 0.0)
        self.assertAlmostEqual(ps[1], 0.5, places=2)
        self.assertEqual(ps[2], 1.0)

    def testRepeats(self):
        '''Test we play well with repeated experiments.'''
        lab = Lab()
        lab[PLCNetwork.N] = 1000
        lab[PLCNetwork.EXPONENT] = 2.5
        lab[PLCNetwork.CUTOFF] = 20
        e = BondPercolation(PLCNetwork(), samples=10)
        lab.runExperiment(RepeatedExperiment(e, 3))
        df = lab.notebook().current().dataframe()
        self.assertEqual(len(df), 3)
        for i in range(len(df)):
            r = df.iloc[i]
            ps = r[BondPercolation.P]
            self.assertEqual(len(ps), 10)

    def testBondsGrowingWorkingNetwork(self):
        '''Test that the working network grows as we bond percolate.'''
        params = dict()
        params[PLCNetwork.N] = 1000
        params[PLCNetwork.EXPONENT] = 2.5
        params[PLCNetwork.CUTOFF] = 20
        g = PLCNetwork()._generate(params)
        e = SamplingBondPercolation(g, samples=100)
        rc = e.run()
        edges = rc[Experiment.RESULTS][SamplingBondPercolation.EDGES]

        # occupied edge set grows monotonically
        self.assertEqual(edges[0], 0)
        self.assertEqual(edges[-1], len(g.edges))
        for i in range(len(edges) - 1):
            self.assertTrue(edges[i] <  edges[i + 1])

        # at the end we have all the edges again
        self.assertSetEqual(set(g.edges), set(e.network().edges))


   # ---------- Site percolation ----------

    def testSiteZero(self):
        '''Test we can do the basic site percolation operations.'''
        g = complete_graph(5)
        e = SitePercolation(g)
        _ = e.run(fatal=True)

    def testSiteTransition(self):
        '''Test the site percolation transition on a PLC network.'''
        params = dict()
        params[PLCNetwork.N] = 1000
        params[PLCNetwork.EXPONENT] = 2.5
        params[PLCNetwork.CUTOFF] = 20
        e = SitePercolation(PLCNetwork())
        rc = e.set(params).run(fatal=True)

    def testSitesGrowingWorkingNetwork(self):
        '''Test that the working network grows as we site percolate.'''
        params = dict()
        params[PLCNetwork.N] = 1000
        params[PLCNetwork.EXPONENT] = 2.5
        params[PLCNetwork.CUTOFF] = 20
        g = PLCNetwork()._generate(params)
        e = SamplingSitePercolation(g, samples=100)
        rc = e.run()
        nodes = rc[Experiment.RESULTS][SamplingSitePercolation.NODES]

        # occupied node set grows monotonically
        self.assertEqual(nodes[0], 0)
        self.assertEqual(nodes[-1], g.order())
        for i in range(len(nodes) - 1):
            self.assertTrue(nodes[i] <  nodes[i + 1])

        # at the end we have the network we started with (nodes and edges)
        self.assertEqual(g.order(), e.network().order())
        self.assertSetEqual(set(g.nodes), set(e.network().nodes))
        self.assertEqual(len(g.edges), len(e.network().edges))
        # (we don't guarantee edge direction is maintained,
        # so the simple way with sets doesn't work)
        #self.assertSetEqual(set(e.network().edges), set(g.edges))
        for (n, m) in e.network().edges:
            self.assertTrue((n, m) in g.edges or (m, n) in g.edges)



if __name__ == '__main__':
    unittest.main()
