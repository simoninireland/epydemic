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
import random

class Locus(object):
    '''The locus of dynamics, where chanmges can happen. Loci
    are filled with nodes or edges, typically populated and re-populated as
    a process over the network evolves. The contents of a locus are
    tracked to improve performance.

    :param name: the locus name'''

    def __init__( self, name ):
        super(Locus, self).__init__()
        self._name = name
        self._elements = set()
        self._events = []

    def name( self ):
        '''Returns the name of the locus.

        :returns: the locus' name'''
        return self._name
        
    def __len__( self ):
        '''Return the number of elements at the locus.

        :returns: the number of elements'''
        return len(self._elements)

    def elements( self ):
        '''Return the underlying elements of the locus.

        :returns: the elements'''
        return self._elements
    
    def draw( self ):
        '''Draw a random element from the locus. The locus is left unchanged.

        :returns: a random element at the locus'''
        e = (random.sample(self._elements, 1))[0]
        return e

    def leaveHandler( self, g, n ):
        '''Handler for when a node leaves the locus. Must be overridden
        by sub-classes.

        :param g: the network
        :param n: the node'''
        raise NotImplementedError('leaveHandler')

    def enterHandler( self, g, n ):
        '''Handler for when a node enters the locus. Must be overridden
        by sub-classes.

        :param g: the network
        :param n: the node'''
        raise NotImplementedError('enterHandler')

    def addEvent( self, p, ef ):
        '''Add a probabilistic event that occurs with a particular probability at
        each element, calling the :term:`event function` when it is selected.

        The :term:`event function` takes the dynamics, the simulation time,
        the network, and the element to which the event applies (a node or an edge,
        which will have been drawn from the event's locus).

        :param l: the locus name
        :param p: the event probability
        :param ef: the event function'''
        self._events.append((self, p, ef))

    def events(self):
        '''Return the events associated with this locus.

        :returns: a list of (locus, probability, function) pairs'''
        return self._events


class Singleton(Locus):
    '''A :class:`Locus` with a single element. This means that any events attached
    to this locus will occur with a fixed given probability, independent of the size
    of the network.

    :param name: the locus; name'''

    def __init__(self, name):
        super(Singleton, self).__init__(name)
        self._elements = set([ None ])

    def __len__( self ):
        '''A singleton is treated as a locus with a single element.

        :returns: 1'''
        return 1

    def elements( self ):
        '''A singleton uses None as its element

        :returns: a list containing one None value'''
        return [ None ]

    def draw(self):
        '''Draw the only element from the locus.

        :returns: None'''
        return None

    def leaveHandler( self, g, n ):
        '''Nothing ever leaves this locus.

        :param g: the network
        :param n: the node'''
        raise Exception('Something tried to leave the singleton locus')

    def enterHandler( self, g, n ):
        '''Nothing can be added to this locis.

        :param g: the network
        :param n: the node'''
        raise Exception('Something tried to enter the singleton locus')


class AllNodes(Locus):
    '''A :class:`Locus` containing all the nodes in a given network. This will reflect
    changes to the node set as the graph evolves. An event attached to this locus will
    choose any node from then network.

    :param name: the name of the locus
    :param g: the network for which we hold all the nodes'''

    def __init__(self, name, g):
        super(AllNodes, self).__init__(name)
        self._g = g

    def __len__( self ):
        '''Return the number of nodes in the underlying network.

        :returns: the number of nodes'''
        return self._g.order()

    def elements( self ):
        '''Return the nodes in the network we're tracking.

        :returns: the nodes'''
        return self._g.nodes()

    def leaveHandler( self, g, n ):
        '''Nothing to do.

        :param g: the network
        :param n: the node'''
        pass

    def enterHandler( self, g, n ):
        '''Nothing to do.

        :param g: the network
        :param n: the node'''
        pass


class AllEdges(Locus):
    '''A :class:`Locus` containing all the edges in a given network. This will reflect
    changes to the edge set as the graph evolves. An event attached to this locus will
    choose any edge from then network.

    :param name: the name of the locus
    :param g: the network for which we hold all the edges'''

    def __init__(self, name, g):
        super(AllEdges, self).__init__(name)
        self._g = g

    def __len__( self ):
        '''Return the number of edges in the underlying network.

        :returns: the number of edges'''
        return len(self._g.edges())

    def elements( self ):
        '''Return the edges in the network we're tracking.

        :returns: the nodes'''
        return self._g.edges()

    def leaveHandler(self, g, n):
        '''Nothing to do.

        :param g: the network
        :param n: the node'''
        pass

    def enterHandler(self, g, n):
        '''Nothing to do.

        :param g: the network
        :param n: the node'''
        pass