# Networks-with-dynamics simulation base class
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import networkx


class GraphWithDynamics(networkx.Graph):
    '''A NetworkX undirected network with an associated dynamics. This
    class combines two sets of entwined functionality: a network, and
    the dynamical process being studied. This is the abstract base class
    for studying different kinds of dynamics.'''

    # keys for node and edge attributes
    DYNAMICAL_STATE = 'state'   # dynamical state of a node
    OCCUPIED = 'occupied'       # edge has been used to transfer infection or not

    def __init__( self, g = None ):
        '''Create a graph, optionally with nodes and edges copied from
        the graph given.
        
        g: graph to copy (optional)'''
        networkx.Graph.__init__(self, g)
        if g is not None:
            self.copy_from(g)
        
    def copy_from( self, g ):
        '''Copy the nodes and edges from another graph into us.
        
        g: the graph to copy from
        returns: the copy of the graph'''
        
        # copy in nodes and edges from source network
        self.add_nodes_from(g.nodes_iter())
        self.add_edges_from(g.edges_iter())
        
        # remove self-loops
        es = self.selfloop_edges()
        self.remove_edges_from(es)
        
        return self
    
    def remove_all_nodes( self ):
        '''Remove all nodes and edges from the graph.'''
        self.remove_nodes_from(self.nodes())

    def at_equilibrium( self, t ):
        '''Test whether the model is an equilibrium. The default runs for
        20000 timesteps and then stops.
        
        t: the current simulation timestep
        returns: True if we're done'''
        return (t >= 20000)

    def before( self ):
        '''Placeholder to be run ahead of simulation. Default does nothing.'''
        pass

    def after( self ):
        '''Placeholder to be run after simulation Default does nothing.'''
        pass
    
    def _dynamics( self ):
        '''Internal function defining the way the dynamics works. Must be
        overridden in sub-classes.

        returns: a dict of properties'''
        raise NotYetImplementedError('_dynamics()')
        
    def dynamics( self ):
        '''Run a number of iterations of the model over the network. The
        default simply runs the dynamics once.
        
        returns: a dict of properties'''
        return self._dynamics()

    def skeletonise( self ):
        '''Remove unoccupied edges from the network. This leaves the network
        consisting of only "occupied" edges that were used to transmit the
        infection between nodes.
        
        returns: the network with unoccupied edges removed'''
        
        # find all unoccupied edges
        edges = []
        for n in self.nodes_iter():
            for (np, m, data) in self.edges_iter(n, data = True):
                if (self.OCCUPIED not in data.keys()) or (data[self.OCCUPIED] != True):
                    # edge is unoccupied, mark it to be removed
                    # (safe because there are no parallel edges)
                    edges.insert(0, (n, m))
                    
        # remove all the unoccupied edges in one go
        self.remove_edges_from(edges)
        return self
    
    def populations( self ):
        '''Return a count of the number of nodes in each dynamical state.
        
        returns: a dict mapping states to number of nodes in that state'''
        pops = dict()
        for n in self.nodes_iter():
            s = self.node[n][self.DYNAMICAL_STATE]
            if s not in pops.keys():
                pops[s] = 1
            else:
                pops[s] = pops[s] + 1
        return pops
    
