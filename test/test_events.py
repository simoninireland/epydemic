# Test event taps
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

from types import MethodType
import unittest
from epydemic import *
from epyc import Experiment


def addTap(o):
    '''Monkey-patch the tap infrastructure onto an object.'''

    # Event tap API

    def initialiseEventTaps(self):
        self._tapped = []
        self._tapStarted = False
        self._tapEnded = False

    def simulationStarted(self):
        self._tapStarted = True

    def simulationEnded(self):
        self._tapEnded = True

    def eventFired(self, t, name, e):
        self._tapped.append((t, name))

    # Access methods

    def tappedEvents(self):
        return self._tapped

    def startEnd(self):
        return (self._tapStarted, self._tapEnded)

    # monkey-patch the new methods into place
    o.initialiseEventTaps = MethodType(initialiseEventTaps, o)
    o.simulationStarted = MethodType(simulationStarted, o)
    o.simulationEnded = MethodType(simulationEnded, o)
    o.eventFired = MethodType(eventFired, o)
    o.tappedEvents = MethodType(tappedEvents, o)
    o.startEnd = MethodType(startEnd, o)

    o.initialiseEventTaps()   # tap is installed late

    return o


class EventsTest(unittest.TestCase):

    def testTapSimulation( self ):
        '''Test we tap events from a normal simulation.'''
        params = dict()
        params[SIR.P_INFECT] = 0.3
        params[SIR.P_INFECTED] = 0.01
        params[SIR.P_REMOVE] = 0.05
        params[ERNetwork.N] = 1000
        params[ERNetwork.PHI] = 0.005
        model = SIR()
        e = addTap(StochasticDynamics(model, ERNetwork()))
        rc = e.set(params).run()

        # check we got events
        es = e.tappedEvents()
        self.assertEqual(e.startEnd(), (True, True))
        self.assertGreater(len(es), 0)
        self.assertGreater(len([n for (_, n) in es if n == SIR.INFECTED]), 0)
        self.assertGreater(len([n for (_, n) in es if n == SIR.REMOVED]), 0)

    def testTapBond(self):
        '''Test we can tap bond percolation.'''
        params = dict()
        params[ERNetwork.N] = 1000
        params[ERNetwork.PHI] = 0.005
        e = addTap(BondPercolation(ERNetwork()))
        rc = e.set(params).run()

        # check we got events
        es = e.tappedEvents()
        self.assertEqual(e.startEnd(), (True, True))
        self.assertGreater(len(es), 0)

    def testTapSite(self):
        '''Test we can tap site percolation.'''
        params = dict()
        params[ERNetwork.N] = 1000
        params[ERNetwork.PHI] = 0.005
        e = addTap(SitePercolation(ERNetwork()))
        rc = e.set(params).run()

        # check we got events
        es = e.tappedEvents()
        self.assertEqual(e.startEnd(), (True, True))
        self.assertEqual(len(es), params[ERNetwork.N])  # all nodes occupied


if __name__ == '__main__':
    unittest.main()
