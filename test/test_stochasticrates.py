# Test stochastic dynamics generates believable event traces
#
# Copyright (C) 2017--2019 Simon Dobson
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

import epyc
from epydemic import *
import networkx
import unittest
import six

class DummyLocus(Locus):
    def __init__(self, name):
        super(DummyLocus, self).__init__(name)

    def draw(self):
        return None

    def __len__(self):
        return 1


class FixedRatesCounter(Process):
    def __init__(self):
        super(FixedRatesCounter, self).__init__()

    def build( self, params ):
        ecr = params['eventCountRate']
        self._eventCount = [ 0 ] * len(ecr)
        for i in range(len(ecr)):
            l = self.addLocus(i, DummyLocus(i))
            self.addFixedRateEvent(l, ecr[i], lambda t, e: self.happened(i, t, e))

    def happened( self, i, t, e ):
        self._eventCount[i] = self._eventCount[i] + 1

    def results(self):
        rc = dict()
        rc['eventCount'] = self._eventCount
        return rc


class StochasticRatesTest(unittest.TestCase):

    def setUp(self):
        self._dyn = StochasticDynamics(FixedRatesCounter(), networkx.erdos_renyi_graph(100, 0.01))
        self._maxTime = 5000
        self._dyn.process().setMaximumTime(self._maxTime)

    def _checkRates(self, rc):
        eps = self._maxTime * 0.01                                # allow 1% deviation
        ecr = rc[epyc.Experiment.PARAMETERS]['eventCountRate']
        ecs = rc[epyc.Experiment.RESULTS]['eventCount']
        for i in range(0, len(ecs)):
            if ecr[i] == 0:
                self.assertEqual(ecs[i], 0)
            else:
                self.assertAlmostEqual(((ecs[i] + 0.0) / ecr[i]) / self._maxTime, 1.0, delta = eps)

    def testSameRates(self):
        '''Test same rates are generated in the correct proportions.'''
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 1, 1, 1 ])).run())

    def testDifferentRates(self):
        '''Test different rates are generated in the correct proportions.'''
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 1, 2, 5 ])).run())

    def testDifferentRatesOrder(self):
        '''Test different rates are generated in the correct proportions when presented in a different order.'''
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 5, 2, 1 ])).run())

    def testRadicallyDifferentRates(self):
        '''Test very different rates are generated in the correct proportions.'''
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 1, 2, 5, 1000 ])).run())

    def testZeroRates(self):
        '''Test that a zero-rate event isn't generated.'''
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 1, 0, 1 ])).run())

    def testAllZeroRates(self):
        '''Test that nothing happens when rates are all zero.'''
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 0, 0, 0 ])).run())

    def testOneRates(self):
        '''Test that things still work when there's only one event type.'''
        self._checkRates(self._dyn.set(dict(eventCountRate=[ 1 ])).run())

    def testLotsOfRates(self):
        '''Test that things still work when there are a lot of low-rate events.'''
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 1 ] * 50)).run())

if __name__ == '__main__':
    unittest.main()
