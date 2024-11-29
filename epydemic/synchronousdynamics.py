# Synchronous dynamics base class
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

import sys
from networkx import Graph
from epydemic import Dynamics, rng, Process, NetworkGenerator, Locus, Element, EventFunction
from typing import Any, Dict, Union, Tuple, List
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final


class SynchronousDynamics(Dynamics):
    '''A dynamics that runs synchronously in discrete time, applying local
    rules to each node in the network. These are simple to understand and
    simple to code for many cases, but can be statistically inexact and slow
    for large systems.

    :param p: the network process to run
    :param g: prototype network to run over (optional)'''

    # additional metadata
    TIMESTEPS_WITH_EVENTS: Final[str] = 'epydemic.dynamics.timesteps_with_events'  #: Metadata element holding the number timesteps that actually had events occur within them

    def __init__(self, p: Process, g: Union[Graph, NetworkGenerator] = None):
        super().__init__(p, g)

    def allEventsInTimestep(self, t: float) -> List[Tuple[Locus, Element, EventFunction, str]]:
        '''Return the list of events to be executed in this timestep.
        This includes both the stochastic and fixed-rate events, but
        does not include posted events.

        By default this method accesses the stochastic event
        distribution and looks at each event type in the order in
        which they were registered by :meth:`Process.build`. It
        chooses those events that should be fired based on the choice
        probability, and returns them in order. It then re-visits the
        distributions for fixed-rate events and choose random elements
        for them to happen on.

        This behaviour can be overridden by sub-classes to provide a
        different ordering for events. The order sometimes has a
        significant impact on the behaviour of the simulation.

        :param t: the simulation time
        :returns: a list of locus, element, event function, and name
        '''
        evs = []

        # stochastic events
        dist = self.perElementEventDistribution(t)
        for (l, p, ef, name) in dist:
            if (len(l) > 0) and (p > 0.0):
                for e in l:
                    # test for occurrance of the event on this element
                    if rng.random() <= p:
                        # yes, record the event element and function
                        evs.append((l, e, ef, name))

        # fixed-rate events
        dist = self.fixedRateEventDistribution(t)
        for (l, p, ef, name) in dist:
            if (len(l) > 0) and (p > 0.0):
                # test for the occurrance of the event
                if rng.random() <= p:
                    # yes, draw a random element of the locus and record it
                    e = l.draw()
                    evs.append((l, e, ef, name))

        return evs

    def do(self, params: Dict[str, Any]) -> Dict[str, Any]:
        '''Execute the process under synchronous dynamics.

        :param params: the parameters of the simulation
        :returns: a dict of experimental results'''
        self.simulationStarted(params)

        proc = self.process()
        t = 1.0
        events = 0
        timestepEvents = 0
        while not proc.atEquilibrium(t):
            self.setCurrentSimulationTime(t)

            # fire any events posted for at or before this time
            nev = self.runPendingEvents(t)

            # run all the stochastic and fixed-rate events
            evs = self.allEventsInTimestep(t)
            for (l, e, ef, name) in evs:
                # test the the element is still in the locus
                if e in l:
                    # yes, fire the event
                    ef(t, e)
                    self.eventFired(t, l.process(), name, e)
                    nev = nev + 1

            # add the events to the count
            events = events + nev
            if nev > 0:
                # we had events happen in this timestep
                timestepEvents += 1

            # advance to the next timestep
            t += 1.0

        # add some more metadata
        (self.metadata())[self.TIME] = t
        (self.metadata())[self.EVENTS] = events
        (self.metadata())[self.TIMESTEPS_WITH_EVENTS] = timestepEvents

        # report results
        res = self.experimentalResults()
        self.simulationEnded(res)
        return res
