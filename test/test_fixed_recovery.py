# Test the SIR and SIS fixed-time recovery variants
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
from test.compartmenteddynamics import CompartmentedDynamicsTest
import epyc
import unittest
import networkx

class FixedRecoveryTest(unittest.TestCase):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        
        # single experiment
        self._params = dict()
        self._params[SIR_FixedRecovery.P_INFECT] = 0.1
        self._params[SIR_FixedRecovery.P_INFECTED] = 0.01
        self._params[SIR_FixedRecovery.T_INFECTED] = 1
        self._network = networkx.erdos_renyi_graph(1000, 0.005)

        # lab run
        self._lab = epyc.Lab()
        self._lab[SIR_FixedRecovery.P_INFECT] = [ 0.1, 0.3 ]
        self._lab[SIR_FixedRecovery.P_INFECTED] = [ 0.01 ]
        self._lab[SIR_FixedRecovery.T_INFECTED] = [ 0.5, 1, 2 ]

    def testRunSingleSIRSynchronous( self ):
        '''Test a single run of a fixed-period SIR under synchronous dynamics.'''
        e = CompartmentedSynchronousDynamics(SIR_FixedRecovery(), self._network)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.EXCEPTION])
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])

    def testRunSingleSIRStochastic( self ):
        '''Test a single run of a fixed-period SIR under stochastic dynamics.'''
        e = CompartmentedStochasticDynamics(SIR_FixedRecovery(), self._network)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.EXCEPTION])
            print(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
  
