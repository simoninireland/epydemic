# Loci for dynamics in compartmented models model
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

import numpy
import random

class Locus(object):
    '''The locus of dynamics.'''

    def __init__( self, name ):
        super(Locus, self).__init__()
        self._name = name
        self._elements = set()

    def name( self ):
        '''Returns the name of the locus.

        :returns: the locus' name'''
        return self_name
        
    def __len__( self ):
        '''Return the number of elements at the locus.

        :returns: the number of elements'''
        return len(self._elements)

    def elements( self ):
        '''Return the underlying elements of the locus.

        :returns: the elements'''
        return self._elements
    
    def draw( self ):
        '''Draw a random element from the locus.

        :returns: a random element at the locus'''
        e = (random.sample(self._elements, 1))[0]
        #self._elements.remove(e)
        return e

    def leaveHandler( self, m, g, n, c ):
        '''Handler for when a node leaves a compartment., Must be overridden
        by sub-classes.

        :param m: the model
        :param g: the network
        :param n: the node
        :param c: the compartment the node is leaving'''
        raise NotYetImplemented('leaveHandler()')

    def enterHandler( self, m, g, n, c ):
        '''Handler for when a node enters a compartment., Must be overridden
        by sub-classes.

        :param m: the model
        :param g: the network
        :param n: the node
        :param c: the compartment the node is entering'''
        raise NotYetImplemented('enterHandler()')


class NodeLocus(Locus):
    '''A locus for dynamics occurring at a single node.'''

    def __init__( self, name, c ):
        '''Create a locus for nodes in the given compartment.

        :param name: the locus' name
        :param c: the compartment''' 
        super(NodeLocus, self).__init__(name)
        self._compartment = c
        
    def leaveHandler( self, m, g, n, c ):
        '''Node leves the right compartment, rewmove it from the locus

        :param m: the model
        :param g: the network
        :param n: the node
        :param c: the compartment the node is leavinging'''
        print 'node {n} leaves {c}'.format(n = n, c = self._compartment)
        self._elements.remove(n)

    def enterHandler( self, m, g, n, c ):
        '''Node enters the right compartment, add it to the locus

        :param m: the model
        :param g: the network
        :param n: the node
        :param c: the compartment the node is entering'''
        print 'node {n} enters {c}'.format(n = n, c = self._compartment)
        self._elements.add(n)


class EdgeLocus(Locus):
    '''A locus for dynamics occurring at an edge.'''

    def __init__( self, name, l, r ):
        '''Create a locus for an edge with endpoints in the
        given compartments. Edges are treated as directed, in the
        sense that the edge will always be manipulated according to
        the given orientation.

        :param name: the locus' name
        :param l: the left compartment 
        :param r: the right compartment''' 
        super(EdgeLocus, self).__init__(name)
        self._left = l
        self._right = r

    def leaveHandler( self, m, g, n, c ):
        '''Node leaves one of the edge's compartments, remove any incident edges
        that no longer have the correct orientation.

        :param m: the model
        :param g: the network
        :param n: the node
        :param c: the compartment the node is leaving'''
        for (nn, mm) in g.edges_iter(n):
            if (g.node[nn][m.COMPARTMENT] == self._right) and (g.node[mm][m.COMPARTMENT] == self._left):
                print 'edge ({m}, {n}) leaves {l}'.format(n = nn, m = mm, l = self._name)
                self._elements.remove((mm, nn))
            else:
                if (g.node[nn][m.COMPARTMENT] == self._left) and (g.node[mm][m.COMPARTMENT] == self._right):
                    print 'edge ({n}, {m}) leaves {l}'.format(n = nn, m = mm, l = self._name)
                    self._elements.remove((nn, mm))

    def enterHandler( self, m, g, n, c ):
        '''Node enters one of the edge's compartments, add any incident edges
        that now have the correct orientation.

        :param m: the model
        :param g: the network
        :param n: the node
        :param c: the compartment the node is entering'''
        for (nn, mm) in g.edges_iter(n):
            if (g.node[nn][m.COMPARTMENT] == self._right) and (g.node[mm][m.COMPARTMENT] == self._left):
                print 'edge ({m}, {n}) enters {l}'.format(n = nn, m = mm, l = self._name)
                self._elements.add((mm, nn))
            else:
                if (g.node[nn][m.COMPARTMENT] == self._left) and (g.node[mm][m.COMPARTMENT] == self._right):
                    print 'edge ({n}, {m}) enters {l}'.format(n = nn, m = mm, l = self._name)
                    self._elements.add((nn, mm))
