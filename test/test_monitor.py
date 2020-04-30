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

    def testSimple( self ):
        '''Test we capture the right time series.'''
        m = MonitoredSIR()
        m.setMaximumTime(100)
        e = StochasticDynamics(m, networkx.erdos_renyi_graph(1000, 5.0 / 1000))

        param = dict()
        param[SIR.P_INFECTED] = 0.01
        param[SIR.P_INFECT] = 0.002
        param[SIR.P_REMOVE] = 0.002
        param[Monitor.DELTA] = 1.0

        rc = e.set(param).run()
        self.assertIn(Monitor.TIMESERIES, rc[epyc.Experiment.RESULTS])
        self.assertSetEqual(set(rc[epyc.Experiment.RESULTS].keys()), set([Monitor.TIMESERIES, SIR.SUSCEPTIBLE, SIR.INFECTED, SIR.REMOVED]))
        self.assertSetEqual(set(rc[epyc.Experiment.RESULTS][Monitor.TIMESERIES].keys()), set([Monitor.OBSERVATIONS, SIR.SI, SIR.INFECTED]))
        # the next test is >=, not =, because some events may be drawn after the maxiumum time,
        # but the time is short enough that the number of infecteds won't be exhausted beforehand
        self.assertGreaterEqual(len(rc[epyc.Experiment.RESULTS][Monitor.TIMESERIES][Monitor.OBSERVATIONS]), 100)
        n = len(rc[epyc.Experiment.RESULTS][Monitor.TIMESERIES][Monitor.OBSERVATIONS])
        for k in [SIR.SI, SIR.INFECTED]:
            self.assertEqual(len(rc[epyc.Experiment.RESULTS][Monitor.TIMESERIES][k]), n)

if __name__ == '__main__':
    unittest.main()