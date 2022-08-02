# Test SIR with variable infection under different dynamics
#
# Copyright (C) 2017--2022 Simon Dobson
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

import unittest
import networkx             # type: ignore
import epyc
from epydemic import *
from test.compartmenteddynamics import CompartmentedDynamicsTest

class SIRTest(unittest.TestCase, CompartmentedDynamicsTest):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''

        # single epidemic-causing experiment
        self._params = dict()
        self._params[SIR.P_INFECT] = 0.3
        self._params[SIR.P_INFECTED] = 0.01
        self._params[SIR.P_REMOVE] = 0.05
        self._network = networkx.erdos_renyi_graph(1000, 0.005)

        # lab run
        self._lab = epyc.Lab()
        self._lab[SIR.P_INFECTED] = 0.01
        self._lab[SIR.P_REMOVE] = [ 0.05, 1 ]

        # model
        self._model = SIR_VariableInfection()

    def assertEpidemic(self, rc):
        self.assertCountEqual(rc, [SIR.SUSCEPTIBLE, SIR.INFECTED, SIR.REMOVED])
        self.assertTrue(rc[SIR.SUSCEPTIBLE] > 0)
        self.assertTrue(rc[SIR.INFECTED] == 0)
        self.assertTrue(rc[SIR.REMOVED] > 0)
        self.assertEqual(rc[SIR.SUSCEPTIBLE] + rc[SIR.REMOVED], self._network.order())

    def testConstantInfection(self):
        '''Test we get consistent results under standard and variable infection when the infection is constant.'''

        # under ordinary SIR
        e = StochasticDynamics(SIR(), self._network)
        rc_basic = e.set(self._params).run(fatal=True)
        self.assertTrue(rc_basic[epyc.Experiment.METADATA][epyc.Experiment.STATUS])
        self.assertEpidemic(rc_basic[epyc.Experiment.RESULTS])

        # under variable dynamics with constant value
        m = SIR_VariableInfection()
        inf = self._params[SIR.P_INFECT]

        def patchInitialInfectivities(self):
            '''Set all infectivities to the same value.'''
            g = self.network()
            for(_, _, data) in g.edges(data=True):
                data[self.INFECTIVITY] = inf

        # patch the model instance
        import types
        m.initialInfectivities = types.MethodType(patchInitialInfectivities, m)

        e = StochasticDynamics(m, self._network)
        rc_var = e.set(self._params).run(fatal=True)
        self.assertTrue(rc_var[epyc.Experiment.METADATA][epyc.Experiment.STATUS])
        self.assertEpidemic(rc_var[epyc.Experiment.RESULTS])

        # check consistency
        self.assertAlmostEqual(rc_basic[epyc.Experiment.RESULTS][SIR.REMOVED],
                               rc_var[epyc.Experiment.RESULTS][SIR.REMOVED],
                               delta=int(self._network.order() * 0.05))  # within 5% difference


if __name__ == '__main__':
    unittest.main()
