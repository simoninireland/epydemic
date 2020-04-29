# Test compartmented model basic functions
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

from epydemic import *
import unittest
import networkx
import six

class CompartmentedModelTest(unittest.TestCase):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        self._er = networkx.erdos_renyi_graph(1000, 0.005)
        self._params = dict()
        self._params[SIR.P_INFECT] = 0.1
        self._params[SIR.P_INFECTED] = 0.01
        self._params[SIR.P_REMOVE] = 0.05
       
    def testPopulation( self ):
        '''Test populating a model.'''
        e = StochasticDynamics(SIR(), self._er)
        e.setUp(self._params)

    def testDuplicateNodeLocus( self ):
        '''Test we can't duplicate node-loci names'''
        m = SIR()
        params = dict()
        params[SIR.P_INFECT] = 0.1
        params[SIR.P_INFECTED] = 1.0    # infect all nodes initially
        params[SIR.P_REMOVE] = 0.05
        m.build(params)
        with self.assertRaises(Exception):
            m.trackNodesInCompartment(SIR.INFECTED)      # part of SIR already

    def testDuplicateEdgeLocus( self ):
        '''Test we can't duplicate edge-loci names'''
        m = SIR()
        params = dict()
        params[SIR.P_INFECT] = 0.1
        params[SIR.P_INFECTED] =  1.0    # infect all nodes initially
        params[SIR.P_REMOVE] = 0.05
        m.build(params)
        with self.assertRaises(Exception):
            m.trackEdgesBetweenCompartments(SIR.SUSCEPTIBLE, SIR.INFECTED, name = SIR.SI)      # part of SIR already

    def testLocusNames(self):
        '''Test that a locus gets an automatic name.'''
        m = SIR()

        # add new loci
        m.trackNodesInCompartment(SIR.REMOVED)
        self.assertIn(SIR.REMOVED, m._loci.keys())
        m.trackEdgesBetweenCompartments(SIR.REMOVED, SIR.SUSCEPTIBLE)
        self.assertIn("{l}-{r}".format(l = SIR.REMOVED, r = SIR.SUSCEPTIBLE), m._loci.keys())

    def testLoci( self ):
        '''Test we can populate loci correctly.'''
        g = networkx.Graph()
        g.add_edges_from([(1, 2), (2, 3), (1, 4), (3, 4)])
        m = SIR()
        e = StochasticDynamics(m, g)
        params = dict()
        params[SIR.P_INFECT] = 0.1
        params[SIR.P_INFECTED] =  1.0    # infect all nodes initially
        params[SIR.P_REMOVE] = 0.05
        e.setUp(params)

        # keep track of the other compartments as well
        m.trackNodesInCompartment(SIR.SUSCEPTIBLE)
        m.trackNodesInCompartment(SIR.REMOVED)
        
        # all nodes in I
        six.assertCountEqual(self, m._loci[SIR.INFECTED].elements(), [1, 2, 3, 4])

        # one node from I into S, two edges into SI
        m.changeCompartment(1, SIR.SUSCEPTIBLE)
        six.assertCountEqual(self, m._loci[SIR.INFECTED].elements(), [2, 3, 4])
        six.assertCountEqual(self, m._loci[SIR.SUSCEPTIBLE].elements(), [1])
        six.assertCountEqual(self, m._loci[SIR.SI].elements(), [(1, 2), (1, 4)])

        # recover the infected node
        m.changeCompartment(1, SIR.REMOVED)
        six.assertCountEqual(self, m._loci[SIR.INFECTED].elements(), [2, 3, 4])
        six.assertCountEqual(self, m._loci[SIR.SUSCEPTIBLE].elements(), [])
        six.assertCountEqual(self, m._loci[SIR.REMOVED].elements(), [1])
        six.assertCountEqual(self, m._loci[SIR.SI].elements(), [])

    def testSkeletonise( self ):
        '''Test that a network skeletonises correctly'''
        m = SIR()
        g = networkx.Graph()
        m.setNetwork(g)
        g.add_edges_from([ (1, 2), (2, 3), (1, 4), (3, 4) ])

        # mark some edges as occupied
        m.markOccupied((1, 2), 0)
        m.markOccupied((1, 4), 0)

        # check skeletonisation
        g2 = m.skeletonise()
        six.assertCountEqual(self, g2.edges(), [(1, 2), (1, 4)])
        six.assertCountEqual(self, g2.nodes(), [ 1, 2, 3, 4])

    def testAddNode(self):
        '''Test that a node can be added and land in the right compartment.'''
        m = SIR()
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)

        m.addNode(1, c = SIR.INFECTED)
        six.assertCountEqual(self, m.compartment(SIR.INFECTED), [1])

        m.addNode(2, c = SIR.INFECTED, h = "test")
        six.assertCountEqual(self, m.compartment(SIR.INFECTED), [1, 2])
        self.assertEqual(g.nodes[2]['h'], "test")

    def testAddNodes(self):
        '''Test that nodes can be added and land in the right compartment.'''
        m = SIR()
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)

        ns = [1,2,3]
        m.addNodesFrom(ns, c = SIR.INFECTED, h = 'test')
        six.assertCountEqual(self, m.compartment(SIR.INFECTED), ns)
        for n in ns:
            self.assertEqual(g.nodes[n]['h'], "test")

    def testRemoveNode(self):
        '''Test that a node can be removed.'''
        m = SIR()
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)

        m.addNode(1, c = SIR.INFECTED)
        six.assertCountEqual(self, m.compartment(SIR.INFECTED), [1])
        m.removeNode(1)
        six.assertCountEqual(self, m.compartment(SIR.INFECTED), [])

    def testAddEdge(self):
        '''Test we can add an edge, keeping all the data straight.'''
        m = SIR()
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)
        m.trackEdgesBetweenCompartments(SIR.INFECTED, SIR.SUSCEPTIBLE, name = SIR.SI)

        m.addNode(1, c = SIR.INFECTED)
        m.addNode(2, c = SIR.SUSCEPTIBLE)
        six.assertCountEqual(self, m.compartment(SIR.INFECTED), [1])
        six.assertCountEqual(self, m.compartment(SIR.SUSCEPTIBLE), [2])
        m.addEdge(1, 2)
        self.assertEqual(len(m[SIR.SI]), 1)

    def testRemoveEdge(self):
        '''Test we can remove an edge, keeping all the data straight.'''
        m = SIR()
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)
        m.trackEdgesBetweenCompartments(SIR.INFECTED, SIR.SUSCEPTIBLE, name = SIR.SI)

        m.addNode(1, c = SIR.INFECTED)
        m.addNode(2, c = SIR.SUSCEPTIBLE)
        m.addNode(3, c = SIR.SUSCEPTIBLE)
        m.addEdge(1, 2)
        m.addEdge(1, 3)
        m.addEdge(3, 2)
        self.assertEqual(len(m[SIR.SI]), 2)
        m.removeEdge(1, 2)
        self.assertEqual(len(m[SIR.SI]), 1)
        print(list(g.edges()))
        m.removeEdge(2, 3)
        print(list(g.edges()))
        self.assertEqual(len(m[SIR.SI]), 1)

if __name__ == '__main__':
    unittest.main()
