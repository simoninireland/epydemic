# Test the behaviour of the addition-deletion process
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

from __future__ import print_function
from epydemic import *
from test.compartmenteddynamics import CompartmentedDynamicsTest
import epyc
import unittest
import networkx

class AddDeleteRecorder(AddDelete):

    N = 'networkSize'

    def __init__(self):
        super(AddDeleteRecorder, self).__init__()

    def results( self ):
        '''Save the size of the resulting network.

        :returns: a dict of experimental results'''
        rc = super(AddDeleteRecorder, self).results()
        rc[self.N] = self.network().order()
        return rc


class AddDeleteTest(unittest.TestCase):

    def setUp(self):
        '''Set up the experimental parameters and process.'''
        N = 5000
        kmean = 10
        phi = (kmean + 0.0) / N
        self._network = networkx.erdos_renyi_graph(N, phi)
        self._maxTime = 5000

        self._params = dict()
        self._params[AddDelete.DEGREE] = 10
        self._process = AddDeleteRecorder()
        self._process.setMaximumTime(self._maxTime)
        self._e = StochasticDynamics(self._process, self._network)

    def testRun(self):
        '''Test that the process runs and adds and deletes at roughly equal rates.'''
        self._params[AddDelete.P_ADD] = 1
        self._params[AddDelete.P_DELETE] = 1
        rc = self._e.set(self._params).run()
        self.assertAlmostEqual(rc[epyc.Experiment.RESULTS][AddDeleteRecorder.N], self._network.order(), delta = int((self._network.order() + 0.0) * 0.1))

    def testRunFaster(self):
        '''Test that the process runs and adds faster than it deletes.'''
        self._params[AddDelete.P_ADD] = 1
        self._params[AddDelete.P_DELETE] = 0.5
        rc = self._e.set(self._params).run()
        dn = self._maxTime * (self._params[AddDelete.P_ADD] - self._params[AddDelete.P_DELETE])
        self.assertAlmostEqual(rc[epyc.Experiment.RESULTS][AddDeleteRecorder.N], self._network.order() + dn, delta = int((self._network.order() + 0.0) * 2 * 0.1))
