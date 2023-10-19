# Networks experiment base class
#
# Copyright (C) 2017--2023 Simon Dobson
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

from typing import Union, Dict, Any, List, cast
from networkx import Graph
from epyc import Experiment
from epydemic import NetworkGenerator, FixedNetwork, Process, Element


class NetworkExperiment(Experiment):
    '''A very lightweight base class for providing a network to an
    :ref:`experiment <epyc:experiment-class>`. The network can either
    be a fixed network used for each experimental run, or a network
    generator that will be used to generate a new instance for each
    run.

    The experiment also provides the interface for :ref:`event-taps`,
    allowing external code to tap-into the changes the experiment makes
    to the network. Sub-classes need to insert calls to this interface
    as appropriate, notably around the main body of the simulation and
    at each significant change.

    :param g: (optional) prototype network or network generator

    '''
    def __init__(self, g: Union[Graph, NetworkGenerator] = None):
        super().__init__()

        # turn a literal network into a network generator
        if isinstance(g, Graph):
            g = FixedNetwork(g)
        self._generator: NetworkGenerator = cast(NetworkGenerator, g) # network generator
        self._graph: Graph = None                                     # working network instance

        # initialise the event tap sub-system
        self.initialiseEventTaps()


    # ---------- Configuration ----------

    def network(self) -> Graph:
        '''Return the network this dynamics is running over. This will return
        None unless we're actually running a simulation.

        :returns: the network

        '''
        return self._graph

    def setNetworkGenerator(self, g: Union[Graph, NetworkGenerator]):
        '''Set the network or generator for the networks the dynamics will run
        over.  If a network is supplied rather than a generator it
        will be treated as an instance of :class:`FixedNetwork`.

        Note that calling this method doesn't change the working
        network mid-experiment: for that, use
        :meth:`NetworkExperiment.setNetwork`.

        :param g: network or network generator

        '''
        if isinstance(g, Graph):
            g = FixedNetwork(g)
        self._generator = g

    def setNetwork(self, g: Graph):
        '''Set the working network. This changes the current working network
        immediately (i.e., within a running experiment): to change how
        initial working networks are obtained, use
        :meth:`NetworkExperiment.setNetworkGenerator`.

        :param g: the network

        '''
        self._graph = g

    def networkGenerator(self) -> NetworkGenerator:
        '''Return the generator used for this dynamics.

        :returns: the generator'''
        return self._generator


    # ---------- Set-up ----------

    def setUp(self, params: Dict[str, Any]):
        '''Set up the experiment for a run. This creates a working copy of the
        network (class) underlying the experiment.

        :param params: the experimental parameters
        '''
        super().setUp(params)

        # delete any working network from previous runs
        self._graph = None

        # generate a working network instance
        gen = self.networkGenerator()
        g = gen.set(params).generate()
        self.setNetwork(g)

        # update the parameters with the topology marker for the generator
        params[NetworkGenerator.TOPOLOGY] = gen.topology()


    # ---------- Event taps ----------

    def initialiseEventTaps(self):
        '''Initialise the event tap sub-system, which allows external code
        access to the event stream of the simulation as it runs.

        The default does nothing.'''
        pass

    def simulationStarted(self, params: Dict[str, Any]):
        '''Called when the simulation has been configured and set up, any
        processes built, and is ready to run.

        The default does nothing.

        :param params: the experimental parameters'''
        pass

    def simulationEnded(self, res: Union[Dict[str, Any], List[Dict[str, Any]]]):
        '''Called when the simulation has stopped, immediately before tear-down.

        The default does nothing.

        :param res: the experimental results'''
        pass

    def eventFired(self, t: float, p: Process, name: str, e: Element):
        '''Respond to the occurrance of the given event. The method is
        passed the simulation time, originating process, event name,
        and the element affected -- and isn't passed the event
        function, which is used elsewhere. p will be None if the event
        is not associated with a :class:`Process` instance.

        This method is called in the past tense, *after* the event has
        happened. This lets the effects of the event be observed from
        within the tap.

        The event name is simply the optional name to differentiate
        between different kinds of event. When used from
        :class:`Dynamics`, event names are generated automatically
        from the names associated with event handlers when they are
        defined in the corresponding :class:`Process`, using
        :meth:`Process.addEventPerElement` or :meth:`Process.addFixedRateEvent`.

        The default does nothing. It can be overridden by sub-classes to
        provide event-level logging or other functions.

        :param t: the simulation time
        :param p: the process firing the event
        :param name: the event name
        :param e: the element

        '''
        pass
