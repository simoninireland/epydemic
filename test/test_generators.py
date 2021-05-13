# Test standard network generators
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

from epydemic import Process, Dynamics, StochasticDynamics, SIR, NetworkGenerator, FixedNetwork, ERNetwork, BANetwork, PLCNetwork
from epyc import Experiment
import unittest
import networkx

class GeneratorTest(unittest.TestCase):

    def assertGraphsEqual( self, g1, g2 ):
        '''Test two graphs for equality.
        sd: should check for attributes as well?

        :param g1: the first graph
        :param g2: the second graph'''
        g1ns = set(g1.nodes())
        g2ns = set(g2.nodes())
        self.assertCountEqual(g1ns, g2ns)
        g1es = set(g1.edges())
        g2es = set(g2.edges())
        self.assertCountEqual(g1es, g2es)


    def testFixedNetwork( self ):
        '''Test we always return a fixed network.'''
        g = networkx.diamond_graph()   # doesn't matter what it as, as long as it's fixed
        gen = FixedNetwork(g)

        self.assertGraphsEqual(g, gen.generate())

        for _ in range(5):   # make sure the iterator is stable
            gp = gen.__next__()
            self.assertGraphsEqual(g, gp)

    def testLimit(self):
        '''Test we can limit the number of instances generated.'''
        g = networkx.diamond_graph()
        gen = FixedNetwork(g, limit=10)

        n = 0
        for _ in gen:
            n += 1
        self.assertEqual(n, 10)

    def testFixedNetworkGenerator(self):
        '''Test that adding a network creates the right generator.'''
        g = networkx.diamond_graph()
        p = Process()
        dyn = Dynamics(p)

        dyn.setNetworkGenerator(g)
        self.assertIsInstance(dyn.networkGenerator(), FixedNetwork)
        self.assertGraphsEqual(g, dyn.networkGenerator().generate())

    def testER(self):
        '''Test we can generate ER networks with all parameter combinations.'''
        param = dict()
        param[ERNetwork.N] = 1000

        # test using <k>
        param[ERNetwork.KMEAN] = 20
        gen = ERNetwork(param)
        _ = gen.generate()

        # test using phi
        del param[ERNetwork.KMEAN]
        param[ERNetwork.PHI] = 0.02
        gen = ERNetwork(param)
        __= gen.generate()

        # test working with both
        param[ERNetwork.KMEAN] = 20
        gen = ERNetwork(param)
        _ = gen.generate()

        # test failing with neither
        del param[ERNetwork.KMEAN]
        del param[ERNetwork.PHI]
        gen = ERNetwork(param)
        with self.assertRaises(AttributeError):
            _ = gen.generate()

    def testBA(self):
        '''Test we can generate BA networks.'''
        param = dict()
        param[BANetwork.N] = 1000
        param[BANetwork.M] = 20
        gen = BANetwork(param)
        _ = gen.generate()

    def testPLC(self):
        '''Test we can  generate PLC networks.'''
        param = dict()
        param[PLCNetwork.N] = 1000
        param[PLCNetwork.EXPONENT] = 2
        param[PLCNetwork.CUTOFF] = 10
        gen = PLCNetwork(param)
        _ = gen.generate()

    def testTopologyMarker(self):
        '''Test we capture the topology of the network.'''
        param = dict()
        param[SIR.P_INFECT] = 0.1
        param[SIR.P_REMOVE] = 0.01
        param[SIR.P_INFECTED] = 0   # so no running time

        gen = FixedNetwork(networkx.gnp_random_graph(1000, 0.001))
        param_g = param.copy()
        e = StochasticDynamics(SIR(), gen)
        rc = e.set(param_g).run()
        ps = rc[Experiment.PARAMETERS]
        self.assertIn(NetworkGenerator.TOPOLOGY, ps)
        self.assertEqual(ps[NetworkGenerator.TOPOLOGY], gen.topology())

        gen = ERNetwork()
        param_er = param.copy()
        param_er[ERNetwork.N] = 1000
        param_er[ERNetwork.KMEAN] = 20
        e = StochasticDynamics(SIR(), gen)
        rc = e.set(param_er).run()
        ps = rc[Experiment.PARAMETERS]
        self.assertIn(NetworkGenerator.TOPOLOGY, ps)
        self.assertEqual(ps[NetworkGenerator.TOPOLOGY], gen.topology())

        gen = BANetwork()
        param_ba = param.copy()
        param_ba[BANetwork.N] = 1000
        param_ba[BANetwork.M] = 20
        e = StochasticDynamics(SIR(), gen)
        rc = e.set(param_ba).run()
        ps = rc[Experiment.PARAMETERS]
        self.assertIn(NetworkGenerator.TOPOLOGY, ps)
        self.assertEqual(ps[NetworkGenerator.TOPOLOGY], gen.topology())

        gen = PLCNetwork()
        param_plc = param.copy()
        param_plc[PLCNetwork.N] = 1000
        param_plc[PLCNetwork.EXPONENT] = 2
        param_plc[PLCNetwork.CUTOFF] = 5
        e = StochasticDynamics(SIR(), gen)
        rc = e.set(param_plc).run()
        ps = rc[Experiment.PARAMETERS]
        self.assertIn(NetworkGenerator.TOPOLOGY, ps)
        self.assertEqual(ps[NetworkGenerator.TOPOLOGY], gen.topology())

if __name__ == '__main__':
    unittest.main()
