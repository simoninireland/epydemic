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
from epyc import Lab, RepeatedExperiment
import numpy
import unittest
from networkx import complete_graph

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
        self.assertEqual(len(df), 50)
        self.assertIn(0.0, df[BondPercolation.P])
        self.assertIn(1.0, df[BondPercolation.P])

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
        self.assertEqual(len(df), 3)
        points = sorted(list(df[BondPercolation.P]))
        self.assertEqual(points[0], 0.0)
        self.assertAlmostEqual(points[1], 0.5, places=2)
        self.assertEqual(points[2], 1.0)

    def testRepeats(self):
        '''Test we play well with repeated experiments.'''
        lab = Lab()
        lab[PLCNetwork.N] = 1000
        lab[PLCNetwork.EXPONENT] = 2.5
        lab[PLCNetwork.CUTOFF] = 20
        e = BondPercolation(PLCNetwork(), samples=10)
        lab.runExperiment(RepeatedExperiment(e, 3))
        df = lab.notebook().current().dataframe()
        self.assertEqual(len(df), 3 * 10)
        for p in df[BondPercolation.P]:
            self.assertEqual(len(df[df[BondPercolation.P] == p]), 3)


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
        #print(rc)


if __name__ == '__main__':
    unittest.main()
