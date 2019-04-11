# Gillespie dynamics base class
#
# Copyright (C) 2017 Simon Dobson
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

import math
import numpy

class StochasticDynamics(Dynamics):
    '''A dynamics that runs stochastically in :term:`continuous time`. This is a
    very efficient and statistically exact approach, but requires that the
    statistical properties of the events making up the process are known.

    :param p: the process to run
    :param g: prototype network to run the dynamics over (optional, can be provided later)'''

    def __init__( self, p, g = None ):
        super(StochasticDynamics, self).__init__(p, g)

    def do( self, params ):
        '''Run the simulation using Gillespie dynamics. The process terminates
        when either there are no events with zero rates or when :meth:`at_equilibrium`
        returns True.

        :param params: the experimental parameters
        :returns: the experimental results dict'''
        
        # run the dynamics
        g = self.network()
        proc = self.process()
        t = 0
        events = 0
        while not proc.atEquilibrium(t):
            # pull the transition dynamics at this timestep
            transitions = proc.eventRateDistribution(t)

            # compute the total rate of transitions for the entire network
            a = 0.0
            for (_, r, _) in transitions:
                a = a + r
            if a == 0.0:       
                break              # no events with non-zero rates 
            
            # shuffle the transitions
            #random.shuffle(transitions)
            
            # calculate the timestep delta
            r1 = numpy.random.random()
            dt = (1.0 / a) * math.log(1.0 / r1)
            
            # calculate which event happens
            (l, _, ef) = transitions[0]
            if len(transitions) > 1:
                # choose the rate threshold
                r2 = numpy.random.random()
                xc = r2 * a

                # find the largest event for which the cumulative rates
                # are less than the random threshold
                xs = 0
                for v in range(0, len(transitions)):
                    (l, xsp, ef) = transitions[v]
                    if (xs + xsp) > xc:
                        break
                    else:
                        xs = xs + xsp

            # increment the time
            t = t + dt

            # fire any events posted for at or before this time
            events = events + self.runPendingEvents(t)

            # it's possible that posted events have removed all elements
            # from the chosen locus, in which case we simply continue
            # with the next event selection
            # sd: is this correct? or does it mess up the statistics too much?
            if len(l) > 0:
                # draw a random element from the chosen locus
                e = l.draw()
            
                # perform the event by calling the event function,
                # passing the dynamics, event time, network, and element
                ef(t, g, e)
            
                # increment the event counter    
                events = events + 1

        # add some more metadata
        (self.metadata())[self.TIME] = t
        (self.metadata())[self.EVENTS] = events

        # report results
        rc = self.experimentalResults()
        return rc

