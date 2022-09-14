# Test the core-periphery network generator
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

from epydemic import CorePeripheryNetwork
from epyc import Experiment
import unittest
import networkx

class CorePeripheryTests(unittest.TestCase):

    def setUp(self):
        self._params = dict()
        self._params[CorePeripheryNetwork.N_core] = 1000
        self._params[CorePeripheryNetwork.PHI_core] = 0.01
        self._params[CorePeripheryNetwork.N_per] = 1000
        self._params[CorePeripheryNetwork.PHI_per] = 0.005

        self._gen = CorePeripheryNetwork(self._params)
        self._g = self._gen.generate()

    def testParameters(self):
        '''Check we generate core and periphery correctly.'''

        # check N and PHI for core
        core_ns = len([n for n in self._g.nodes() if self._g.nodes[n][CorePeripheryNetwork.ORIGIN] == 0])
        self.assertAlmostEqual(core_ns, self._params[CorePeripheryNetwork.N_core], delta=1)
        core_es = len([e for e in self._g.edges() if (self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] == 0 and
                                                  self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN] == 0)])
        self.assertAlmostEqual(core_es / (core_ns * (core_ns - 1) / 2),
                               self._params[CorePeripheryNetwork.PHI_core], places=1)

        # check N and PHI for periphery
        per_ns = len([n for n in self._g.nodes() if self._g.nodes[n][CorePeripheryNetwork.ORIGIN] == 1])
        self.assertAlmostEqual(per_ns, self._params[CorePeripheryNetwork.N_per], delta=1)
        per_es = len([e for e in self._g.edges() if (self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] == 1 and
                                                  self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN] == 1)])
        self.assertAlmostEqual(per_es / (per_ns * (per_ns - 1) / 2),
                               self._params[CorePeripheryNetwork.PHI_per], places=1)

        # check density between core and periphery is that of periphery
        link_es = len([e for e in self._g.edges() if self._g.nodes[e[0]][CorePeripheryNetwork.ORIGIN] != self._g.nodes[e[1]][CorePeripheryNetwork.ORIGIN]])
        self.assertAlmostEqual(link_es / ((core_ns + per_ns) * ((core_ns + per_ns) - 1) / 2),
                               self._params[CorePeripheryNetwork.PHI_per], places=1)


if __name__ == '__main__':
    unittest.main()
