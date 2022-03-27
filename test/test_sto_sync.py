# Test compatibility between the two kinds of dynamics
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

from epydemic import *
import epyc
import unittest
import networkx


class MonitoredSIR(SIR):

    def build(self, params):
        super().build(params)
        self.trackNodesInCompartment(SIR.SUSCEPTIBLE)
        self.trackNodesInCompartment(SIR.REMOVED)


class StoSyncTest(unittest.TestCase):

    def testStochasticMonitor(self):
        '''Test monitoring of a process under stochastic dynamics.'''
        p = ProcessSequence([MonitoredSIR(), Monitor()])

        param = dict()
        param[SIR.P_INFECTED] = 0.001
        param[SIR.P_INFECT] = 0.0001
        param[SIR.P_REMOVE] = 0.001
        param[ERNetwork.N] = 10000
        param[ERNetwork.KMEAN] = 50
        param[Monitor.DELTA] = 1

        e = StochasticDynamics(p, ERNetwork())
        rc = e.set(param).run(fatal=True)

    def testSynchronousMonitor(self):
        '''Test monitoring of a process under synchronous dynamics.'''
        p = ProcessSequence([MonitoredSIR(), Monitor()])

        param = dict()
        param[SIR.P_INFECTED] = 0.001
        param[SIR.P_INFECT] = 0.0001
        param[SIR.P_REMOVE] = 0.001
        param[ERNetwork.N] = 10000
        param[ERNetwork.KMEAN] = 50
        param[Monitor.DELTA] = 1

        e = SynchronousDynamics(p, ERNetwork())
        rc = e.set(param).run(fatal=True)


if __name__ == '__main__':
    unittest.main()
