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
    '''A dynamics that runs stochastically in continuous time. This is a
    very efficient and statistically exact approach, but requires that the
    statistical properties of the events making up the process are known.'''

    # Additional metadata elements
    TIME = 'simulation_time'      #: Metadata element holding the logical simulation end-time
    EVENTS = 'simulation_events'  #: Metadata element holding the number of events that happened
    
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given network.
        
        :param g: prototype network to run the dynamics over (optional)'''
        super(StochasticDynamics, self).__init__(g)

    def eventRateDistribution( self, t ):
        '''Return the event distribution, a sequence of (r, f) pairs
        where r is the rate at which an event happens and
        f is the event function called to make it happen. This method
        must be overridden in sub-classes. Note that it's a rate we want,
        not a probability: the former can be obtained from the latter
        simply by multiplying the event probability by the number of
        times it's possible in the current network, which is often a
        population of nodes or edges in a given state.
        
        It is perfectly fine for an event to have a zero rate. The process
        is assumed to have reached equilibrium if all events have zero rates.

        :param t: current time
        :returns: the event rate distribution'''
        raise NotYetImplementedError('eventRateDistribution()')

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

            # advance time by the timestep
            t = t + dt
            
            # calculate which transition happens
            if len(transitions) == 1:
                # if there's only one, that's the one that happens
                (l, _, f) = transitions[0]
            else:
                # otherwise, choose one at random based on the rates
                r2 = numpy.random.random()
                xc = r2 * a
                k = 0
                (l, xs, f) = transitions[k]
                while xs < xc:
                    k = k + 1
                    (l, xsp, f) = transitions[k]
                    xs = xs + xsp

            # drawe a random element from the chosen locus
            e = l.draw()
            
            # perform the event by calling the event function
            f(t, l, g, e)
            
            # increment the event counter
            events = events + 1

        # add some more metadata
        (self.metadata())[self.TIME] = t
        (self.metadata())[self.EVENTS] = events

        # report results
        rc = self.experimentalResults()
        return rc

