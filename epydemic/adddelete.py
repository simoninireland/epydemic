# Canonical addition-deletion process
#
# Copyright (C) 2017--2020 Simon Dobson
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

import sys
from typing import Any, Dict
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final
from epydemic import Process, Node, Element


class AddDelete(Process):
    '''A process to manage an addition-deletion network, in which nodes are added
    and deleted at random according to some probability. Nodes that are added
    are connected to existing nodes.

    The default behaviour has fixed addition and removal probabilities, independent
    of the size of the network, and a fixed degree for added nodes.'''

    # parameters
    P_ADD: Final[str] = "pAdd"        #: Parameter for the node addition probability
    P_DELETE: Final[str] = "pDelete"  #: Parameter for the node deletion probability
    DEGREE: Final[str] = "addDegree"  #: Degree of newly-added nodes

    # loci
    NODES : Final[str] = "allnodes"       #: Name of the locus holding all nodes in the network

    def __init__(self):
        super().__init__()


    # ---------- Setup and initialisation ----------

    def build(self, params: Dict[str, Any]):
        '''Build the model. This method expects parameters for the node addition
        and deletion probabilities, and for the degree of newly-created nodes.

        :param params: the model parameters'''
        super().build(params)

        # stash the degree of new nodes for the events
        self._c = params[self.DEGREE]

        # keep track of all the nodes and edges
        self.addLocus(self.NODES)

        # add events occurring at constant probability regardless of the network size
        pAdd = params[self.P_ADD]
        pDelete = params[self.P_DELETE]
        self.addFixedRateEvent(self.NODES, pAdd, self.add)
        self.addFixedRateEvent(self.NODES, pDelete, self.delete)

    def setUp(self, params : Dict[str, Any]):
        super().setUp(params)

        # add all nodes to the all-nodes locus
        l = self.locus(self.NODES)
        g = self.network()
        for n in g.nodes():
            l.addHandler(g, n)


    # ---------- Accessing and evolving the network ----------

    def addNode(self, n: Node, **kwds):
        '''Add a node to the working network. Any keyword arguments added as node attributes.

        :param n: the new node
        :param kwds: (optional) node attributes'''
        super().addNode(n, **kwds)
        self.locus(self.NODES).addHandler(self.network(), n)
        #print('added {n}'.format(n=n)

    def newNodeName(self) -> Node:
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

        :param kwds: (optional) node attributes
        :returns: the generated name of the new node'''
        n = self.newNodeName()
        self.addNode(n, **kwds)
        return n

    def removeNode(self, n: Node):
        '''Remove a node from the working network.

        :param n: the node'''
        self.locus(self.NODES).removeHandler(self.network(), n)
        super().removeNode(n)
        #print('removed {n}'.format(n=n))


    # ---------- Events ----------

    def add(self, t: float, e: Element):
        '''Add a node to the network, connecting it at random to
        other nodes. The degree of the new node is given by the :attr:`DEGREE` parameter,
        with the nodes being selected at random from the entire network.

        The node is added to the network by calling :meth:`addNewNode`.

        :param t: the current simulation time (not used)
        :param e: the element (not used)'''

        # create a new node
        i = self.addNewNode()

        # link to c other nodes (not including i) with uniform probability
        ns = self.locus(self.NODES)
        es = set()
        for _ in range(self._c):
            # a probably unnecessary test for parallel edges and self-loops
            while True:
                j = ns.draw()
                if (j not in es) and (i != j):
                    break
            es.add(j)
        for j in es:
            self.addEdge(i, j)

    def delete(self, t: float, n: Node):
        '''Delete a node from the network. The node is
        deleted from the network by calling :meth:`removeNode`.

        :param t: the current simulation time (not used)
        :param n: the node to be removed'''
        self.removeNode(n)
