# Process combinator to build sequences of processes
#
# Copyright (C) 2017--2021 Simon Dobson
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

from epydemic import Process, Dynamics
from typing import List, Dict, Any

class ProcessSequence(Process):
    '''A process build from a sequence of other processes. This allows separate process
    behaviour to be defined independently and then combined in different ways.
    
    :param ps: the processes'''

    def __init__(self, ps : List[Process]):
        self._processes = ps
        super(ProcessSequence, self).__init__()
        
    def setDynamics(self, d : Dynamics):
        '''Set the dynamics.

        :param d: the dynamics'''
        super(ProcessSequence, self).setDynamics(d)
        for p in self._processes:
            p.setDynamics(d)

    def reset(self):
        '''Reset the processes.'''
        for p in self._processes:
            p.reset()
            
    def build(self, params : Dict[str, Any]):
        '''Build the proceses.
        
        :param params: the experimental parameters'''
        for p in self._processes:
            p.build(params)
            
    def setUp(self, params : Dict[str, Any]):
        '''Set up the proceses.
        
        :param params: the experimental parameters'''
        for p in self._processes:
            p.setUp(params)
            
    def tearDown(self):
        '''Tear down the processes.'''
        for p in self._processes:
            p.tearDown()
            
    def atEquilibrium(self, t : float):
        '''Test for equilibrium. A process sequence is at equilibrium if and when all
        its component processes are.
        
        :param t: the simulation time
        :returns: True if all the processes are at equilibrium'''
        for p in self._processes:
            if not p.atEquilibrium(t):
                return False
        return True

    def setMaximumTime(self, t : float):
        '''Set the maximum default simulation time for all processes

        :param t: the maximum simulation time'''
        for p in self._processes:
            p.setMaximumTime(t)

    def maximumTime(self) -> float:
        '''Return the maximum assumed simulation time, which is the maximum
        of all component processes.

        :returns: the maximum simulation time'''
        t = 0
        for p in self._processes:
            t = max(t, p.maximumTime())
        return t

    def results(self) -> Dict[str, Any]:
        '''Return all the experimental results from all the processes. The dict
        is created in process order, meaning that later processes may alter or overwrite
        the results of earlier ones, accidentally or deliberately.
        
        :returns: a dict of experimental results'''
        res = super(ProcessSequence, self).results()
        for p in self._processes:
            res.update(p.results())
        return res
        