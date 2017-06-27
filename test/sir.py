# Test SIR under different dynamics
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
from .compartmenteddynamics import CompartmentedDynamicsTest

import epyc
import unittest
import networkx

class SIRTest(CompartmentedDynamicsTest):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        
        # single experiment
        self._params = dict(pInfect = 0.1,
                            pInfected = 0.01,
                            pRemove = 0.05)
        self._network = networkx.erdos_renyi_graph(1000, 0.005)

        # lab run
        self._lab = epyc.Lab()
        self._lab['pInfect'] = [ 0.1, 0.2, 0.3 ]
        self._lab['pInfected'] = [ 0.01 ]
        self._lab['pRecover'] = [ 0.05, 0.1, 1 ]

        # model
        self._model = SIR()

        # no maximum time needed
        self._maxTime = None
