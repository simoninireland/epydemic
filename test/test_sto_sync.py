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


class StoSyncTest(unittest.TestCase):

    def testStochasticMonitor(self):
        '''Test monitoring of a process under stochastic dynamics.'''
        T = 1000000
        num_of_points = 1000
        deltaM = T / num_of_points

        m = SIR()
        p = ProcessSequence([m, Monitor()])

        param = dict()
        param[SIR.P_INFECTED] = 0.01
        param[SIR.P_INFECT] = 0.1
        param[SIR.P_REMOVE] = 0.2
        param[ERNetwork.N] = 5000
        param[ERNetwork.KMEAN] = 10
        param[Monitor.DELTA] = deltaM

        e = StochasticDynamics(p, ERNetwork())
        e.process().setMaximumTime(T)
        rc = e.set(param).run(fatal=True)

    def testSynchronousMonitor(self):
        '''Test monitoring of a process under synchronous dynamics.'''
        T = 1000000
        num_of_points = 1000
        deltaM = T / num_of_points

        m = SIR()
        p = ProcessSequence([m, Monitor()])

        param = dict()
        param[SIR.P_INFECTED] = 0.01
        param[SIR.P_INFECT] = 0.1
        param[SIR.P_REMOVE] = 0.2
        param[ERNetwork.N] = 5000
        param[ERNetwork.KMEAN] = 10
        param[Monitor.DELTA] = deltaM

        e = SynchronousDynamics(p, ERNetwork())
        e.process().setMaximumTime(T)
        rc = e.set(param).run(fatal=True)


if __name__ == '__main__':
    unittest.main()
