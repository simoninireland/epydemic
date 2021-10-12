# Test the opinion dynamics process
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
import epyc
import unittest
import networkx


class OpinionRecorder(Opinion):

    N = 'networkSize'

    def __init__(self):
        super().__init__()
        self._finalNetwork = None

    def setUp(self, params):
        super().setUp(params)
        self._finalNetwork = None

    def finalNetwork(self):
        '''Return the final network that we saved.

        :returns: the network'''
        return self._finalNetwork

    def results(self):
        '''Save the size of the resulting network and the final
        network itself for further analysis.

        :returns: a dict of experimental results'''
        rc = super().results()
        rc[self.N] = self.network().order()
        self._finalNetwork = self.network()
        return rc


class OpinionTest(unittest.TestCase):

    def setUp(self):
        '''Set up the experimental parameters and process.'''
        N = 5000
        kmean = 10
        phi = (kmean + 0.0) / N
        self._network = networkx.erdos_renyi_graph(N, phi)
        self._maxTime = 5000

        self._params = dict()
        self._process = OpinionRecorder()
        self._process.setMaximumTime(self._maxTime)
        self._e = StochasticDynamics(self._process, self._network)

    def testRun(self):
        '''Test that the process runs.'''
        self._params[Opinion.P_AFFECTED] = 0.02
        self._params[Opinion.P_AFFECT] = 0.01
        self._params[Opinion.P_STIFLE] = 0.01
        rc = self._e.set(self._params).run(fatal=True)


if __name__ == '__main__':
    unittest.main()
