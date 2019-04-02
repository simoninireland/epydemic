# Mixin class containing common tests for compartmented models
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

from __future__ import print_function
from epydemic import *
import epyc

class CompartmentedDynamicsTest():

    def setUp( self ):
        '''Set up for the specific model under test. This should fill in
        self._network, self._model, self._params, self._maxTime, 
        and self._lab as required.'''
        raise NotImplementedError('setUp')

    def testRunSingleStochastic( self ):
        '''Test a single run of a stochastic dynamics.'''
        e = StochasticDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.EXCEPTION])
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
    
    def testRunSingleSynchronous( self ):
        '''Test a single run of a synchronous dynamics.'''
        e = SynchronousDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.EXCEPTION])
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
        
    def testRunMultipleStochastic( self ):
        '''Test a stochastic dynamics run of a model over a (small) parameter space.'''
        e = StochasticDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        self._lab.runExperiment(e)

    def testRunMultipleSynchronous( self ):
        '''Test a synchronous dynamics run of a model over a (small) parameter space.'''
        e = SynchronousDynamics(self._model, self._network)
        if self._maxTime is not None:
            e.setMaximumTime(self._maxTime)
        self._lab.runExperiment(e)
