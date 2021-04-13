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

import unittest
import os
from tempfile import NamedTemporaryFile
import epyc
import networkx
from epydemic import *


class MonitoredSIR(SIR, Monitor):

    def __init__(self):
        super().__init__()


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
        self.assertSetEqual(set(rc[epyc.Experiment.RESULTS].keys()),
                            set([Monitor.timeSeriesForLocus(SIR.SI),
                                 Monitor.timeSeriesForLocus(SIR.INFECTED),
                                 Monitor.OBSERVATIONS,
                                 SIR.SUSCEPTIBLE,
                                 SIR.INFECTED,
                                 SIR.REMOVED]))
        # the next test is >=, not =, because some events may be drawn after the maxiumum time,
        # but the time is short enough that the number of infecteds won't be exhausted beforehand
        n = len(rc[epyc.Experiment.RESULTS][Monitor.OBSERVATIONS])
        self.assertGreaterEqual(n, 100)
        for k in [SIR.SI, SIR.INFECTED]:
            self.assertEqual(len(rc[epyc.Experiment.RESULTS][Monitor.timeSeriesForLocus(k)]), n)

    def testHDF5(self):
        '''Test we can save and retrieve the time series as HDF5.'''
        tf = NamedTemporaryFile()
        tf.close()
        fn = tf.name
        #fn = 'test.h5'

        try:
            nb = epyc.HDF5LabNotebook(fn, create=True)
            lab = epyc.Lab(nb)

            # run the experiment
            m = MonitoredSIR()
            m.setMaximumTime(100)
            e = StochasticDynamics(m, networkx.erdos_renyi_graph(1000, 5.0 / 1000))
            lab[SIR.P_INFECTED] = 0.01
            lab[SIR.P_INFECT] = 0.002
            lab[SIR.P_REMOVE] = 0.002
            lab[Monitor.DELTA] = 1.0
            rc = lab.runExperiment(e)
            df = lab.dataframe()

            # check we read back in correctly
            with epyc.HDF5LabNotebook(fn).open() as nb1:
                df1 = nb1.dataframe()
                r = df.iloc[0]
                r1 = df1.iloc[0]
                for f in [Monitor.OBSERVATIONS, Monitor.timeSeriesForLocus(SIR.SI), Monitor.timeSeriesForLocus(SIR.INFECTED)]:
                    self.assertCountEqual(r[f], r1[f])
        finally:
            try:
                os.remove(fn)
                #pass
            except OSError:
                pass


if __name__ == '__main__':
    unittest.main()
