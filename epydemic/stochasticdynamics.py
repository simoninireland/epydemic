# Gillespie dynamics base class
#
# Copyright (C) 2017--2022 Simon Dobson
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

import math
from typing import Dict, Any, Union
from networkx import Graph
from epydemic import Dynamics, rng, Process, NetworkGenerator


class StochasticDynamics(Dynamics):
    '''A dynamics that runs stochastically in :term:`continuous
    time`. This is a very efficient and statistically exact approach,
    but requires that the statistical properties of the events making
    up the process are known. See Gillespie
    :cite:`Gillespie76,Gillespie77` for a discussion of the technique.

    :param p: the process to run
    :param g: network or network generator (optional, can be provided later)

    '''

    def __init__(self, p: Process, g: Union[Graph, NetworkGenerator] = None):
        super().__init__(p, g)

    def do(self, params: Dict[str, Any]) -> Dict[str, Any]:
        '''Run the simulation using Gillespie dynamics.

        :param params: the experimental parameters
        :returns: the experimental results dict'''
        self.simulationStarted(params)

        proc = self.process()
        t = 0
        events = 0
        while not proc.atEquilibrium(t):
            # pull the transition dynamics at this timestep
            transitions = self.eventRateDistribution(t)

            # compute the total rate of transitions for the entire network
            a = 0.0
            for (_, r, _, _) in transitions:
                a += r
            if a == 0.0:
                # no events with non-zero rates, check for posted events
                et = self.nextPendingEventTime()
                if et is None:
                    # no pending events either, so we're done
                    break
                else:
                    # run the event
                    events += self.runPendingEvents(et)
                    t = et
            else:
                # we have stochastic events to run

                # shuffle the transitions
                #random.shuffle(transitions)

                # calculate the timestep delta
                r1 = rng.random()
                dt = (1.0 / a) * math.log(1.0 / r1)

                # calculate which event happens
                (l, _, ef, name) = transitions[0]
                if len(transitions) > 1:
                    # choose the rate threshold
                    r2 = rng.random()
                    xc = r2 * a

                    # find the largest event for which the cumulative rates
                    # are less than the random threshold
                    xs = 0
                    for v in range(len(transitions)):
                        (l, xsp, ef, name) = transitions[v]
                        if (xs + xsp) > xc:
                            break
                        else:
                            xs += xsp

                # compute increment to the simulation time
                nt = t + dt

                # fire any events posted for at or before this time
                events += self.runPendingEvents(nt)

                # update the simulation time
                t = nt
                self.setCurrentSimulationTime(t)

                # it's possible that posted events have removed all elements
                # from the chosen locus, in which case we simply continue
                # with the next event selection
                # sd: is this correct? or does it mess up the statistics too much?
                if len(l) > 0:
                    # draw a random element from the chosen locus
                    e = l.draw()

                    # perform the event by calling the event function,
                    # passing the event time and element
                    ef(t, e)
                    self.eventFired(t, l.process(), name, e)

                    # increment the event counter
                    events += 1

        # if we get here through hitting equilibrium then any
        # posted events will be discarded and any possible stochastic
        # events won;t be drawn: equilibriom essentially overrides
        # everything else

        # add some more metadata
        (self.metadata())[self.TIME] = t
        (self.metadata())[self.EVENTS] = events

        # generate and return experimental results
        res = self.experimentalResults()
        self.simulationEnded(res)
        return res
