# Compartmented models model
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

import epydemic
from epydemic import *

import numpy
import random
import collections

class CompartmentedModel(object):
    '''The base class for compartmented models. A :term:`compartmented model of disease`
    represents a disease as a collection of discrete compartments, with each
    :term:`compartment` specifying some facet of the disease's progression. Nodes
    transition between compartments with some probability, so the disease's
    progession is a stochastic process in which the various nodes typically move
    through several compartments according to the probabilities defined.

    Compartmented models can be run in :term:`discrete time` using :term:`synchronous dynamics`,
    or in :term:`continuous time` using :term:`stochastic dynamics` (also known as Gilespie
    dynamics).'''
    
    
    # model state variables
    COMPARTMENT = 'dynamics_compartment'   #: Node attribute used to hold compartment
    OCCUPIED = 'occupied'                  #: Edge attribute, True if edge passed infection
    
    def __init__( self ):
        '''Create a new compartmented model.'''
        super(CompartmentedModel, self).__init__()
        self._compartments = []
        self._loci = dict()
        self._effects = dict()
        self._events = []
        
    def addCompartment( self, c, p = 0.0 ):
        '''Add a compartment to the model. A node is assigned to the compartment
        initially with the given probability. The probabilities for all compartments
        in the model must sum to 1.

        :param c: the compartment name
        :param p: the initial occupancy probability (defaults to  0.0)'''
        self._compartments.append((c, p))

    def addLocus( self, l, r = None, name = None ):
        '''Add a one- or two-compartment locus, corresponding to a node
        or edge at which dynamics occurs (e.g,. which can have events associated
        with it).

        :param l: the left-hand (or only) compartment
        :param r: the right-hand compartment (for an edge)
        :param name: the name of the locus'''

        if r is None:
            # one compartment, node locus
            if name is None:
                name = l
            if name in self._loci.keys():
                raise Exception('Locus {n} already exists'.format(n = name))

            # add locus
            locus = epydemic.NodeLocus(name, l)
            self._loci[name] = locus

            # add effects
            self._addHandlers(l, lambda m, g, n, c: locus.leaveHandler(m, g, n, c),
                                 lambda m, g, n, c: locus.enterHandler(m, g, n, c))
        else:
            # two compartments, edge locus
            if name is None:
                name = '{l}{r}'.format(l = l, r = r)
                if name in self._loci.keys():
                    raise Exception('Locus {n} already exists'.format(n = name))

            # add locus
            locus = epydemic.EdgeLocus(name, l, r)
            self._loci[name] = locus

            # add effects
            self._addHandlers(l, lambda m, g, n, c: locus.leaveHandler(m, g, n, c),
                                 lambda m, g, n, c: locus.enterHandler(m, g, n, c))
            self._addHandlers(r, lambda m, g, n, c: locus.leaveHandler(m, g, n, c),
                                 lambda m, g, n, c: locus.enterHandler(m, g, n, c))

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
                lh(self, g, n, c)

    def _callEnterHandlers( self, g, n, c ):
        '''Call all handlers affected by a node entering a compartment.

        :param g: the network
        :param n: the node
        :param c: the compartment'''
        if c in self._effects.keys():
            for (_, eh) in self._effects[c]:
                eh(self, g, n, c)

    def changeCompartment( self, g, n, c ):
        '''Change the compartment of a node. This will update all loci
        potentiually affected by the change.

        :param g: the network
        :param n: the node
        :param c: the new compartment for the node'''
        
        # propagate effects of leaving the current compartment
        self._callLeaveHandlers(g, n, g.node[n][self.COMPARTMENT])

        # record new compartment on node
        g.node[n][self.COMPARTMENT] = c

        # propagate effects of entering new compartment
        self._callEnterHandlers(g, n, c)

    def addEvent( self, l, p, ef ):
        '''Add an event to a locus, occurring with a particular (fixed)
        probability and calling the event function when it is selected.

        :param l: the locus name
        :param p: the event probability
        :param ef: the event function'''
        self._events.append((self._loci[l], p, ef))

    def initialCompartmentDistribution( self ):
        '''Return the initial distribution of nodes to compartments. The
        result should be a valid distribution, with probabilities summing
        to one.

        :returns: a list of (compartment, probability) pairs'''
        return self._compartments

    def eventDistribution( self, t ):
        '''Return the distribution of events. The result should be a valid distribution,
        with probabilities summing to one. The default implemnentation returns a constantr
        distribution populated from the model paremeters. Sub-classes may override to
        provide time-evolving probabilities.

        :param t: the current simulation time
        :returns: a list of (locus, probability, event) triples'''
        return self._events

    def setUp( self, g, params ):
        '''Set up the initial population of nodes into compartments.

        :param g: the network
        :param params: the simulation parameters'''

        # initialise all nodes to an empty compartment
        # (so we can assume all nodes have a compartment attribute)
        for n in g.nodes_iter():
            g.node[n][self.COMPARTMENT] = None
            
        # get the initial compartment distribution
        dist = self.initialCompartmentDistribution()

        # assign nodes to compartments
        for n in g.nodes_iter():
            # select a compartment according to the initial distribution
            r = numpy.random.random()
            a = 0.0
            for (c, p) in dist:
                a = a + p
                if r <= a:
                    # change node's compartment
                    g.node[n][self.COMPARTMENT] = c
                    
                    # propagate effects of entering new compartment
                    self._callEnterHandlers(g, n, c)

                    # on to the next node
                    break

        # mark edges as unoccupied
        for (_, _, data) in g.edges_iter(data = True):
            data[self.OCCUPIED] = False

    def markOccupied( self, g, e ):
        '''Mark the givewn edge as having been occupied by the dynamics, i.e., to
        have been traversed in transmitting the disease.

        :param g: the network
        :param e: the edge'''
        (n, m) = e
        data = g.get_edge_data(n, m)
        data[self.OCCUPIED] = True
        
    def results( self, g ):
        '''Create a dict of experimental results for the experiment.

        :param g: the network
        :returns: a dict of experimental results'''
        rc = dict()

        # add final sizes of all loci
        rc['loci'] = dict()
        for (l, locus) in self._loci.iteritems():
            rc['loci'][l] = len(locus)

        # add final sizes of all compartments
        rc['compartments'] = dict()
        for (c, _) in self._compartments:
            rc['compartments'][c] = 0        
        for n in g.nodes_iter():
            c = g.node[n][self.COMPARTMENT]
            rc['compartments'][c] = rc['compartments'][c] + 1

        return rc

    def skeletonise( self, g ):
        '''Remove unoccupied edges from the network. This leaves the network
        consisting of only "occupied" edges that were used to transmit the
        infection between nodes. Note that this process means that further
        dynamics over the network doesn't make sense.
        
        :returns: the network with unoccupied edges removed'''
        
        # find all unoccupied edges
        edges = []
        for (n, m, data) in g.edges_iter(data = True):
            if (self.OCCUPIED not in data.keys()) or (data[self.OCCUPIED] != True):
                # edge is unoccupied, mark it to be removed
                # (safe because there are no parallel edges)
                edges.insert(0, (n, m))
                    
        # remove all the unoccupied edges
        g.remove_edges_from(edges)
        
        return g
    
