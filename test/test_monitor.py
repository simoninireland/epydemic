# Test process monitoring
#
# Copyright (C) 2020 Simon Dobson
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
import unittest
import epyc
import networkx

class MonitoredSIR(SIR, Monitor):
    
    def __init__(self):
        super(MonitoredSIR, self).__init__()


class MonitorTest(unittest.TestCase):

    def testNoInfection( self ):
        '''Test we capture an empty time series when there's no infection.'''
        m = MonitoredSIR()
        m.setMaximumTime(500)
        e = StochasticDynamics(m, networkx.erdos_renyi_graph(1000, 5.0 / 1000))

        param = dict()
        param[SIR.P_INFECTED] = 0.0
        param[SIR.P_INFECT] = 0.002
        param[SIR.P_REMOVE] = 0.002
        param[Monitor.DELTA] = 0.001

        rc = e.set(param).run()
        print(rc)
        self.assertTrue(len([ l for (_, l) in rc[epyc.Experiment.RESULTS][Monitor.TIMESERIES][SIR.INFECTED] if l > 0 ]), 0)

