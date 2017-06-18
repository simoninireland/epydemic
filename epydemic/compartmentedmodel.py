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

from epydemic import *
import itertools
import numpy
import random
import collections

class CompartmentedModel(object):

    COMPARTMENT = 'dynamics_compartment'
    OCCUPIED = 'occupied'
    
    def __init__( self ):
        super(CompartmentedModel, self).__init__()

    def addCompartment( self, c, p = 0.0 ):
        '''Add a compartment to the model. A node is assigned to the compartment
        initially with the given probability. The probabilities for all compartments
        in the model must sum to 1.

        :param c: the compartment name
        :param p: the initial occupancy probability (defaults to  0.0)'''
        self._compartments.append((c, p))

    def addLocus(self, l, r = None, name = None ):
        # fill in default
        if name is None:
            if r is None:
                name = l
            else:
                name = '{l}{r}'.format(l = l, r = r)

        # create locus
        self._loci[name] = set()

        # for edge loci, record the end compartments
        if r is not None:
            self._effects[name] = (l, r)
            
    def addEvent( self, locus, p, event ):
        self._events.append((locus, p, event))

    def eventDistribution( self, t ):
        return self._events
    
    def initialCompartmentDistribution( self ):
        return self._compartments

    def checkDistributionIsNormalised( self, dist ):
        a = 0.0
        for (_, p) in dist:
            a = a + p
        if a != 1.0:
            raise Exception('Distribution nor normalised (probabilities sum to {a})'.format(a = a))
        
    def drawFromDistribution( self, dist ):
        r1 = numpy.random.random()
        a = 0.0
        for (c, p) in dist:
            a = a + p
            if r1 <= a:
                return c

    def setUp( self, g, params ):
        # re-set the model ready for a new run
        self._compartments = []       # list of (compartment, initial-probability) pairs
        self._loci = dict()           # mapping from locus to set of elements (nodes or edges)
        self._events = []             # list of (locus, probability, event) triples
        self._effects = dict()
        
        # build the model
        self.build(g, params)

    def compartments( self ):
        return map((lambda (c, _): c), self._compartments)
    
    def loci( self ):
        return self._loci.keys()

    def locus( self, l ):
        return self._loci[l]

    def sizeOfLocus( self, l ):
        return len(self._loci[l])

    def totalLoci( self ):
        return self._totalLoci

    def moveCompartment( self, g, n, c ):
        g.node[n][self.COMPARTMENT] = c

    def isInCompartment( self, g, n, l ):
        return g.node[n][self.COMPARTMENT] == l

    def isInLocus( self, g, v, l ):
        return v in self._loci[l]
    
    def markUnoccupied( self, g, n, m ):
        data = g.get_edge_data(n, m)
        data[self.OCCUPIED] = False
 
    def markOccupied( self, g, n, m ):
        data = g.get_edge_data(n, m)
        data[self.OCCUPIED] = True

    def addEdgeToLocus( self, g, n, m, l ):
        (lc, rc) = self._effects[l]
        
        nc = g.node[n][self.COMPARTMENT]
        mc = g.node[m][self.COMPARTMENT]
        if (nc == lc) and (mc == rc):
            self.addToLocus(l, (n, m))
        else:
            if (mc == lc) and (nc == rc):
                self.addToLocus(l, (m, n))

    def addToLocus( self, l, vs ):
        if l in self._loci.keys():
            if isinstance(vs, collections.Set):
                self._loci[l].update(vs)
            else:
                self._loci[l].add(vs)

    def removeFromLocus( self, l, vs ):
        if l in self._loci.keys():
            if isinstance(vs, collections.Set):
                self._loci[l].difference_update(vs)
            else:
                self._loci[l].remove(vs)

    def drawFromLocus( self, l ):
        e = (random.sample(self._loci[l], 1))[0]
        self._loci[l].remove(e)
        return e
            
    def results( self, g ):
        rc = dict()

        # add final sizes of all loci
        rc['loci'] = dict()
        for l in self.loci():
            rc['loci'][l] = self.sizeOfLocus(l)

        # add final sizes of all compartments
        rc['compartments'] = dict()
        for c in self.compartments():
            rc['compartments'] [c] = 0        
        for n in g.nodes_iter():
            s = g.node[n][self.COMPARTMENT]
            rc['compartments'] [s] = rc['compartments'] [s] + 1

        return rc

    def skeletonise( self, g ):
        '''Remove unoccupied edges from the network. This leaves the network
        consisting of only "occupied" edges that were used to transmit the
        infection between nodes.
        
        :returns: the network with unoccupied edges removed'''
        
        # find all unoccupied edges
        edges = []
        for n in g.nodes_iter():
            for (_, m, data) in g.edges_iter(n, data = True):
                if (self.OCCUPIED not in data.keys()) or (data[self.OCCUPIED] != True):
                    # edge is unoccupied, mark it to be removed
                    # (safe because there are no parallel edges)
                    edges.insert(0, (n, m))
                    
        # remove all the unoccupied edges
        g.remove_edges_from(edges)
        
        return g
    
