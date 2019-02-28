# Test the functioning of thew various loci classes
#
# Copyright (C) 2017--2019 Simon Dobson
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

from __future__ import print_function
from epydemic import *
import unittest
import six
import networkx


class LociTest(unittest.TestCase):

    def setUp(self):
        self._g = networkx.Graph()

    def testLocus(self):
        '''Test the standard locus initialisation.'''
        l = Locus('test locus')
        self.assertEqual(l.name(), 'test locus')
        self.assertEqual(len(l), 0)

    def testSingleton(self):
        '''Test that singleton loci behave as expected.'''
        l = Singleton('singleton')
        self.assertEqual(l.name(), 'singleton')
        self.assertEqual(len(l.elements()), 1)
        six.assertCountEqual(self, l.elements(), [ None ])
        self.assertEqual(l.draw(), None)

    def testAlNodes(self):
        '''Test that we capture all the nodes in an underlying network.'''
        l = AllNodes('allnodes', self._g)
        self.assertEqual(l.name(), 'allnodes')
        self.assertEqual(len(l), 0)

        ns = [ 1, 2, 3 ]
        self._g.add_nodes_from(ns)
        self.assertEqual(len(l), len(ns))
        six.assertCountEqual(self, l.elements(), ns)

        self._g.remove_node(ns[0])
        self.assertEqual(len(l), len(ns) - 1)
        six.assertCountEqual(self, l.elements(), ns[1:])


    def testAllEdges(self):
        '''Test that we capture all the edges in an underlying network.'''
        l = AllEdges('alledges', self._g)
        self.assertEqual(l.name(), 'alledges')
        self.assertEqual(len(l), 0)

        ns = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
        self._g.add_nodes_from(ns)
        es = []
        for i in range(len(ns) - 1):
            es.append((ns[i], ns [i + 1]))
        es.append((ns[-1], ns[0]))
        self._g.add_edges_from(es)
        self.assertEqual(len(l), len(es))
        for e in es:     # can't use six.assertCountEqual as networkx doesn't maintain edge orientation
            self.assertTrue(e in l.elements())

        self._g.remove_edge(*es[0])
        self.assertEqual(len(l), len(es) - 1)
        for e in es[1:]:
            self.assertTrue(e in l.elements())
