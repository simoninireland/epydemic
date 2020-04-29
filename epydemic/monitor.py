# Monitor the progress of an epidemic
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

from epydemic import Process

class Monitor(Process):
    '''Add progress monitoring to a process. This class captures the
    sizes of all loci in the process at regular intervals, returning
    them as time series.'''
    
    # Experimental parameters
    DELTA = "time_delta"                #: Parameter for the time interval for observations.
    
    # Results
    TIMESERIES = "loci_timeseries"      #: Result holding a dict mapping locus names to a dict of sample time and size.
 

    def __init__(self):
        super(Monitor, self).__init__()

    def reset(self):
        '''Reset the process.'''
        super(Monitor, self).reset()
        print('reset')
        self._timeSeries = None
        
    def build(self, params):
        '''Build the observation process.
        
        :param params: the experimental parameters'''
        super(Monitor, self).build(params)
        print('build')

        # post a repeating event to observe the process
        delta = params[self.DELTA]
        self.postRepeatingEvent(delta, delta, None, self.observe)
        
    def observe(self, t, e):
        '''Observe the network.
        
        :param t: the current simulation time
        :param e: the element (ignored)'''
        print('observe')

        # if this is the first run, build the initial dicts per locus
        if self._timeSeries is None:
            self._timeSeries = dict()
            for l in self:
                self._timeSeries[l.name()] = dict()

        # make the observation
        for l in self:
            self._timeSeries[l.name()][t] = len(l)
        
    def results(self):
        '''Return the time series.
        
        :returns: the results'''
        rc = super(Monitor, self).results()
        
        # store the series
        rc[self.TIMESERIES] = self._timeSeries
        
        return rc