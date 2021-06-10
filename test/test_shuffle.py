# Test the behaviour of the edge-rewiring process
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
import epyc
import unittest
import networkx

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


class ShuffleTest(unittest.TestCase):

    def testPreserve(self):
        '''Test that shuffling preserves degree.'''
        g = networkx.fast_gnp_random_graph(5000, 0.005)
        g_orig = g.copy()

        params = dict()
        params[ShuffleK.REWIRE_FRACTION] = 0.5
        c = CaptureNetwork()
        e = StochasticDynamics(ProcessSequence([ShuffleK(), c]), g)
        rc = e.set(params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc)

        g = c.finalNetwork()
        for n in g.nodes():
            self.assertEqual(g.degree(n), g_orig.degree(n))

    def testReduceClustering(self):
        '''Test that shuffling reduces clustrering.'''
        deg = [(1, 0), (1, 0), (1, 0), (2, 0), (1, 0), (2, 1), (0, 1), (0, 1)]
        g = networkx.random_clustered_graph(deg, create_using=networkx.Graph)
        kbefore = networkx.average_clustering(g)

        params = dict()
        params[ShuffleK.REWIRE_FRACTION] = 0.1
        c = CaptureNetwork()
        e = StochasticDynamics(ProcessSequence([ShuffleK(), c]), g)
        rc = e.set(params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc)

        kafter = networkx.average_clustering(c.finalNetwork())
        self.assertTrue(kbefore >= kafter)


if __name__ == '__main__':
    unittest.main()
