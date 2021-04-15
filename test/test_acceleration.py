# Test accelerated Gillespie algorithms
#
# Copyright (C) 2021 Simon Dobson
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

from time import time
import unittest
from epydemic import *
import epyc
import networkx


class AccelerationTest(unittest.TestCase):

    def setUp(self):
        '''Set up the experimental parameters and process.'''
        N = 100000
        kmean = 10

        self._params = dict()
        self._params[SIR.P_INFECT] = 0.05
        self._params[SIR.P_REMOVE] = 0.01
        self._params[SIR.P_INFECTED] = 0.001
        self._params[ERNetwork.N] = N
        self._params[ERNetwork.KMEAN] = kmean

    def testBase(self):
        '''Benchmark the base algorithm.'''
        e = StochasticDynamics(SIR(), ERNetwork())
        start = time()
        rc = e.set(self._params).run()
        end = time()
        t = end - start
        print(f'Base algorithm {t}s')


if __name__ == '__main__':
    unittest.main()
