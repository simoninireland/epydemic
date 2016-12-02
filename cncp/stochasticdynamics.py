# Gillespie dynamics base class
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp
import epyc
import math
import numpy
import networkx


class StochasticDynamics(cncp.Dynamics):
    '''A dynamics that runs stochastically in continuous time. This is a
    very efficient and statistically exact approach, but requires that the
    statistical properties of the events making up the process are known.'''
        
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given network.
        
        :param g: prototype network to run the dynamics over (optional)'''
        super(StochasticDynamics, self).__init__(g)

    def transitions( self, t, params ):
        '''Return the transition vector, a sequence of (r, f) pairs
        where r is the rate at which a transition happens and
        f is the transition function called to make it happen. This method
        must be overridden in sub-classes. Note that it's a rate we want,
        not a probability. The former can be obtained from the latter
        simply by multiplying the event probability by the number of
        times it's possible in the network, which is often a population of
        nodes in a given state.
        
        It is perfectly fine for an event to have a zero rate. The process
        is assumed to have reached equilibrium if all events have zero rates.

        It's important that the transitions always come in the same order
        in the vector, even though the rates (and indeed functions) can
        change over time.

        :param t: timestep for which we want the transitions
        :param params: the parameters of the simulation
        :returns: the transition vector'''
        raise NotYetImplementedError('transitions()')
        
    def do( self, params ):
        '''Stochastic dynamics. We use the transition probabilities to
        locate the next event in time, and then call the appropriate
        event service routine.
        
        :param params: parameters of the simulation
        :returns: a dict of simulation properties'''
        rc = dict()
        
        # set up the priority list
        transitions = self.transitions(0, params)
        pr = range(len(transitions))
        
        # run the dynamics
        t = 0
        events = 0
        while True:
            # pull the transition dynamics at this timestep
            transitions = self.transitions(t, params)
            
            # compute the total rate of transitions for the entire network
            a = 0.0
            for (r, _) in transitions:
                a = a + r
            if a == 0:       # no events with non-zero rates 
                break
            
            # calculate the timestep delta
            r1 = numpy.random.random()
            dt = (1.0 / a) * math.log(1.0 / r1)
            t = t + dt
            
            # calculate which transition happens
            if len(transitions) == 1:
                # if there's only one, that's the one that happens
                (_, f) = transitions[0]
            else:
                # otherwise, choose one at random based on the rates
                r2 = numpy.random.random()
                xc = r2 * a
                k = 0
                (xs, f) = transitions[pr[k]]
                while xs < xc:
                    k = k + 1
                    (xsp, f) = transitions[pr[k]]
                    xs = xs + xsp

                # if we used a low-priority transition, swap it up the priority queue
                #if k > 0:
                #    p = pr[k - 1]
                #    pr[k - 1] = pr[k]
                #    pr[k] = p       
            
            # perform the transition
            # call the transition function associated with the selected event
            f(t)
            
            # increment the event counter
            events = events + 1
            
            # check for termination
            if self.at_equilibrium(t):
                break
        
        # record statistics
        rc['timesteps'] = t
        rc['events'] = events
        rc['node_types'] = self.populations()        
        return rc

