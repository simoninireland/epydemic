# Test SIR with fixed recovery time under different dynamics
#
# Copyright (C) 2017--2020 Simon Dobson
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
from test.compartmenteddynamics import CompartmentedDynamicsTest
from test.test_sir import SIRTest
import epyc
import unittest
import networkx

class SIRFixedRecoveryTest(SIRTest):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        super().setUp()

        self._params[SIR_FixedRecovery.T_INFECTED] = 1.0
        self._lab[SIR_FixedRecovery.T_INFECTED] = [ 1.0, 2.0 ]

        self._model = SIR_FixedRecovery()


if __name__ == '__main__':
    unittest.main()
