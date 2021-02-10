# Test processes compose into sequences
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
from epyc import Experiment
import unittest
import networkx

class ProcessSequenceTest(unittest.TestCase):

    def testOneSequence(self):
        '''Test we can create a one-process sequence.'''
        params = dict()
        params[ERNetwork.N] = 1000
        params[ERNetwork.KMEAN] = 5
        params[SIR.P_INFECT] = 0.2
        params[SIR.P_REMOVE] = 0.2
        params[SIR.P_INFECTED] = 0.01

        # run as indiviaul process
        e = StochasticDynamics(SIR(), ERNetwork())
        rc1 = e.set(params).run()

        # run as single-process sequence
        p = ProcessSequence([SIR()])
        e = StochasticDynamics(p, ERNetwork())
        rc2 = e.set(params).run()

        self.assertAlmostEqual(rc1[Experiment.RESULTS][SIR.REMOVED], rc2[Experiment.RESULTS][SIR.REMOVED], delta=100)

    def testTwoSequence(self):
        '''Test we can cascade two processes.'''
        params = dict()
        params[ERNetwork.N] = 1000
        params[ERNetwork.KMEAN] = 5
        params[SIR.P_INFECT] = 0.2
        params[SIR.P_REMOVE] = 0.2
        params[SIR.P_INFECTED] = 0.01

        # run the two processes
        p = ProcessSequence([SIR(), NetworkStatistics()])
        e = StochasticDynamics(p, ERNetwork())
        rc1 = e.set(params).run()

        # check we get results from both
        self.assertIn(SIR.REMOVED, rc1[Experiment.RESULTS])
        self.assertIn(NetworkStatistics.LCC, rc1[Experiment.RESULTS])

    def testNetworkPassed(self):
        '''Test the second process sees the network as changed by the first.'''
        params = dict()
        params[ERNetwork.N] = 1000
        params[ERNetwork.KMEAN] = 5
        params[SIR.P_INFECT] = 0.2
        params[SIR.P_REMOVE] = 0.2
        params[SIR.P_INFECTED] = 0.01
        params[Percolate.T] = 0.5

        # run process singly to get baseline
        e = StochasticDynamics(NetworkStatistics(), ERNetwork())
        rc1 = e.set(params).run()

        # reduce the network first by percolation, then run again
        p = ProcessSequence([Percolate(), NetworkStatistics()])
        e = StochasticDynamics(p, ERNetwork())
        rc2 = e.set(params).run()

        # bond percolation shouold reduce the number of edges (only) 
        self.assertTrue(rc1[Experiment.RESULTS][NetworkStatistics.N] == rc2[Experiment.RESULTS][NetworkStatistics.N])
        self.assertTrue(rc1[Experiment.RESULTS][NetworkStatistics.M] > rc2[Experiment.RESULTS][NetworkStatistics.M])

if __name__ == '__main__':
    unittest.main()
