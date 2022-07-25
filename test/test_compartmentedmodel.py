# Test compartmented model basic functions
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
import unittest
import networkx

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

    def testInitialPopulation(self):
        '''Test that initial seeding of compartments works properly.'''
        self._er = networkx.gnp_random_graph(10000, 0.001)   # larger network to reduce variance
        m = SIR()
        e = StochasticDynamics(m)
        m.reset()
        m.setNetwork(self._er)
        m.build(self._params)
        m.setUp(self._params)
        self.assertAlmostEqual(len(m.compartment(SIR.INFECTED)) / self._er.order(), self._params[SIR.P_INFECTED], places=2)
        self.assertAlmostEqual(len(m.compartment(SIR.SUSCEPTIBLE)) / self._er.order(), (1.0 - self._params[SIR.P_INFECTED]), places=2)

    def testChangeInitialPopulation(self):
        '''Test that changing the initial seeding works.'''
        self._er = networkx.gnp_random_graph(10000, 0.001)   # larger network to reduce variance
        m = SIR()
        e = StochasticDynamics(m)
        m.reset()
        m.setNetwork(self._er)
        m.build(self._params)
        pInfected = 0.1       # new infection seed
        m.changeCompartmentInitialOccupancy(SIR.INFECTED, pInfected)
        m.changeCompartmentInitialOccupancy(SIR.SUSCEPTIBLE, 1.0 - pInfected)
        m.setUp(self._params)
        self.assertAlmostEqual(len(m.compartment(SIR.INFECTED)) / self._er.order(), pInfected, places=1)
        self.assertAlmostEqual(len(m.compartment(SIR.SUSCEPTIBLE)) / self._er.order(), (1.0 - pInfected), places=1)

    def testMissingCompartment(self):
        '''Test we catch missing compartments when changing initial occupancy.'''
        m = SIR()
        e = StochasticDynamics(m)
        m.reset()
        m.setNetwork(self._er)
        m.build(self._params)
        with self.assertRaises(Exception):
            m.changeCompartmentInitialOccupancy('missing', 1.0)

    def testSanityCheckDistribution(self):
        '''Check that we detect a bad distribution in initial comaprtment occupancy.'''
        m = SIR()
        e = StochasticDynamics(m)
        m.reset()
        m.setNetwork(self._er)
        m.build(self._params)
        pInfected = 0.1       # new infection seed
        m.changeCompartmentInitialOccupancy(SIR.INFECTED, pInfected)
        # don't update other compartment's probability to compensate
        with self.assertRaises(Exception):
            m.setUp(self._params)

    def testDuplicateNodeLocus( self ):
        '''Test we can't duplicate node-loci names'''
        m = SIR()
        e = StochasticDynamics(m)
        self._params[SIR.P_INFECTED] = 1.0    # infect all nodes initially
        m.reset()
        m.build(self._params)
        with self.assertRaises(Exception):
            m.trackNodesInCompartment(SIR.INFECTED)      # part of SIR already

    def testDuplicateEdgeLocus( self ):
        '''Test we can't duplicate edge-loci names'''
        m = SIR()
        e = StochasticDynamics(m)
        self._params[SIR.P_INFECTED] =  1.0    # infect all nodes initially
        m.reset()
        m.build(self._params)
        with self.assertRaises(Exception):
            m.trackEdgesBetweenCompartments(SIR.SUSCEPTIBLE, SIR.INFECTED, name = SIR.SI)      # part of SIR already

    def testLocusNames(self):
        '''Test that a locus gets an automatic name.'''
        m = SIR()
        e = StochasticDynamics(m)
        m.setDynamics(e)
        m.trackNodesInCompartment(SIR.REMOVED)
        self.assertIn(SIR.REMOVED, m.loci().keys())
        m.trackEdgesBetweenCompartments(SIR.REMOVED, SIR.SUSCEPTIBLE)
        self.assertIn("{l}-{r}".format(l = SIR.REMOVED, r = SIR.SUSCEPTIBLE), m.loci().keys())

    def testLoci( self ):
        '''Test we can populate loci correctly.'''
        g = networkx.Graph()
        g.add_edges_from([(1, 2), (2, 3), (1, 4), (3, 4)])
        m = SIR()
        e = StochasticDynamics(m, g)
        self._params[SIR.P_INFECTED] =  1.0    # infect all nodes initially
        e.setUp(self._params)

        # keep track of the other compartments as well
        m.trackNodesInCompartment(SIR.SUSCEPTIBLE)
        m.trackNodesInCompartment(SIR.REMOVED)

        # all nodes in I
        self.assertCountEqual(m.loci()[SIR.INFECTED], [1, 2, 3, 4])

        # one node from I into S, two edges into SI
        m.changeCompartment(1, SIR.SUSCEPTIBLE)
        self.assertCountEqual(m.loci()[SIR.INFECTED], [2, 3, 4])
        self.assertCountEqual(m.loci()[SIR.SUSCEPTIBLE], [1])
        self.assertCountEqual(m.loci()[SIR.SI], [(1, 2), (1, 4)])

        # recover the infected node
        m.changeCompartment(1, SIR.REMOVED)
        self.assertCountEqual(m.loci()[SIR.INFECTED], [2, 3, 4])
        self.assertCountEqual(m.loci()[SIR.SUSCEPTIBLE], [])
        self.assertCountEqual(m.loci()[SIR.REMOVED], [1])
        self.assertCountEqual(m.loci()[SIR.SI], [])

    def testSkeletonise( self ):
        '''Test that a network skeletonises correctly'''
        m = SIR()
        g = networkx.Graph()
        g.add_edges_from([ (1, 2), (2, 3), (1, 4), (3, 4) ])
        e = StochasticDynamics(m, g)
        m.setNetwork(g)

        # mark some edges as occupied
        m.markOccupied((1, 2), 0)
        m.markOccupied((1, 4), 0)

        # check skeletonisation
        g2 = m.skeletonise()
        self.assertCountEqual(g2.edges(), [(1, 2), (1, 4)])
        self.assertCountEqual(g2.nodes(), [ 1, 2, 3, 4])

    def testAddNode(self):
        '''Test that a node can be added and land in the right compartment.'''
        m = SIR()
        e = StochasticDynamics(m)
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)

        m.addNode(1, c = SIR.INFECTED)
        self.assertCountEqual(m.compartment(SIR.INFECTED), [1])

        m.addNode(2, c = SIR.INFECTED, h = "test")
        self.assertCountEqual(m.compartment(SIR.INFECTED), [1, 2])
        self.assertEqual(g.nodes[2]['h'], "test")

    def testAddNodes(self):
        '''Test that nodes can be added and land in the right compartment.'''
        m = SIR()
        e = StochasticDynamics(m)
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)

        ns = [1,2,3]
        m.addNodesFrom(ns, c = SIR.INFECTED, h = 'test')
        self.assertCountEqual(m.compartment(SIR.INFECTED), ns)
        for n in ns:
            self.assertEqual(g.nodes[n]['h'], "test")

    def testRemoveNode(self):
        '''Test that a node can be removed.'''
        m = SIR()
        e = StochasticDynamics(m)
        g = networkx.Graph()
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)

        m.addNode(1, c = SIR.INFECTED)
        self.assertCountEqual(m.compartment(SIR.INFECTED), [1])
        m.removeNode(1)
        self.assertCountEqual(m.compartment(SIR.INFECTED), [])

    def testAddEdge(self):
        '''Test we can add an edge, keeping all the data straight.'''
        m = SIR()
        g = networkx.Graph()
        e = StochasticDynamics(m, g)
        m.setNetwork(g)
        m.addCompartment(SIR.SUSCEPTIBLE)
        m.addCompartment(SIR.INFECTED)
        m.addCompartment(SIR.REMOVED)
        m.trackEdgesBetweenCompartments(SIR.INFECTED, SIR.SUSCEPTIBLE, name = SIR.SI)

        m.addNode(1, c = SIR.INFECTED)
        m.addNode(2, c = SIR.SUSCEPTIBLE)
        self.assertCountEqual(m.compartment(SIR.INFECTED), [1])
        self.assertCountEqual(m.compartment(SIR.SUSCEPTIBLE), [2])
        m.addEdge(1, 2)
        self.assertEqual(len(m.loci()[SIR.SI]), 1)

        # add an edge with sense reversed
        m.addNode(3, c = SIR.SUSCEPTIBLE)
        m.addEdge(3, 1)
        self.assertEqual(len(m.loci()[SIR.SI]), 2)

    def testRemoveEdge(self):
        '''Test we can remove an edge, keeping all the data straight.'''
        m = SIR()
        e = StochasticDynamics(m)
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
        self.assertEqual(len(m.loci()[SIR.SI]), 2)
        m.removeEdge(1, 2)
        self.assertEqual(len(m.loci()[SIR.SI]), 1)
        #print(list(g.edges()))
        m.removeEdge(2, 3)
        #print(list(g.edges()))
        self.assertEqual(len(m.loci()[SIR.SI]), 1)

        # remove edge with the oppposite sense
        m.removeEdge(3, 1)
        #print(list(g.edges()))
        self.assertEqual(len(m.loci()[SIR.SI]), 0)

if __name__ == '__main__':
    unittest.main()
