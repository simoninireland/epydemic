# Test SIS with fixed recovery time under different dynamics
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
from test.compartmenteddynamics import CompartmentedDynamicsTest
import epyc
import unittest
import networkx

class SISFixedRecoveryTest(unittest.TestCase, CompartmentedDynamicsTest):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''        
        self._network = networkx.erdos_renyi_graph(1000, 0.02)
        self._model = SIS_FixedRecovery()

    def testEpidemic( self ):
        '''Test we get an epidemic'''
        self._lab = epyc.Lab()
        self._lab[SIS.P_INFECT] = 0.1
        self._lab[SIS.P_INFECTED] = 0.01
        self._lab[SIS_FixedRecovery.T_INFECTED] = 1.0
        self._model.setMaximumTime(100)
        e = StochasticDynamics(self._model, self._network)
        self._lab.runExperiment(e)
        rc = (self._lab.results())[0]
        print(rc)

        self.assertCountEqual(rc[epyc.Experiment.RESULTS], [SIS.SUSCEPTIBLE, SIS.INFECTED])
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIS.SUSCEPTIBLE] > 0)
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIS.INFECTED] > 0)
        self.assertEqual(rc[epyc.Experiment.RESULTS][SIS.SUSCEPTIBLE] + rc[epyc.Experiment.RESULTS][SIS.INFECTED], self._network.order())

if __name__ == '__main__':
    unittest.main()
