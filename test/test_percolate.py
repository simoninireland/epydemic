# Test percolation process
#
# Copyright (C) 2017--2020 Simon Dobson
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
import networkx
import numpy
import unittest

class CaptureNetwork(StochasticDynamics):
    '''Class that captures the network after running,
    to make tests simpler.'''

    def __init__(self, p, g):
        super().__init__(p, g)

    def tearDown(self):
        ''' Store the resulting network after running.'''
        self._residual = self.network()
        super().tearDown()


class PercolationTest(unittest.TestCase):

    def testProduceER(self):
        '''Test that a percolation process on a complete network creates an ER network.'''
        N = 2000
        kmean = 15
        phi =  kmean / N

        # create and percolate the complete graph
        g = networkx.complete_graph(N)
        params = dict()
        params[Percolate.T] = phi
        p = Percolate()
        e = CaptureNetwork(p, g)
        _ = e.set(params).run()

        # check the topology of the resulting network
        rg = e._residual
        self.assertEqual(rg.order(), g.order())
        rg_kmean = numpy.mean(list(map(lambda nd: nd[1], list(rg.degree()))))
        self.assertAlmostEqual(rg_kmean, kmean, places=0)   # sd: this isn't a fine enough equality


if __name__ == '__main__':
    unittest.main()
