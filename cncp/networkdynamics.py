# Networks dynamics simulation base class
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import epyc
import networkx


class Dynamics(epyc.Experiment, object):
    '''A dynamical process over a network. This is the abstract base class
    for implementing different kinds of dynamics as computational experiments
    suitable for running under. Sub-classes provide synchronous and stochastic
    (Gillespie) simulation dynamics.'''

    # keys for node and edge attributes
    DYNAMICAL_STATE = 'state'   #: dynamical state of a node
    OCCUPIED = 'occupied'       #: edge has been used to transfer infection or not

    # the default maximum simulation time
    DEFAULT_MAX_TIME = 20000
    
    def __init__( self, g = None ):
        '''Create a dynamics, optionally initialised to run on the given network.
        The network (if provided) is treated as a prototype that is copied before
        each individual simulation experiment.
        
        :param g: prototype network (optional)'''
        super(Dynamics, self).__init__()
        self._graphPrototype = g
        self._graph = None
        self._maxTime = self.DEFAULT_MAX_TIME

    def network( self ):
        '''Return the network this dynamics is running over.

        :returns: the network'''
        return self._graph

    def setNetworkPrototype( self, g ):
        '''Set the network the dynamics will run over. This will be
        copied for each run of an individual experiment.

        :param g: the network'''
        self._graphPrototype = g

    def setMaximumTime( self, t ):
        '''Set the maximum default simulation time. The default is given
        by `DEFAULT_MAX_TIME`.

        param: t: the maximum time'''
        self._maxTime = t
        
    def at_equilibrium( self, t ):
        '''Test whether the model is an equilibrium. The default runs for
        20000 timesteps and then stops. Override this method to provide
        alternative and/or faster simulations.
        
        :param t: the current simulation timestep
        :returns: True if we're done'''
        return (t >= self._maxTime)

    def setUp( self, params ): 
        '''Before each experiment, create a working copy of the prototype network.

        :param params: parameters of the experiment'''
        self._graph = self._graphPrototype.copy()

    def tearDown( self ):
        '''At the end of each experiment, throw away the copy.'''
        self._graph = None
        
    def skeletonise( self ):
        '''Remove unoccupied edges from the network. This leaves the network
        consisting of only "occupied" edges that were used to transmit the
        infection between nodes.
        
        :returns: the network with unoccupied edges removed'''
        
        # find all unoccupied edges
        g = self.network()
        edges = []
        for n in g.nodes_iter():
            for (np, m, data) in g.edges_iter(n, data = True):
                if (self.OCCUPIED not in data.keys()) or (data[self.OCCUPIED] != True):
                    # edge is unoccupied, mark it to be removed
                    # (safe because there are no parallel edges)
                    edges.insert(0, (n, m))
                    
        # remove all the unoccupied edges in one go
        g.remove_edges_from(edges)
        return g
    
    def populations( self ):
        '''Return a count of the number of nodes in each dynamical state.
        
        :returns: a dict mapping states to number of nodes in that state'''
        g = self.network()
        pops = dict()
        for n in g.nodes_iter():
            s = g.node[n][self.DYNAMICAL_STATE]
            if s not in pops.keys():
                pops[s] = 1
            else:
                pops[s] = pops[s] + 1
        return pops
    
