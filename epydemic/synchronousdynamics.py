# Synchronous dynamics base class
#
# Copyright (C) 2017--2020 Simon Dobson
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
from copy import copy
import numpy                     # type: ignore
from networkx import Graph
from epydemic import Dynamics, Process, NetworkGenerator
if sys.version_info >= (3, 8):
    from typing import Any, Dict, Union, Final
else:
    # backport compatibility with older typing
    from typing import Any, Dict, Union
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

    def __init__(self, p: Process, g: Union[Graph, NetworkGenerator] =None):
        super().__init__(p, g)

    def do(self, params: Dict[str, Any]) -> Dict[str, Any]:
        '''Execute the process under synchronous dynamics.

        :param params: the parameters of the simulation
        :returns: a dict of experimental results'''
        rng = numpy.random.default_rng()
        proc = self.process()
        t = 1.0
        events = 0
        timestepEvents = 0
        while not proc.atEquilibrium(t):
            self.setCurrentSimulationTime(t)

            # fire any events posted for at or before this time
            nev = self.runPendingEvents(t)

            # run through all the events in the distribution
            dist = self.perElementEventDistribution(proc, t)
            for (l, p, ef, name) in dist:
                if (len(l) > 0) and (p > 0.0):
                    # run through every possible element on which this event may occur
                    for e in copy(l):
                        # test for occurrance of the event on this element
                        if rng.random() <= p:
                            # yes, perform the event
                            ef(t, e)
                            self.eventFired(t, name, e)
                            nev = nev + 1

            # run through all the fixed-rate events for this timestep
            dist = self.fixedRateEventDistribution(proc, t)
            for (l, p, ef, name) in dist:
                if (len(l) > 0) and (p > 0.0):
                    if rng.random() <= p:
                        # yes, perform the event on an element drawn at random
                        e = l.draw()
                        ef(t, e)
                        self.eventFired(t, name, e)
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
        rc = self.experimentalResults()
        return rc
