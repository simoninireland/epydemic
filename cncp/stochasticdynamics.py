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
    '''A dynamics that runs stochastically, skipping timesteps in which nothing changes.'''
        
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given network.
        
        g: prototype network to run the dynamics over (optional)'''
        super(StochasticDynamics, self).__init__(g)

    def transitions( self, t, params ):
        '''Return the transition vector, a sequence of (r, f) pairs
        where r is the rate at which a transition happens and
        f is the transition function called to make it happen. Note that
        it's a rate we want, not a probability.
        
        It's important that the transitions always come in the same order
        in the vector, even though the rates (and indeed functions) can
        change over time.

        The transition functions should throw an exception if the transition
        can't happen for whatever reason. This will stop the dynamics and
        not be propagated. (Is this the right behaviour?)
        
        t: timestep for which we want the transitions
        params: the paramneters of the simulation
        returns: the transition vector'''
        raise NotYetImplementedError('transitions()')
        
    def do( self, params ):
        '''Stochastic dynamics. We use the transition probabilities to
        locate trhe next event in time, and then call the appropriate
        event service routine.
        
        params: parameters of the simulation
        returns: a dict of simulation properties'''
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
            try:
                # call the transition function associated with the selected event
                f(t)
            except Exception:
                # if the transition fails, silently stop the dynamics
                break
            
            # increment the event counter and distribution
            events = events + 1
            
            # check for termination
            if self.at_equilibrium(t):
                break
        
        # record statistics
        rc['timesteps'] = t
        rc['events'] = events
        rc['node_types'] = self.populations()        
        return rc

