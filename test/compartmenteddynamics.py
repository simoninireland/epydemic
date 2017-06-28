# Base class for testing compartmented models under different dynamics
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
import traceback

class CompartmentedDynamicsTest(unittest.TestCase):

    def setUp( self ):
        '''Set upo for the specific model under test. This should fill in
        self._network, self._model, self._params, self._maxTime, 
        and self._lab as required.'''
        raise NotYetImplementyed('setUp')

    def testRunSingleStochastic( self ):
        '''Test a single run of a stochastic dynamics.'''
        e = CompartmentedStochasticDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print rc[epyc.Experiment.METADATA][epyc.Experiment.EXCEPTION]
            traceback.print_tb(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
    
    def testRunSingleSynchronous( self ):
        '''Test a single run of a synchronous dynamics.'''
        e = CompartmentedSynchronousDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print rc[epyc.Experiment.METADATA][epyc.Experiment.EXCEPTION]
            traceback.print_tb(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
        
    @unittest.skip('not yet')
    def testRunMultipleStochastic( self ):
        '''Test a stochastic dynamics run of a model over a (small) parameter space.'''
        e = CompartmentedStochasticDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        self._lab.runExperiment(e)

    @unittest.skip('not yet')
    def testRunMultipleSynchronous( self ):
        '''Test a synchronousdynamics run of a model over a (small) parameter space.'''
        e = CompartmentedSynchronousDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        self._lab.runExperiment(e)
