# Test synchronisation process
#
# Copyright (C) 2027--2022 Simon Dobson
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

from collections import Counter
import numpy
from networkx import complete_graph
from epyc import Experiment, Lab
from epydemic import *
import unittest


class PulseCoupledSyncSets(PulseCoupledOscillator):

    LARGEST_SYNC_SETS = 'epydemic.pulsecoupled.largest'

    def build(self, params):
        super().build(params)
        self._lastSynched = {}
        self._largestSyncSet = []

    def setUp(self, params):
        super().setUp(params)
        self._lastSynched = self.syncSets(0.0)
        self._largestSyncSet.append(max(map(len, self._lastSynched.values())))

    def syncSets(self, t):
        '''Compute the sync sets, a mapping from phases to
        nodes having that phase.

        :param t: the time
        :returns: the sync sets'''
        g = self.network()

        locked = {}
        locked[0.0] = []
        for n in g.nodes():
            phi = self.getPhase(t, n, normalise=True)
            if phi not in locked.keys():
                locked[phi] = []
            locked[phi].append(n)
        return locked

    def fired(self, t, e):
        super().fired(t, e)

        self._lastSynched = self.syncSets(t)
        self._largestSyncSet.append(max(map(len, self._lastSynched.values())))

        assert self._largestSyncSet[-1] >= self._largestSyncSet[-2]

    def results(self):
        rc = super().results()
        rc[self.LARGEST_SYNC_SETS] = self._largestSyncSet
        return rc


class PulseCoupledPhases(PulseCoupledOscillator):

    PHASES = 'epydemic.pulsecoupled.nPhases'

    def build(self, params):
        super().build(params)
        self._nPhases = []

    def setUp(self, params):
        super().setUp(params)
        self._nPhases.append(self.phases(0.0))

    def phases(self, t):
        g = self.network()
        phis = [self.getPhase(t, n, normalise=True) for n in g.nodes()]
        c = Counter(phis)
        return len(c.keys())

    def fired(self, t, e):
        super().fired(t, e)
        self._nPhases.append(self.phases(t))
        assert self._nPhases[-1] <= self._nPhases[-2]

    def results(self):
        rc = super().results()
        rc[self.PHASES] = self._nPhases
        return rc


class PulseCoupledTest(unittest.TestCase):

    N = 100
    period = 2.0
    dissipation = 1.0
    coupling = 0.007

    repetitions = 10

    def setUp(self):
        self._lab = Lab()
        self._lab[PulseCoupledOscillator.PERIOD] = self.period
        self._lab[PulseCoupledOscillator.B] = self.dissipation
        self._lab[PulseCoupledOscillator.COUPLING] = self.coupling
        self._lab['repetitions'] = range(self.repetitions)

        self._g = complete_graph(self.N)

        self._p = PulseCoupledOscillator()
        self._p.setMaximumTime(12 * self.period)
        self._e = StochasticDynamics(self._p, FixedNetwork(self._g))

    def testStatePhaseFunctions(self):
        '''Test that the state and phase functions have the right properties.'''
        # pick a dissipation parameter
        self._p._b = 1.0

        # phase to state
        # (monotonically increasing, concave down)
        state_0 = 0.0
        diff_0 = None
        for phi in numpy.linspace(0.0, 1.0, 100):
            state_1 = self._p.phaseToState(phi)
            diff_1 = state_1 - state_0

            self.assertTrue(0.0 <= state_1 and state_1 <= 1.0)
            self.assertTrue(state_1 >= state_0)
            if diff_0 is not None and diff_0 > 0.0:
                self.assertTrue(diff_1 <= diff_0)
            state_0, diff_0 = state_1, diff_1

        # state to phase
        # (monotonically increasing, concave up)
        phase_0 = 0.0
        diff_0 = None
        for x in numpy.linspace(0.0, 1.0, 100):
            phase_1 = self._p.stateToPhase(x)
            diff_1 = phase_1 - phase_0

            self.assertTrue(0.0 <= phase_1 and phase_1 <= 1.0)
            self.assertTrue(phase_1 >= phase_0)
            if diff_0 is not None and diff_0 > 0.0:
                self.assertTrue(diff_1 >= diff_0)
            phase_0, diff_0 = phase_1, diff_1

        # inverses
        for phi in numpy.linspace(0.0, 1.0, 100):
            self.assertAlmostEqual(phi, self._p.stateToPhase(self._p.phaseToState(phi)), places=2)

    def testSync(self):
        '''Test we synchronise at the end.'''
        self._lab.runExperiment(self._e)
        df = self._lab.dataframe()
        for phis in df[PulseCoupledOscillator.PHASES]:
            for phi in phis[1:]:
                self.assertEqual(phi, phis[0])

    def testMonotonicSync(self):
        '''Test that the largest sync set grows monotonically.'''
        self._p = PulseCoupledSyncSets()
        self._p.setMaximumTime(12 * self.period)
        self._e = StochasticDynamics(self._p, FixedNetwork(self._g))

        self._lab.runExperiment(self._e)
        df = self._lab.dataframe(only_successful=False)
        for ss in df[PulseCoupledSyncSets.LARGEST_SYNC_SETS]:
            #self.assertEqual(ss[0], 1)
            for i in range(1, len(ss)):
                self.assertGreaterEqual(ss[i], ss[i - 1])

    def testMonotonicPhases(self):
        '''Test that the number of distinct phases shrinks monotonically.'''
        self._p = PulseCoupledPhases()
        self._p.setMaximumTime(12 * self.period)
        self._e = StochasticDynamics(self._p, FixedNetwork(self._g))

        self._lab.runExperiment(self._e)
        df = self._lab.dataframe()
        for ss in df[PulseCoupledPhases.PHASES]:
            #self.assertEqual(ss[0], self.N)
            for i in range(1, len(ss)):
                self.assertLessEqual(ss[i], ss[i -1])


if __name__ == '__main__':
    unittest.main()
