# Test network dynamics
#
# Copyright (C) 2017 Simon Dobson
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

import epyc
import unittest
import networkx

class NetworkDynamicsTest(unittest.TestCase):

    def testPosting( self ):
        '''Test posting events.'''
        dyn = Dynamics()

        # event function builder, will increment the shared
        # value when fired
        self._v = 0
        def make_ef( w ):
            def ef( t, g, e ):
                self._v = self._v + w
            return ef
        
        # post some events at different times
        dyn.postEvent(1, None, None, make_ef(1))
        dyn.postEvent(2, None, None, make_ef(20))
        dyn.postEvent(3, None, None, make_ef(100))
        dyn.postEvent(4, None, None, make_ef(200))

        # check no events before the first one posted
        self.assertItemsEqual(dyn.pendingEvents(0.5), [])

        # check firing of earliest event
        pefs = dyn.pendingEvents(1)
        self.assertTrue(len(pefs), 1)
        (pefs[0])()                # fire the event
        self.assertTrue(self._v, 1)
        self.assertItemsEqual(dyn.pendingEvents(1), [])

        # check multiple events coming off in the right order
        pefs = dyn.pendingEvents(3)
        self.assertTrue(len(pefs), 2)
        (pefs[0])()
        self.assertTrue(self._v, 21)
        (pefs[1])()
        self.assertTrue(self._v, 121)
        self.assertItemsEqual(dyn.pendingEvents(3), [])

        # check we can run all remaining events
        dyn.runPendingEvents(10)       # a long time in the future
        self.assertTrue(self._v, 321)
        self.assertItemsEqual(dyn.pendingEvents(10), [])
        self.assertItemsEqual(dyn.pendingEvents(20), [])
        
            
        
                
