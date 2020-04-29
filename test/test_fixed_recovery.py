# Test the SIR and SIS fixed-time recovery variants
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
import epyc
import unittest
import networkx
import six

class FixedRecoveryTest(unittest.TestCase):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        
        # single experiment
        self._params = dict()
        self._params[SIR_FixedRecovery.P_INFECT] = 0.1
        self._params[SIR_FixedRecovery.P_INFECTED] = 0.01
        self._params[SIR_FixedRecovery.T_INFECTED] = 1
        self._network = networkx.erdos_renyi_graph(1000, 0.005)

    def testRunSingleSIRSynchronous( self ):
        '''Test a single run of a fixed-period SIR under synchronous dynamics.'''
        e = SynchronousDynamics(SIR_FixedRecovery(), self._network)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
            self.assertTrue(rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS])
        else:
            six.assertCountEqual(self, rc[epyc.Experiment.RESULTS], [SIR_FixedRecovery.SUSCEPTIBLE, SIR_FixedRecovery.INFECTED, SIR_FixedRecovery.REMOVED])
            self.assertTrue(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.SUSCEPTIBLE] > 0)
            self.assertTrue(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.INFECTED] == 0)
            self.assertTrue(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.REMOVED] > 0)
            self.assertEqual(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.SUSCEPTIBLE] + rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.REMOVED], self._network.order())

    def testRunSingleSIRStochastic( self ):
        '''Test a single run of a fixed-period SIR under stochastic dynamics.'''
        e = StochasticDynamics(SIR_FixedRecovery(), self._network)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
            self.assertTrue(rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS])
        else:
            six.assertCountEqual(self, rc[epyc.Experiment.RESULTS], [SIR_FixedRecovery.SUSCEPTIBLE, SIR_FixedRecovery.INFECTED, SIR_FixedRecovery.REMOVED])
            self.assertTrue(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.SUSCEPTIBLE] > 0)
            self.assertTrue(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.INFECTED] == 0)
            self.assertTrue(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.REMOVED] > 0)
            self.assertEqual(rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.SUSCEPTIBLE] + rc[epyc.Experiment.RESULTS][SIR_FixedRecovery.REMOVED], self._network.order())
  
if __name__ == '__main__':
    unittest.main()
