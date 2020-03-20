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

from __future__ import print_function
from epydemic import *
import numpy
import collections


class CompartmentedLocus(Locus):
    '''A locus based on the compar6tments that nodes reside in.

    :param name: the locus' name'''

    def __init__(self, name):
        super(CompartmentedLocus, self).__init__(name)

    def compartments(self):
        '''Return the compartments this locus monitors. This should be
        overridden by sub-classes as required.

        :returns: the compartments'''
        return []
   

class CompartmentedNodeLocus(CompartmentedLocus):
    '''A locus for dynamics occurring at a single node, where the
    locus tracks all nodes in a single compartment.

    :param name: the locus' name
    :param c: the compartment'''

    def __init__(self, name, c):
        super(CompartmentedNodeLocus, self).__init__(name)
        self._compartment = c

    def compartments(self):
        '''Return the node compartment we monitor.

        :returns: the compartment'''
        return [ self._compartment ]


class CompartmentedEdgeLocus(CompartmentedLocus):
    '''A locus for dynamics occurring at an edge, where the locus tracks all
    edges whose endpoint nodes are in specified compartments. Since the network may
    also be adaptive, we need to track additionals and removals of edges too.

    :param name: the locus' name
    :param l: the left compartment
    :param r: the right compartment'''

    def __init__(self, name, l, r):
        super(CompartmentedEdgeLocus, self).__init__(name)
        self._left = l
        self._right = r

    def compartments(self):
        '''Return the compartments of the node endpoints we monitor.

        :returns: the compartments'''
        return [ self._left, self._right ]

    def matches(self, g, n, m):
        '''Test whether the given edge has the right compartment endpoints for this compartment. The
        method returns 1 if the edge has the right compartments in the orientation (n, m), -1 if it has
        the right compartments in orientation (m, n), and 0 otherwise.

        :param g: the network
        :param n: the first node
        :param m: the second node
        :returns: match status -1, 0, or 1'''
        if (g.nodes[n][CompartmentedModel.COMPARTMENT] == self._right) and (g.nodes[m][CompartmentedModel.COMPARTMENT] == self._left):
            return -1
        else:
            if (g.nodes[n][CompartmentedModel.COMPARTMENT] == self._left) and (g.nodes[m][CompartmentedModel.COMPARTMENT] == self._right):
                return 1
            else:
                return 0

    def addHandler(self, g, e):
        '''An edge is added to the network, check if its endpoint compartments match the
        locus and add it if so. 

        :param, g: the network
        :param e: the edge'''
        (n, m) = e
        es = self.elements()
        match = self.matches(g, n, m)
        if match == -1:
            #print('edge ({m}, {n}) added to {l}'.format(n = n, m = m, l = self._name))
            es.add((m, n))
        else:
            if match == 1:
                #print('edge ({n}, {m}) added {l}'.format(n = n, m = m, l = self._name))
                es.add((n, m))

    def leaveHandler(self, g, n):
        '''Node leaves one of the edge's compartments, remove any incident edges
        that no longer have the correct orientation.

        :param g: the network
        :param n: the node'''
        es = self.elements()
        for (nn, mm) in g.edges(n):
            match = self.matches(g, nn, mm)
            if match == -1:
                #print('edge ({m}, {n}) leaves {l}'.format(n = nn, m = mm, l = self._name))
                es.discard((mm, nn))
            else:
                if match == 1:
                    #print('edge ({n}, {m}) leaves {l}'.format(n = nn, m = mm, l = self._name))
                    es.discard((nn, mm))

    def enterHandler(self, g, n):
        '''Node enters one of the edge's compartments, add any incident edges
        that now have the correct orientation.

        :param g: the network
        :param n: the node'''
        es = self.elements()
        for (nn, mm) in g.edges(n):
            match = self.matches(g, nn, mm)
            if match == -1:
                #print('edge ({m}, {n}) enters {l}'.format(n = nn, m = mm, l = self._name))
                es.add((mm, nn))
            else:
                if match == 1:
                    #print('edge ({n}, {m}) enters {l}'.format(n = nn, m = mm, l = self._name))
                    es.add((nn, mm))

    def removeHandler(self, g, e):
        '''An edge is removed from the network, check whether it was in this locus and
        remove it if so.

        :param, g: the network
        :param e: the edge'''
        (n, m) = e
        es = self.elements()
        match = self.matches(g, n, m)
        if match == -1:
            print('edge ({m}, {n}) removed from {l}'.format(n = n, m = m, l = self._name))
            es.discard((m, n))
        else:
            if match == 1:
                print('edge ({n}, {m}) removed from {l}'.format(n = n, m = m, l = self._name))
                es.discard((n, m))


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
    COMPARTMENT = 'compartment'                 #: Node attribute holding the node's compartment.
    OCCUPIED = 'occupied'                       #: Edge attribute, True if infection travelled along the edge.
    T_OCCUPIED = 'occupationTime'               #: Edge attribute holding the time the infection crossed the edge.

    # default compartment
    DEFAULT_COMPARTMENT = 'defaultCompartment'  #: Default compartment label for new nodes

    def __init__( self ):
        super(CompartmentedModel, self).__init__()


    # ---------- Setup and initialisation ----------

    def reset( self ):
        '''Reset the model ready to be built.'''
        super(CompartmentedModel, self).reset()
        self._compartments = []
        self._effects = dict()
        self._eventDistribution = None

    def setUp(self, params):
        '''Set up the initial population of nodes into compartments.

        :param params: the simulation parameters'''
        super(CompartmentedModel, self).setUp(params)

        # initialise all nodes to an empty compartment
        # (so we can assume all nodes have a compartment attribute)
        g = self.network()
        for n in g.nodes():
            g.nodes[n][self.COMPARTMENT] = None

        # mark edges as unoccupied
        for (_, _, data) in g.edges(data=True):
            data[self.OCCUPIED] = False

        # place nodes in initial compartments
        self.initialCompartments()

    def initialCompartmentDistribution( self ):
        '''Return the initial distribution of nodes to compartments. The
        result should be a valid distribution, with probabilities summing
        to one. This is used by :meth:`initialCompartments` to set the initial
        compartment of each node.

        :returns: a list of (compartment, probability) pairs'''
        return self._compartments

    def initialCompartments( self ):
        '''Place each node in the network into its initial compartment. The default
        initialises the nodes into a random compartment according to the initial
        compartment distribution returned by :meth:`initialCompartmentDistribution`.
        This method may be overridden to, for example structure the initial
        population non-randomly.'''

        # get the initial compartment distribution
        dist = self.initialCompartmentDistribution()

        # assign nodes to compartments
        g = self.network()
        for n in g.nodes():
            # select a compartment according to the initial distribution
            r = numpy.random.random()
            a = 0.0
            for (c, p) in dist:
                a = a + p
                if r <= a:
                    # change node's compartment
                    self.changeCompartment(n, c)

                    # on to the next node
                    break


    # ---------- Termination and results ----------

    def compartment( self, c ):
        '''Return all the nodes currently in a particular compartment in a network. This works
        for all compartments, not just those that are loci for dynamics.

        :param c: the compartment
        :returns: a collection of nodes'''
        g = self.network()
        return [ n for n in g.nodes() if g.nodes[n][self.COMPARTMENT] == c]

    def results(self):
        '''Create a dict of experimental results for the experiment, consisting of the final
        sizes of all the compartments.

        :returns: a dict of experimental results'''
        rc = super(CompartmentedModel, self).results()

        for (c, _) in self._compartments:
            rc[c] = 0
        g = self.network()
        for n in g.nodes():
            c = g.nodes[n][self.COMPARTMENT]
            rc[c] = rc[c] + 1
        return rc

    def skeletonise(self):
        '''Remove unoccupied edges from the network. This leaves the network
        consisting of only "occupied" edges that were used to transmit the
        infection between nodes. Note that this process means that further
        dynamics over the network probably don't make sense, unless you're
        actually wanting to run on the residual network post-infection.

        :returns: the network with unoccupied edges removed'''

        # find all unoccupied edges
        g = self.network()
        edges = []
        for (n, m, data) in g.edges(data=True):
            if (self.OCCUPIED not in data.keys()) or (data[self.OCCUPIED] != True):
                # edge is unoccupied, mark it to be removed
                # (safe because there are no parallel edges)
                edges.insert(0, (n, m))

        # remove all the unoccupied edges
        g.remove_edges_from(edges)

        return g


    # ---------- Managing compartments ----------

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
        :param name: (optional) the name of the locus (defaults to the compartment name)
        :returns: the locus used to track the nodes'''
        if name is None:
            name = c
        if name in self:
            raise NameError('Locus {c} already exists in model'.format(c = name))
        else:
            # add locus
            locus = CompartmentedNodeLocus(name, c)
            return self.addLocus(name, locus)

    def trackEdgesBetweenCompartments(self, l, r, name = None):
        '''Add a locus to track edges with endpoint nodes in the given compartments.

        :param l: the compartment of the left node
        :param r: the compartment of the right node
        :param name: (optional) the name of the locus (defaults to a combination of the two compartment names)
        :returns: the locus used to track the nodes'''
 
        if name is None:
            name = '{l}-{r}'.format(l = l, r = r)
        if name in self:
            raise NameError('Locus {c} already exists in model'.format(c = name))
        else:
            # add locus
            locus = CompartmentedEdgeLocus(name, l, r)
            return self.addLocus(name, locus)

    def addLocus(self, n, l = None):
        '''Add a locus to the model, initialising the handler functions.

        :param n: the name
        :param l: (optional) the locus
        :returns: the locus'''
        locus = super(CompartmentedModel,self).addLocus(n, l)
        for c in locus.compartments():
            if c not in self._effects.keys():
                self._effects[c] = []
            self._effects[c].append((locus.addHandler, locus.leaveHandler, locus.enterHandler, locus.removeHandler))

    def _addHandlers( self, c, lh, eh ):
        '''Add handler functions for a compartment, to be called whenever the contents
        of that compartment change. This links compartments to loci.

        Handlers are functions that take a network and a node
        and provide the appropriate behaviour for when the node
        enters (or leaves) the compartment.
        
        :param c: the compartment
        :param lh: the leave handler
        :param eh: the enter handler'''
        if c not in self._effects.keys():
            self._effects[c] = [ (lh, eh) ]
        else:
            self._effects[c].append((lh, eh))

    def _handlerCompartments(self, e):
        '''Return the compartments that a given element's change might affect.

        :param e: a node or edge
        :returns: a list of compartments'''
        g = self.network()
        if isinstance(e, tuple):
            # element is an edge, check compartments at the endpoints
            (n, m) = e
            cs = [ g.nodes[n][self.COMPARTMENT], g.nodes[m][self.COMPARTMENT] ]
        else:
            # element is a node, check its own compartmnent
            cs = [ g.nodes[e][self.COMPARTMENT] ]
        return cs

    def _callAddHandlers( self, e ):
        '''Call all handlers affected by a mnode or edge being added to the network.

        :param e the node or edge'''
        g = self.network()
        for c in self._handlerCompartments(e):
            if c in self._effects.keys():
                for (ah, _, _, _) in self._effects[c]:
                    ah(g, e)

    def _callLeaveHandlers( self, e, c ):
        '''Call all handlers affected by a node or edge leaving a compartment.

        :param e: the node or edge
        :param c: the compartment'''
        g = self.network()
        for c in self._handlerCompartments(e):
            if c in self._effects.keys():
                for (_, lh, _, _) in self._effects[c]:
                    lh(g, e)

    def _callEnterHandlers( self, e, c ):
        '''Call all handlers affected by a node or edge entering a compartment.

        :param e: the node or edge
        :param c: the compartment'''
        g = self.network()
        for c in self._handlerCompartments(e):
            if c in self._effects.keys():
                for (_, _, eh, _) in self._effects[c]:
                    eh(g, e)

    def _callRemoveHandlers( self, e ):
        '''Call all handlers affected by a node or edge being removed from the network.

        :param e: the node or edge'''
        g = self.network()
        for c in self._handlerCompartments(e):
            if c in self._effects.keys():
                for (_, _, _, rh) in self._effects[c]:
                    rh(g, e)


    # ---------- Accessing and evolving the network ----------

    def setCompartment(self, n, c):
        '''Set the compartment of a node. This assumes that the node doesn't already have
        a compartment set, and so should be used only for initialising new nodes: in all
        other cases, use :meth:`changeCompartment`.

        :param n: the node
        :param c: the new compartment for the node'''
        g = self.network()

        # set the correct node attribute
        g.nodes[n][self.COMPARTMENT] = c

        # propagate the change to any other compartments
        self._callEnterHandlers(n, c)

    def changeCompartment( self, n, c ):
        '''Change the compartment of a node.

        :param n: the node
        :param c: the new compartment for the node'''
        g = self.network()

        # propagate effects of leaving the current compartment
        self._callLeaveHandlers(n, g.nodes[n][self.COMPARTMENT])

        # record new compartment on node
        g.nodes[n][self.COMPARTMENT] = c

        # propagate effects of entering new compartment
        self._callEnterHandlers(n, c)

    def markOccupied( self, e, t ):
        '''Mark the given edge as having been occupied by the dynamics, i.e., to
        have been traversed in transmitting the disease, at time t.

        :param e: the edge
        :param t: the time at which it was occupied'''
        g = self.network()
        (n, m) = e
        data = g.get_edge_data(n, m)
        data[self.OCCUPIED] = True
        data[self.T_OCCUPIED] = t
        
    def addNode(self, n, compartment, **kwds):
        '''Add a node to the working network, adding it to the appropriate compartment.

        :param n: the new node
        :param compartment: compartment for the node
        :param kwds: (optional) node attributes'''
        super(CompartmentedModel, self).addNode(n, **kwds)
        self.setCompartment(n, compartment)

    def removeNode(self, n):
        '''Remove a node from the working network, updating any affected compartments.

        :param n: the node'''

        # remove node from any compartments
        self._callRemoveHandlers(n)

        # remove the node
        super(CompartmentedModel, self).removeNode(n)

    def addEdge(self, n, m,  **kwds):
        '''Add an edge between nodes, adding the edge to any appropriate compartments.

        :param n: the start node
        :param m: the end node
        :param kwds: (optional) edge attributes'''
        super(CompartmentedModel, self).addEdge(n, m, **kwds)

        # add edge to any compartments it should be in
        self._callAddHandlers((n, m))

    def removeEdge(self, n, m):
        '''Remove an edge from the working network and from any compartments.

        :param n: the start node
        :param m: the end node'''

        # remove edge from any compartments it should be in
        self._callRemoveHandlers((n, m))

        # remove the edge from the network
        super(CompartmentedModel, self).removeEdge(n, m)
