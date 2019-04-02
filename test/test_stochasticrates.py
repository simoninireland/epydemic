# Test stochastic dynamics generates believable event traces
#
# Copyright (C) 2017--18 Simon Dobson
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

from __future__ import print_function
import epyc
from epydemic import *
import unittest
import six

class DummyLocus(Locus):

    def draw( self ):
        return None

    def __len__(self):
        return 1


class StochasticDynamicsFixedRates(StochasticDynamics):

    def __init__(self):
        super(StochasticDynamicsFixedRates, self).__init__(Process())

    def setUp( self, params ):
        ecr = params['eventCountRate']
        self._eventCount = [ 0 ] * len(ecr)
        self._eventHandlers = [ (DummyLocus(i), ecr[i], self._event(i)) for i in range(len(ecr)) ]

    def eventRateDistribution( self, t ):
        return self._eventHandlers

    def _event(self, i):
        return (lambda d, t, g, e: self.event(i, d, t, g, e))

    def event( self, i, d, t, g, e ):
        self._eventCount[i] = self._eventCount[i] + 1

    def experimentalResults(self):
        rc = dict()
        rc['eventCount'] = self._eventCount
        return rc


class StochasticRatesTest(unittest.TestCase):

    def setUp(self):
        self._dyn = StochasticDynamicsFixedRates()

    def _checkRates(self, rc):
        eps = self._dyn._maxTime * 0.01
        ecr = rc[epyc.Experiment.PARAMETERS]['eventCountRate']
        ecs = rc[epyc.Experiment.RESULTS]['eventCount']
        for i in range(0, len(ecs)):
            if ecr[i] == 0:
                self.assertEqual(ecs[i], 0)
            else:
                self.assertAlmostEqual(((ecs[i] + 0.0) / ecr[i]) / self._dyn._maxTime, 1.0, delta = eps)

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
        self._checkRates(self._dyn.set(dict(eventCountRate = [ 1 ] * 100)).run())
