# Test multiple simultaneous instances of the same process
#
# Copyright (C) 2017--2024 Simon Dobson
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

class CoinfectionTest(unittest.TestCase):

    def testTwoProcesses(self):
        """Test we can run two process instances."""
        N = 10000
        kmean = 100

        # network
        params = dict()
        params[ERNetwork.N] = N
        params[ERNetwork.KMEAN] = kmean

        # first infection
        p1 = SIR("First disease")
        p1.setParameters(params,
                         {SIR.P_INFECT: 0.1,
                          SIR.P_INFECTED: 1.0 / N,
                          SIR.P_REMOVE: 0.005,
                          })

        # second infection
        p2 = SIR("Second disease")
        p2.setParameters(params,
                         {SIR.P_INFECT: 0.3,
                          SIR.P_INFECTED: 1.0 / N,
                          SIR.P_REMOVE: 0.005,
                          })

        # run the processes together
        ps = ProcessSequence([p1, p2])
        e = StochasticDynamics(ps, ERNetwork())
        rc = e.set(params).run(fatal=True)

        # we should have more nodes hit by the second infection than by the first
        g = e.network()
        hit1 = [n for n in g.nodes if g.nodes[n].get(p1.HITTING_PROCESS_NAME) == "First disease"]
        hit2 = [n for n in g.nodes if g.nodes[n].get(p2.HITTING_PROCESS_NAME) == "Second disease"]
        self.assertTrue(len(hit2) > len(hit1))
        self.assertEqual(rc[Experiment.RESULTS][SIR.REMOVED], len(hit1) + len(hit2))


if __name__ == '__main__':
    unittest.main()
