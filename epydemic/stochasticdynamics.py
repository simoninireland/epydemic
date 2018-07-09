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

import epyc
import math
import numpy

class StochasticDynamics(Dynamics):
    '''A dynamics that runs stochastically in :term:`continuous time`. This is a
    very efficient and statistically exact approach, but requires that the
    statistical properties of the events making up the process are known.

    :param g: prototype network to run the dynamics over (optional)'''

    def __init__( self, g = None ):
        super(StochasticDynamics, self).__init__(g)

    def eventRateDistribution( self, t ):
        '''Return the event distribution, a sequence of (l, r, f) triples
        where l is the locus where the event occurs, r is the rate at
        which an event occurs, and f is the event function called to
        make it happen.

        Note that it's a rate we want, not a probability:
        the former can be obtained from the latter simply by
        multiplying the event probability by the number of times it's
        possible in the current network, which is the population
        of nodes or edges in a given state.
        
        It is perfectly fine for an event to have a zero rate. The process
        is assumed to have reached equilibrium if all events have zero rates.

        :param t: current time
        :returns: the event rate distribution'''
        dist = self.eventDistribution(t)
        return map((lambda l, p, f: (l, p * len(l), f)), dist)

    def do( self, params ):
        '''Run the simulation using Gillespie dynamics. The process terminates
        when either there are no events with zero rates or when :meth:`at_equilibrium`
        return True.

        :param params: the experimental parameters
        :returns: the experimental results dict'''
        
        # run the dynamics
        g = self.network()
        t = 0
        events = 0
        while not self.at_equilibrium(t):
            # pull the transition dynamics at this timestep
            transitions = self.eventRateDistribution(t)
            
            # compute the total rate of transitions for the entire network
            a = 0.0
            for (_, r, _) in transitions:
                a = a + r
            if a == 0:       
                break              # no events with non-zero rates 
            
            # calculate the timestep delta
            r1 = numpy.random.random()
            dt = (1.0 / a) * math.log(1.0 / r1)
            
            # calculate which event happens
            if len(transitions) == 1:
                # if there's only one, that's the one that happens
                (l, _, ef) = transitions[0]
            else:
                # otherwise, choose one at random based on the rates
                r2 = numpy.random.random()
                xc = r2 * a
                k = 0
                (l, xs, ef) = transitions[k]
                while xs < xc:
                    k = k + 1
                    (l, xsp, ef) = transitions[k]
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
                ef(self, t, g, e)
            
                # increment the event counter    
                events = events + 1

        # run any events posted for before the maximum simulation time
        self.runPendingEvents(self._maxTime)

        # add some more metadata
        (self.metadata())[self.TIME] = t
        (self.metadata())[self.EVENTS] = events

        # report results
        rc = self.experimentalResults()
        return rc

