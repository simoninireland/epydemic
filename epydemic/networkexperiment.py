# Networks experiment base class
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

from epyc import Experiment
from epydemic import NetworkGenerator, FixedNetwork
from networkx import Graph
from typing import Union, Dict, Any, cast


class NetworkExperiment(Experiment):
    '''A very lightweight base class for providing a network
    to an `epyc` experiment. The network can either be a fixed network
    used for each experimental run, or a network generator that will be 
    used to generate a new instance for each run.
    
    :param g: (optional) prototype network or network generator'''
    def __init__(self, g : Union[Graph, NetworkGenerator] =None):
        super(NetworkExperiment, self).__init__()

        # turn a literal network into a network generator
        if isinstance(g, Graph):
            g = FixedNetwork(g)
        self._generator = cast(NetworkGenerator, g)       # network generator
        self._graph : Graph = None                        # working network instance


    # ---------- Configuration ----------

    def network(self) -> Graph:
        '''Return the network this dynamics is running over. This will return None
        unless we're actually running a simulation.

        :returns: the network'''
        return self._graph

    def setNetworkGenerator(self, g : Union[Graph, NetworkGenerator]):
        '''Set the network or generator for the networks the dynamics will run over.
        If a network is supplied rather than a generator it will be treated as an
        instance of :class:`FixedNetwork`.

        :param g: network or network generator'''
        if isinstance(g, Graph):
            g = FixedNetwork(g)
        self._generator = g

    def networkGenerator(self) -> NetworkGenerator:
        '''Return the generator used for this dynamics.

        :returns: the generator'''
        return self._generator


    # ---------- Set-up and tear-down ----------

    def setUp(self, params : Dict[str, Any]):
        '''Set up the experiment for a run. This creates a working copy
        of the network (class) underlying the experiment.

        :params params: the experimental parameters'''
        super(NetworkExperiment, self).setUp(params)

        # generate a working network instance
        self._graph = self.networkGenerator().set(params).generate()

    def tearDown(self):
        '''At the end of each experiment, throw away the working network.'''
        super(NetworkExperiment, self).tearDown()
        self._graph = None

