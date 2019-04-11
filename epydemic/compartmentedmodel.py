# Compartmented models base class
#
# Copyright (C) 2017--2019 Simon Dobson
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
import numpy
import collections


class CompartmentedNodeLocus(Locus):
    '''A locus for dynamics occurring at a single node, where the
    locus tracks all nodes in a single compartment.

    :param name: the locus' name
    :param c: the compartment'''

    def __init__(self, name, c):
        super(CompartmentedNodeLocus, self).__init__(name)
        self._compartment = c


class CompartmentedEdgeLocus(Locus):
    '''A locus for dynamics occurring at an edge, where the locus tracks all
    edges whose endpoint nodes are in specified compartments.

    :param name: the locus' name
    :param l: the left compartment
    :param r: the right compartment'''

    def __init__(self, name, l, r):
        super(CompartmentedEdgeLocus, self).__init__(name)
        self._left = l
        self._right = r

    def leaveHandler(self, g, n):
        '''Node leaves one of the edge's compartments, remove any incident edges
        that no longer have the correct orientation.

        :param g: the network
        :param n: the node'''
        es = self.elements()
        for (nn, mm) in g.edges(n):
            if (g.node[nn][CompartmentedModel.COMPARTMENT] == self._right) and (g.node[mm][CompartmentedModel.COMPARTMENT] == self._left):
                #print 'edge ({m}, {n}) leaves {l}'.format(n = nn, m = mm, l = self._name)
                es.remove((mm, nn))
            else:
                if (g.node[nn][CompartmentedModel.COMPARTMENT] == self._left) and (g.node[mm][CompartmentedModel.COMPARTMENT] == self._right):
                    #print 'edge ({n}, {m}) leaves {l}'.format(n = nn, m = mm, l = self._name)
                    es.remove((nn, mm))

    def enterHandler(self, g, n):
        '''Node enters one of the edge's compartments, add any incident edges
        that now have the correct orientation.

        :param g: the network
        :param n: the node'''
        es = self.elements()
        for (nn, mm) in g.edges(n):
            if (g.node[nn][CompartmentedModel.COMPARTMENT] == self._right) and (g.node[mm][CompartmentedModel.COMPARTMENT] == self._left):
                # print 'edge ({m}, {n}) enters {l}'.format(n = nn, m = mm, l = self._name)
                es.add((mm, nn))
            else:
                if (g.node[nn][CompartmentedModel.COMPARTMENT] == self._left) and (g.node[mm][CompartmentedModel.COMPARTMENT] == self._right):
                    # print 'edge ({n}, {m}) enters {l}'.format(n = nn, m = mm, l = self._name)
                    es.add((nn, mm))


class CompartmentedModel(Process):
    '''The base class a :term:`compartmented model of disease`, which
    represents a disease as a collection of discrete :term:`compartments` with each
    compartment specifying some facet of the disease's progression. Nodes
    transition between compartments with some probability, so the disease's
    progression forms a stochastic process in which nodes typically move
    through several compartments according to the probabilities defined.

    When run, a compartmented model generates results consisting of the size of each
    compartment at the end of the experiment. This can be changed by overriding the
    :meth:`results` method.'''
    
    # model state variables
    COMPARTMENT = 'compartment'            #: Node attribute holding the node's compartment.
    OCCUPIED = 'occupied'                  #: Edge attribute, True if infection travelled along the edge.
    
    def __init__( self ):
        super(CompartmentedModel, self).__init__()
        self.reset()

    def reset( self ):
        '''Reset the model ready to be built.'''
        super(CompartmentedModel, self).reset()
        self._compartments = []
        self._effects = dict()
        self._eventDistribution = None

    def build( self, params ):
        '''Build the model. This must be overridden by sub-classes, and should
        call methods such as :meth:`addCompartment`, :meth:`trackEdgesBetweenCompartments`,
        :teth:`trackEdgesBetweenCompartments`, and :meth:`addEventAtLocus`
        to add the various elements of the specific disease model.

        :param params: the model parameters'''
        raise NotImplementedError('build')

    def addCompartment( self, c, p = 0.0 ):
        '''Add a compartment to the model. A node is assigned to the compartment
        initially with the given probability. The probabilities for all compartments
        in the model must sum to 1.

        :param c: the compartment name
        :param p: the initial occupancy probability (defaults to  0.0)'''
        self._compartments.append((c, p))

    def trackNodesInCompartment(self, c, name = None):
        '''Add a locus tracking nodes in a given compartment.

        :param c: the compartment to track
        :param name: (optional) the name of the locus (defaults to the compartment name)'''
        if name is None:
            name = c
        if name in self:
            raise NameError('Locus {c} already exists in model'.format(c = name))
        else:
            # add locus
            locus = CompartmentedNodeLocus(name, c)
            self.addLocus(name, locus)

            # add handlers
            self._addHandlers(c, lambda g, n: locus.leaveHandler(g, n),
                                 lambda g, n: locus.enterHandler(g, n))

    def trackEdgesBetweenCompartments(self, l, r, name = None):
        '''Add a locus to track edges with endpoint nodes in the given compartments.

        :param l: the compartment of the left node
        :param r: the compartment of the right node
        :param name: (optional) the name of the locus (defaults to a combination of the two compartment names)'''
        if name is None:
            name = '{l}-{r}'.format(l = l, r = r)
        if name in self:
            raise NameError('Locus {c} already exists in model'.format(c = name))
        else:
            # add locus
            locus = CompartmentedEdgeLocus(name, l, r)
            self.addLocus(name, locus)

            # add handlers
            self._addHandlers(l, lambda g, n: locus.leaveHandler(g, n),
                                 lambda g, n: locus.enterHandler(g, n))
            self._addHandlers(r, lambda g, n: locus.leaveHandler(g, n),
                                 lambda g, n: locus.enterHandler(g, n))

    def _addHandlers( self, c, lh, eh ):
        '''Add handler functions for a compartment, to be called whenever the contents
        of that compartment change. This links compartments to loci.

        Handlers are functions that take a model, a network, a node, and a
        compartment, and provide the appropriate behaviour for when the node
        enters (or leaves) the compartment.
        
        :param c: the compartment
        :param lh: the leave handler
        :param eh: the enter handler'''
        if c not in self._effects.keys():
            self._effects[c] = [ (lh, eh) ]
        else:
            self._effects[c].append((lh, eh))

    def _callLeaveHandlers( self, g, n, c ):
        '''Call all handlers affected by a node leaving a compartment.

        :param g: the network
        :param n: the node
        :param c: the compartment'''
        if c in self._effects.keys():
            for (lh, _) in self._effects[c]:
                lh(g, n)

    def _callEnterHandlers( self, g, n, c ):
        '''Call all handlers affected by a node entering a compartment.

        :param g: the network
        :param n: the node
        :param c: the compartment'''
        if c in self._effects.keys():
            for (_, eh) in self._effects[c]:
                eh(g, n)

    def compartment( self, g, c ):
        '''Return all the nodes currently in a particular compartment in a network. This works
        for all compartments, not just those that are loci for dynamics.

        :param g: the network
        :param c: the compartment
        :returns: a collection of nodes'''
        return [ n for n in g.nodes() if g.node[n][self.COMPARTMENT] == c]
    
    def changeCompartment( self, g, n, c ):
        '''Change the compartment of a node.

        :param g: the network
        :param n: the node
        :param c: the new compartment for the node'''
        
        # propagate effects of leaving the current compartment
        self._callLeaveHandlers(g, n, g.node[n][self.COMPARTMENT])

        # record new compartment on node
        g.node[n][self.COMPARTMENT] = c

        # propagate effects of entering new compartment
        self._callEnterHandlers(g, n, c)

    def initialCompartmentDistribution( self ):
        '''Return the initial distribution of nodes to compartments. The
        result should be a valid distribution, with probabilities summing
        to one. This is used by :meth:`initialCompartments` to set the initial
        compartment of each node.

        :returns: a list of (compartment, probability) pairs'''
        return self._compartments

    def initialCompartments( self, g ):
        '''Place each node in the network into its initial compartment. The default
        initialises the nodes into a random compartment according to the initial
        compartment distribution returned by :meth:`initialCompartmentDistribution`.
        This method may be overridden to, for example structure the initial
        population non-randomly.

        :param g: the network'''

        # get the initial compartment distribution
        dist = self.initialCompartmentDistribution()

        # assign nodes to compartments
        for n in g.nodes():
            # select a compartment according to the initial distribution
            r = numpy.random.random()
            a = 0.0
            for (c, p) in dist:
                a = a + p
                if r <= a:
                    # change node's compartment
                    self.changeCompartment(g, n, c)

                    # on to the next node
                    break

    def setUp( self, params ):
        '''Set up the initial population of nodes into compartments.
        
        :param params: the simulation parameters'''

        # initialise all nodes to an empty compartment
        # (so we can assume all nodes have a compartment attribute)
        g = self.network()
        for n in g.nodes():
            g.node[n][self.COMPARTMENT] = None

        # mark edges as unoccupied
        for (_, _, data) in g.edges(data = True):
            data[self.OCCUPIED] = False

        # place nodes in initial compartments
        self.initialCompartments(g)

    def markOccupied( self, g, e ):
        '''Mark the given edge as having been occupied by the dynamics, i.e., to
        have been traversed in transmitting the disease.

        :param g: the network
        :param e: the edge'''
        (n, m) = e
        data = g.get_edge_data(n, m)
        data[self.OCCUPIED] = True
        
    def results( self ):
        '''Create a dict of experimental results for the experiment, consisting of the final
        sizes of all the compartments.

        :returns: a dict of experimental results'''
        rc = super(CompartmentedModel, self).results()

        for (c, _) in self._compartments:
            rc[c] = 0
        g = self.network()
        for n in g.nodes():
            c = g.node[n][self.COMPARTMENT]
            rc[c] = rc[c] + 1
        return rc

    def skeletonise( self ):
        '''Remove unoccupied edges from the network. This leaves the network
        consisting of only "occupied" edges that were used to transmit the
        infection between nodes. Note that this process means that further
        dynamics over the network probably don't make sense, unless you're
        actually wanting to run on the residual network post-infection.

        :returns: the network with unoccupied edges removed'''
        
        # find all unoccupied edges
        g = self.network()
        edges = []
        for (n, m, data) in g.edges(data = True):
            if (self.OCCUPIED not in data.keys()) or (data[self.OCCUPIED] != True):
                # edge is unoccupied, mark it to be removed
                # (safe because there are no parallel edges)
                edges.insert(0, (n, m))
                    
        # remove all the unoccupied edges
        g.remove_edges_from(edges)
        
        return g
    
