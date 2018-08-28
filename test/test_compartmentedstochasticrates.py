# Test stochastic dynamics generates believable event traces for compartmented networks
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
import networkx
import unittest
import six


class DummyModel(CompartmentedModel):

    def build(self, params):
        ep = params['eventProbability']
        for i in range(len(ep)):
            self.addCompartment(i, 1.0 / len(ep))
            self.addLocus(i)
            self.addEvent(i, ep[i], self._event(i))

    def _event(self, i):
        return (lambda d, t, g, e: self.event(i, d, t, g, e))

    def event(self, i, d, t, g, e):
        d._eventCount[i] = d._eventCount[i] + 1

class CompartmentedStochasticDynamicsFixedRates(CompartmentedStochasticDynamics):

    def setUp( self, params ):
        super(CompartmentedStochasticDynamicsFixedRates, self).setUp(params)
        self._eventCount = [ 0 ] * len(params['eventProbability'])

    def experimentalResults(self):
        rc = dict()
        rc['compartments'] = super(CompartmentedStochasticDynamicsFixedRates, self).experimentalResults()
        rc['eventCount'] = self._eventCount
        return rc


class CompartmentedStochasticRatesTest(unittest.TestCase):

    N = 5000
    kmean = 5

    def setUp(self):
        phi = self.kmean/ self.N
        g = networkx.erdos_renyi_graph(self.N, phi)
        self._dyn = CompartmentedStochasticDynamicsFixedRates(DummyModel(), g)
        self._dyn.setMaximumTime(100)

    def _checkRates(self, rc):
        eps = self._dyn._maxTime * 0.01
        ep = rc[epyc.Experiment.PARAMETERS]['eventProbability']
        ecs = rc[epyc.Experiment.RESULTS]['eventCount']
        cs = rc[epyc.Experiment.RESULTS]['compartments']
        for i in range(0, len(ecs)):
            if ep[i] == 0:
                self.assertEqual(ecs[i], 0)
            else:
                self.assertAlmostEqual(((ecs[i] + 0.0) / (ep[i] * cs[i])) / self._dyn._maxTime, 1.0, delta = eps)

    def testSameRates(self):
        '''Test same rates are generated in the correct proportions.'''
        self._checkRates(self._dyn.set(dict(eventProbability = [ 0.25, 0.25, 0.25, 0.25 ])).run())

    def testDifferentRates(self):
        '''Test different rates are generated in the correct proportions.'''
        self._checkRates(self._dyn.set(dict(eventProbability = [ 0.1, 0.2, 0.75, 1 ])).run())

    def testDifferentRatesOrder(self):
        '''Test different rates are generated in the correct proportions when presented in a diferent order.'''
        self._checkRates(self._dyn.set(dict(eventProbability = [ 1, 0.75, 0.1, 0.2 ])).run())

    def testRadicallyDifferentRates(self):
        '''Test very different rates are generated in the correct proportions.'''
        self._checkRates(self._dyn.set(dict(eventProbability = [ 0.25, 1, 0.25, 50 ])).run())

    def testZeroRates(self):
        '''Test that a zero-rate event isn't generated.'''
        self._checkRates(self._dyn.set(dict(eventProbability = [ 0.75, 0, 0.75 ])).run())

    def testAllZeroRates(self):
        '''Test that nothing happens when rates are all zero.'''
        self._checkRates(self._dyn.set(dict(eventProbability = [ 0, 0, 0 ])).run())

    def testOneRates(self):
        '''Test that things still work when there's only one event type.'''
        self._checkRates(self._dyn.set(dict(eventProbability=[ 0.25 ])).run())

    def testLotsOfRates(self):
        '''Test that things still work when there are a lot of low-rate events.'''
        self._checkRates(self._dyn.set(dict(eventProbability = [ 0.01 ] * 100)).run())
