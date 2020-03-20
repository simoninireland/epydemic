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

from __future__ import print_function
from epydemic import *


class AddDelete(Process):
    '''A process to manage an addition-deletion network, in which nodes are added
    and deleted at random according to some probability. Nodes that are added
    are connected to existing nodes.

    The default behaviour has fixed addition and removal probabilities, independent
    of the size of the network, and a fixed degree for added nodes.'''

    # parameters
    P_ADD = "pAdd"  #: Parameter for the node addition probability
    P_DELETE = "pDelete"  #: Parameter for the node deletion probability
    DEGREE = "addDegree"  #: Degree of newly-added nodes

    # loci
    NODES = "allnodes"       #: Name of the locus holding all nodes in the network

    def __init__(self):
        super(AddDelete, self).__init__()


    # ---------- Setup and initialisation ----------

    def build(self, params):
        '''Build the model. This method expects parameters for the node addition
        and deletion probabilities, and for the degree of newly-created nodes.

        :param params: the model parameters'''
        pAdd = params[self.P_ADD]
        pDelete = params[self.P_DELETE]

        # stash the degree of new nodes for the events
        self._c = params[self.DEGREE]

        # keep track of all the nodes and edges
        self.addLocus(self.NODES)

        # add events occurring at constant probability regardless of the network size
        self.addFixedRateEvent(self.NODES, pAdd, self.add)
        self.addFixedRateEvent(self.NODES, pDelete, self.remove)

    def setUp(self, params):
        super(AddDelete, self).setUp(params)

        # add all nodes to the all-nodes locus
        g = self.network()
        for n in g.nodes():
            self[self.NODES].addHandler(g, n)


    # ---------- Accessing and evolving the network ----------

    def addNode(self, n, **kwds):
        '''Add a node to the working network. Any keyword arguments added as node attributes.

        :param n: the new node
        :param kwds: (optional) node attributes'''
        super(AddDelete, self).addNode(n, **kwds)
        self[self.NODES].addHandler(self.network(), n)
        #print('Added {n}'.format(n=n))

    def newNodeName(self):
        '''Generate a new name for a node to be added. This is guaranteed not to be
        the name of another node in the network (although it might possibly re-use
        a name of a node that's been removed).

        :returns: the generated name'''
        # sd: might be faster to generate a random name?
        g = self.network()
        i = g.order() + 1
        while i in g.nodes():
            i = i + 1
        return i

    def addNewNode(self, **kwds):
        '''Add a new node to the network with a new, unused name. Any keyword arguments are
        added as node attributes.

        :returns: the generated name of the new node'''
        i = self.newNodeName()
        self.addNode(i, **kwds)
        return i

    def removeNode(self, n):
        '''Remove a node from the working network.

        :param n: the node'''
        self[self.NODES].removeHandler(self.network(), n)
        super(AddDelete, self).removeNode(n)
        #print('removed {n}'.format(n=n))


    # ---------- Events ----------

    def add(self, t, e):
        '''Add a node to the network, connecting it at random to
        other nodes. The degree of the new node is given by the :attr:`DEGREE` parameter,
        with the nodes being selected at random from the entire network.

        :param t: the current simulation time (not used)
        :param e: the element (not used)'''

        # create a new node
        i = self.addNewNode()

        # link to c other nodes (not including i) with uniform probability
        ns = self[self.NODES]
        es = set()
        for m in range(self._c):
            # a probably unnecessary test for parallel edges and self-loops
            while True:
                j = ns.draw()
                if (j not in es) and (i != j):
                    break
            es.add(j)
        for j in es:
            self.addEdge(i, j)

    def remove(self, t, n):
        '''Remove a node from the network.

        :param t: the current simulation time (not used)
        :param n: the node to be removed'''
        self.removeNode(n)