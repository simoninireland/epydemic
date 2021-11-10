# Test the vaccination processes
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
import epyc
import unittest
import networkx


class VaccinationTest(unittest.TestCase):

    def setUp(self):
        '''Set up the experimental parameters and process.'''
        N = 5000
        kmean = 10
        phi = (kmean + 0.0) / N
        self._network = networkx.erdos_renyi_graph(N, phi)
        self._maxTime = 5

        self._params = dict()

    def testRun(self):
        '''Test that the process runs.'''

        # opinion process
        self._process = ProcessSequence([Vaccinate(), Monitor()])
        self._e = StochasticDynamics(self._process, self._network)

        # disease
        self._params[SIR.P_INFECT] = 0.05
        self._params[SIR.P_REMOVE] = 0.05
        self._params[SIR.P_INFECTED] = 0.001

        # opinion (pro- and anti-vax)
        self._params[Opinion.P_AFFECTED] = 0.02
        self._params[Opinion.P_AFFECT] = 0.01
        self._params[Opinion.P_STIFLE] = 0.01

        # vaccination
        self._params[SIvR.EFFICACY] = 0.8
        self._params[Vaccinate.P_VACCINATE] = 0.5

        # monitoring
        self._params[Monitor.DELTA] = 1 # self._maxTime / 100

        rc = self._e.set(self._params).run(fatal=True)
        print(rc)


if __name__ == '__main__':
    unittest.main()
