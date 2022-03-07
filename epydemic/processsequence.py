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

from typing import List, Dict, Any, Union, cast
from epydemic import Process, Dynamics

class ProcessSequence(Process):
    '''A process build from a sequence of other processes. This allows separate process
    behaviour to be defined independently and then combined in different ways.

    The processes can be defined either by a list or a dict. The former
    generates anonymous processes, which is usually fine; the latter gives
    each component process a name by which it can be retrieved by *other* processes.
    This allows more complex interactions between processes.

    If you need to use non-anonymous process sequences, it's often better to
    define a sub-class to manage all the names, since the component processes
    will almost certainly make assumptions about the existence of the processes
    they need to interact closely with, under a specific name.

    :param ps: the processes'''

    def __init__(self, ps: Union[List[Process], Dict[str, Process]]):
        if isinstance(ps, dict):
            # named processes
            self._processes = list(cast(Dict[str, Process], ps).values())
            self._processNames = ps
        else:
            # list of anonymous processes
            self._processes = ps
            self._processNames = None
        for p in self._processes:
            p.setContainer(self)
        super().__init__()


    # ---------- Component processes ----------

    def processes(self) -> List[Process]:
        '''Return a list of component processes.

        :returns: a list of processes'''
        return self._processes

    def processNames(self) -> List[str]:
        '''Return a list of component process names. This will be None
        for anonymous processes.

        :returns: a list of keys or None'''
        if self._processNames is None:
            return None
        else:
            return list(self._processNames.keys())

    def get(self, n: str, v: Process = None) -> Process:
        '''Return the named component process by name, or the default
        value if there is no such process. An exception is raised if the
        process sequence is anonymous.

        :param n: the process name
        :param v: (optional) the default process (defaults to None)
        :returns: the process or the default value'''
        if self._processNames is None:
            raise ValueError('Attempting to retrieve a component process from an anonymous process sequence')
        else:
            return self._processNames.get(n, v)

    def __getitem__(self, n: str) -> Process:
        '''Retrieve a process by name. An exception is raised if the
        process sequence is anonymous or if the named process doesn't exist.

        :param n: the process name
        :returns: the process'''
        p = self.get(n)
        if p is None:
            raise ValueError(f'No component process {n}')
        else:
            return p


    # ---------- Process interface ----------

    def setDynamics(self, d: Dynamics):
        '''Set the dynamics.

        :param d: the dynamics'''
        super().setDynamics(d)
        for p in self.processes():
            p.setDynamics(d)

    def reset(self):
        '''Reset the processes.'''
        for p in self.processes():
            p.reset()

    def build(self, params: Dict[str, Any]):
        '''Build the proceses.

        :param params: the experimental parameters'''
        for p in self.processes():
            p.build(params)

    def setUp(self, params: Dict[str, Any]):
        '''Set up the proceses.

        :param params: the experimental parameters'''
        for p in self.processes():
            p.setUp(params)

    def tearDown(self):
        '''Tear down the processes.'''
        for p in self.processes():
            p.tearDown()

    def atEquilibrium(self, t : float):
        '''Test for equilibrium. A process sequence is at equilibrium if and when all
        its component processes are.

        :param t: the simulation time
        :returns: True if all the processes are at equilibrium'''
        for p in self.processes():
            if not p.atEquilibrium(t):
                return False
        return True

    def setMaximumTime(self, t: float):
        '''Set the maximum default simulation time for all processes

        :param t: the maximum simulation time'''
        for p in self.processes():
            p.setMaximumTime(t)

    def maximumTime(self) -> float:
        '''Return the maximum assumed simulation time, which is the maximum
        of all component processes.

        :returns: the maximum simulation time'''
        t = 0
        for p in self.processes():
            t = max(t, p.maximumTime())
        return t

    def results(self) -> Dict[str, Any]:
        '''Return all the experimental results from all the processes. The dict
        is created in process order, meaning that later processes may alter or overwrite
        the results of earlier ones, accidentally or deliberately.

        :returns: a dict of experimental results'''
        res = super().results()
        for p in self.processes():
            res.update(p.results())
        return res
