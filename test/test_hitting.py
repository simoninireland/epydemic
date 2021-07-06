# Test hitting time recording
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
import unittest


class CaptureNetwork(Process):

    def __init__(self):
        super().__init__()
        self._finalNetwork = None

    def finalNetwork(self):
        return self._finalNetwork

    def setUp(self, params):
        super().setUp(params)
        self._finalNetwork = None

    def results(self):
        rc = super().results()
        self._finalNetwork = self.network()
        return rc


class HittingTest(unittest.TestCase):

    def testHitting(self):
        '''Test all nodes infected during the epidemic get a hitting time recorded.'''
        params = dict()
        params[ERNetwork.N] = 5000
        params[ERNetwork.KMEAN] = 20
        params[SIR.P_INFECTED] = 0.001
        params[SIR.P_INFECT] = 0.3
        params[SIR.P_REMOVE] = 0.05

        m = SIR()
        c = CaptureNetwork()
        g = ERNetwork()
        e = StochasticDynamics(ProcessSequence([m, c]), g)
        rc = e.set(params).run(fatal=True)

        gprime = c.finalNetwork()
        infecteds = [n for n in gprime.nodes if gprime.nodes[n][CompartmentedModel.COMPARTMENT] == SIR.REMOVED]
        initialInfecteds = 0
        for n in infecteds:
            if CompartmentedModel.T_HITTING in gprime.nodes[n]:
                # hitting time is actually a time
                t = gprime.nodes[n][CompartmentedModel.T_HITTING]
                self.assertTrue(t > 0)

                # there's an occupied incident edge with the same occupation time
                occs = [(n, m ) for (n, m) in gprime.edges(n) if gprime.get_edge_data(n, m)[CompartmentedModel.OCCUPIED]]
                ts = [gprime.get_edge_data(n, m)[CompartmentedModel.T_OCCUPIED] for (n, m) in occs]
                self.assertTrue(t in ts)
            else:
                # initially infected node
                initialInfecteds += 1

        # there can't be too many initially infected nodes
        self.assertAlmostEqual(initialInfecteds, params[ERNetwork.N] * params[SIR.P_INFECTED], delta=5)


if __name__ == '__main__':
    unittest.main()
