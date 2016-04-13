# Makefile for "Complex networks, complex processes"
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

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
