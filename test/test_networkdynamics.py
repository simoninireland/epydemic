# Test network dynamics
#
# Copyright (C) 2017--2021 Simon Dobson
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

import unittest
from epydemic import *
from epyc import Experiment


class NetworkDynamicsTest(unittest.TestCase):

    def pendingEvents(self, dyn, t):
        '''Return all the events posted to occur at or before time t.

        :param dyn: the dynamics
        :param t: the time
        :returns: the events'''
        evs = []
        while True:
            ev = dyn.nextPendingEventBefore(t)
            if ev is None:
                break
            else:
                evs.append(ev)
        return evs

    def testPosting( self ):
        '''Test posting events.'''
        p = Process()
        dyn = Dynamics(p)

        # event function builder, will increment the shared
        # value when fired
        self._v = 0
        def make_ef( w ):
            def ef( t, e ):
                self._v = self._v + w
            return ef

        # post some events at different times
        dyn.postEvent(1, None, make_ef(1))
        dyn.postEvent(2, None, make_ef(20))
        dyn.postEvent(3, None, make_ef(100))
        dyn.postEvent(4, None, make_ef(200))

        # check no events before the first one posted
        self.assertCountEqual(self.pendingEvents(dyn, 0.5), [])

        # check firing of earliest event
        pevs = self.pendingEvents(dyn, 1)
        self.assertTrue(len(pevs), 1)
        (_, _, pef, _, _) = pevs[0]
        pef()                # fire the event
        self.assertTrue(self._v, 1)
        self.assertCountEqual(self.pendingEvents(dyn, 1), [])

        # check multiple events coming off in the right order
        pevs = self.pendingEvents(dyn, 3)
        self.assertTrue(len(pevs), 2)
        (_, _, pef, _, _) = pevs[0]
        pef()
        self.assertTrue(self._v, 21)
        (_, _, pef, _, _) = pevs[0]
        pef()
        self.assertTrue(self._v, 121)
        self.assertCountEqual(self.pendingEvents(dyn, 3), [])

        # check we can run all remaining events
        dyn.runPendingEvents(10)       # a long time in the future
        self.assertTrue(self._v, 321)
        self.assertCountEqual(self.pendingEvents(dyn, 10), [])
        self.assertCountEqual(self.pendingEvents(dyn, 20), [])

    def testPostedPosting(self):
        '''Test the case when a posted event itself posts an event.'''
        p = Process()
        dyn = Dynamics(p)

        # event function builder, will increment the shared
        # value when fired and also post a further event
        self._v = 0
        def make_ef(dt):
            def ef(t, e):
                self._v = self._v + 1
                p.postEvent(t + dt, None, make_ef(dt))
            return ef

        # post the first of the events
        p.postEvent(1, None, make_ef(5))

        # post an intermediate event that should be fired alongside a regular one
        def inter(t, e):
            self._v = self._v + 1000
        p.postEvent(12, None, inter)

        # carefully run the event sequence for a while
        for t in range(1, 25, 5):
            nev = dyn.runPendingEvents(t)
            v = self._v
            if t == 1:
                self.assertEqual(v, 1)
                self.assertEqual(nev, 1)
            if t == 6:
                self.assertEqual(v, 2)
                self.assertEqual(nev, 1)
            if t == 11:
                self.assertEqual(v, 3)
                self.assertEqual(nev, 1)
            if t == 16:
                self.assertEqual(v, 1004)
                self.assertEqual(nev, 2)
            if t == 21:
                self.assertEqual(v, 1005)
                self.assertEqual(nev, 1)

        # should be one event left
        self.assertEqual(len(self.pendingEvents(dyn, 100)), 1)

    def testRepeating(self):
        '''Test that repeating events repeat properly.'''
        p = Process()
        dyn = Dynamics(p)

        # event function builder to count the times
        self._ps = []
        def make_ef():
            def ef(t, e):
                self._ps.append((t))
            return ef

        # post a repeating event
        p.postRepeatingEvent(1, 3, None, make_ef())
        for t in range(20):
            dyn.runPendingEvents(t)

        # should be one event left
        self.assertEqual(len(self.pendingEvents(dyn, 100)), 1)

        # check list of times
        self.assertEqual(self._ps, [1, 4, 7, 10, 13, 16, 19])

    def testNoLoci(self):
        '''Test we can handle processes without loci.'''
        p = Process()
        dyn = Dynamics(p)
        self.assertCountEqual(dyn.lociForProcess(p), dict())

    def testTopologyMarjer(self):
        '''Test we get a topology marker in the experimental parameters.'''
        params = dict()
        params[SIR.P_INFECTED] = 0.01
        params[SIR.P_INFECT] = 0.02
        params[SIR.P_REMOVE] = 0.01
        params[ERNetwork.N] = 2000
        params[ERNetwork.KMEAN] = 5

        p = SIR()
        gen = ERNetwork()
        e = StochasticDynamics(p, gen)
        rc = e.set(params).run(fatal=True)

        self.assertIn(NetworkGenerator.TOPOLOGY, rc[Experiment.PARAMETERS])
        self.assertEqual(rc[Experiment.PARAMETERS][NetworkGenerator.TOPOLOGY], gen.topology())


if __name__ == '__main__':
    unittest.main()
