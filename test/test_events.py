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

    def simulationStarted(self, params):
        self._tapStarted = True

    def simulationEnded(self, res):
        self._tapEnded = True

    def eventFired(self, t, p, name, e):
        self._tapped.append((t, p, name))

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

    # ---------- Stochastic process dynamics ----------

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
        rc = e.set(params).run(fatal=True)

        # check we got events
        es = e.tappedEvents()
        self.assertEqual(e.startEnd(), (True, True))
        self.assertGreater(len(es), 0)
        self.assertGreater(len([n for (_, _, n) in es if n == SIR.INFECTED]), 0)
        self.assertGreater(len([n for (_, _, n) in es if n == SIR.REMOVED]), 0)


    # ---------- Synchronous process dynamics ----------

    # TBD

    # ---------- Multiple processes ----------

    def testProcess(self):
        '''Test we're passed the right process.'''
        params = dict()
        params[SIR.P_INFECT] = 0.3
        params[SIR.P_INFECTED] = 0.01
        params[SIR.P_REMOVE] = 0.05
        params[ERNetwork.N] = 1000
        params[ERNetwork.PHI] = 0.005
        model = SIR()
        e = addTap(StochasticDynamics(model, ERNetwork()))
        rc = e.set(params).run(fatal=True)

        es = e.tappedEvents()
        for (_, p, _) in es:
            self.assertEqual(p, model)

    def testTwoProcesses(self):
        '''Test we get the right events from two processes.'''
        params = dict()
        params[Percolate.T] = 0.1
        params[SIR.P_INFECT] = 0.3
        params[SIR.P_INFECTED] = 0.01
        params[SIR.P_REMOVE] = 0.05
        params[ERNetwork.N] = 1000
        params[ERNetwork.PHI] = 0.005
        model1 = Percolate()
        model2 = SIR()
        p = ProcessSequence([model1, model2])
        e = addTap(StochasticDynamics(p, ERNetwork()))
        rc = e.set(params).run(fatal=True)

        es = e.tappedEvents()
        for (_, p, _) in es:
            self.assertTrue(p == model2)



if __name__ == '__main__':
    unittest.main()
