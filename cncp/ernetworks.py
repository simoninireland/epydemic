# Functions for ER networks
#
# Copyright (C) 2014-2017 Simon Dobson
# 
# This file is part of Complex networks, complex processes (CNCP).
#
# CNCP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CNCP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CNCP. If not, see <http://www.gnu.org/licenses/gpl.html>.

import networkx as nx


def erdos_renyi_graph_from_scratch( n, pEdge ):
    """Build the graph with n nodes and a probability pEdge of there
    being an edge between any pair of nodes.
    
    n: number of nodes in the network
    pEdge: probability that there is an edge between any pair of nodes"""
    g = nx.empty_graph(n)
    
    # run through all the possible edges
    ne = 0
    for i in xrange(n):
        for j in xrange(i + 1, n):
            if rnd.random() <= pEdge:
                ne = ne + 1
                g.add_edge(i, j, { 'added': ne })
    
    return g
