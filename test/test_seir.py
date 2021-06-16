# Test SEIR under different dynamics
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

class SEIRTest(unittest.TestCase, CompartmentedDynamicsTest):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''

        # single experiment
        self._params = dict()
        self._params[SEIR.P_INFECT_SYMPTOMATIC] = 0.3
        self._params[SEIR.P_INFECT_ASYMPTOMATIC] = 0.3
        self._params[SEIR.P_EXPOSED] = 0.01
        self._params[SEIR.P_SYMPTOMS] = 0.05
        self._params[SEIR.P_REMOVE] = 0.05
        self._network = networkx.erdos_renyi_graph(1000, 0.005)

        # lab run
        self._lab = epyc.Lab()
        self._lab[SEIR.P_INFECT_SYMPTOMATIC] = 0.1
        self._lab[SEIR.P_INFECT_ASYMPTOMATIC] = [ 0.1,  0.3 ]
        self._lab[SEIR.P_EXPOSED] = 0.01
        self._lab[SEIR.P_SYMPTOMS] = [ 0.05, 1 ]
        self._lab[SEIR.P_REMOVE] = 0.05

        # model
        self._model = SEIR()

    def assertEpidemic(self, rc):
        self.assertCountEqual(rc, [SEIR.SUSCEPTIBLE, SEIR.EXPOSED, SEIR.INFECTED, SEIR.REMOVED])
        self.assertTrue(rc[SEIR.SUSCEPTIBLE] > 0)
        self.assertTrue(rc[SEIR.EXPOSED] == 0)
        self.assertTrue(rc[SEIR.INFECTED] == 0)
        self.assertTrue(rc[SEIR.REMOVED] > 0)
        self.assertEqual(rc[SEIR.SUSCEPTIBLE] + rc[SEIR.REMOVED], self._network.order())

if __name__ == '__main__':
    unittest.main()
