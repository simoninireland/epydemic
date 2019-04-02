# Canonical addition-deletion process
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
import networkx
import numpy


class AddDelete(Process):
    '''A process to manage an addition-deletion network, in which nodes are added
    and deleted at random according to some probability. Nodes that are added
    are connected to existing nodes.

    The default behaviour has fixed addition and removal probabilities, independent
    of the size of the network, and a fixed degree for added nodes.'''

    P_ADD = "pAdd"  #: Parameter for the node addition probability
    P_DELETE = "pDelete"  #: Parameter for the node deletion probability
    DEGREE = "addDegree"  #: Degree of newly-added nodes

    SINGLETON = "singleton"  #: Name of the locus capturing all the nodes
    NODES = "allnodes"       #: Name of the locus holding all nodes in the network

    def __init__(self):
        super(AddDelete, self).__init__()
        self.reset()

    def build(self, params):
        '''Build the model. This method expects parameters for the node addition
        and deletion probabilities, and for the degree of newly-created nodes.

        :param params: the model parameters'''
        pAdd = params[self.P_ADD]
        pDelete = params[self.P_DELETE]

        # stash the degree of new nodes for the events
        self._c = params[self.DEGREE]

        # add events, which occur at constant probability regardless of the network size
        self.trackNetwork(self.SINGLETON)
        self.addEvent(self.SINGLETON, pAdd, self.add)
        self.addEvent(self.SINGLETON, pDelete, self.remove)

        # also keep track of all the nodes
        self.trackAllNodes(self.NODES, self.network())

    def addNode(self):
        '''Add a new node to the network.

        :returns: the node'''
        g = self.network()

        # create a new name for the new node
        i = g.order() + 1
        while i in g.nodes():
            i = i + 1

        # add the node to the network
        g.add_node(i)

        # add the new node to the all-nodes locus
        self[self.NODES].enterHandler(g, n)

        return i

    def addEdge(self, n, m):
        '''Add an edge between the two nodes.

        :param n: one node
        :param m: the other node'''
        self.network().add_edge(n, m)

    def removeNode(self, n):
        '''Remove the given node and all its incident edges

        :param n: the node to remove'''

        # remove the node from the network
        self.network().remove_node(n)

        # remove the node from the all-nodes locus
        self[self.NODES].leaveHandler(g, n)


    def add(self, t, g, e):
        '''Add a node to the network, connecting it at random to
        other nodes. The degree of the new node is given by the :attr:`DEGREE` parameter,
        with the nodes being selected at random from the entire network.

        :param t: the current simulation time (not used)
        :param g: the network
        :param e: the element (not used)'''

        # create a new node
        i = self.addNode()

        # link to c other nodes (not including i) with uniform probability
        ns = self[self.NODES]
        es = set()
        for m in xrange(self._c):
            # a probably unnecessary test for parallel edges and self-loops
            while (True):
                j = ns.draw()
                if (i <> j) and (j not in es):
                    break
            es.add(j)
        for j in es:
            self.addEdge(i, j)

    def remove(self, t, g, n):
        '''Remove a node from the network.

        :param t: the current simulation time (not used)
        :param g: the network
        :param e: the node to be removed'''
        self.removeNode(e)