# Functions to create and display lattice networks.
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import networkx as nx
import numpy as np


def lattice_graph( lattice_rows, lattice_columns ):
    """Create a regular 2D lattice with the given dimensions."""
    
    # create the graph and populate with nodes indexed by a single integer
    lattice = nx.Graph()
    lattice.add_nodes_from(xrange(lattice_rows * lattice_columns))
    
    # add edges to the main body of the lattice
    for r in xrange(0, lattice_rows - 1):             # sweep top-left to bottom-right
        for c in xrange(0,lattice_columns - 1):
            i = r * lattice_columns + c
            lattice.add_edge(i, i + 1)                # edge to right neighbour
            lattice.add_edge(i, i + lattice_columns)  # edge to south neighbour (row below)
        
    # add edges along the right-hand column
    for r in xrange(0, lattice_rows - 1):
        i = (r + 1) * lattice_columns - 1    
        lattice.add_edge(i, i + lattice_columns)      # edge to south neighbour (row below)
        
    # add edges along the bottom (south) edge
    for c in xrange(0, lattice_columns - 1):
        i = (lattice_rows - 1) * lattice_columns + c        
        lattice.add_edge(i, i + 1)                    # edge to right neighbour
        
    return lattice


def lattice_positions( lattice, lattice_rows, lattice_columns ):
    """Return a dictionary of positions for nodes laid out in a lattice."""
    pos = dict()
    rh = 1.0 / (lattice_rows)           # row height
    cw = 1.0 / (lattice_columns)        # column width
    
    # run through the rows and columns, laying-out nodes as we go
    # and storing their co-ordinates into pos. Co-ordinates lie in
    # the range [0.0 ... 1.0]
    nodes = lattice.nodes_iter()
    try:
        for r in xrange(lattice_rows):
            for c in xrange(lattice_columns):
                n = nodes.next()
                pos[n] = (c * cw,
                          1.0 - r * rh) # lowest nodes in the top row, not the bottom
    except StopIteration:
        # ran out of nodes, so drop through
        pass
    
    return pos


def draw_lattice(g, lattice_rows = None, lattice_columns = None, **kwds):
    """Draw the graph with a lattice layout.
    
    g: the network to position
    lattice_rows: the number of rows in the lattice
    lattice_columns: the number of columns in the lattice
    """
    
    # fill in the argument defaults where not specified
    if lattice_rows is not None:
        if lattice_columns is None:
            # rows fixed, set the columns
            lattice_columns = g.order() / lattice_rows
            if g.order() % lattice_rows > 0:
                lattice_columns = lattice_columns + 1
    else:
        if lattice_columns is None:
            # neither rows nor columns fixed, set both
            lattice_rows = lattice_columns = int(np.sqrt(g.order()))
            if lattice_rows * lattice_columns < g.order():
                lattice_rows = lattice_rows + 1
        else:
            # columns fixed, set the rows
            lattice_rows = g.order() / lattice_columns
            if g.order() % lattice_columns > 0:
                lattice_rows = lattice_rows + 1

    # compute the layout using these dimensions
    pos = lattice_positions(g, lattice_rows, lattice_columns)
    
    # pass through the layout and any additional keyword arguments
    return nx.draw_networkx(g, pos, **kwds)
