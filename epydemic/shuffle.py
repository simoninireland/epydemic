# Degree-preserving shuffles of edges
#
# Copyright (C) 2021 Simon Dobson
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
import numpy
from networkx import Graph
from epydemic import Process, DrawSet


class ShuffleK(Process):
    '''A degree-preserving shuffle that rewrites the edges of its
    network while maintaiing the node degrees.'''

    # Experimental parameters
    REWIRE_FRACTION: Final[str] = "epydemic.shufflek.rewire"        #: Parameter for the fraction of edges to rewire.

    def __init__(self):
        super().__init__()


    # ---------- Setup and initialisation ----------

    def build(self, params: Dict[str, Any]):
        '''Shuffle the network while preserving node degrees.

        :param params: the experimental parameters'''
        super().build(params)

        # extract the rewiring fraction
        f = params[self.REWIRE_FRACTION]

        # perform rewiring
        g = self.network()
        bins = self._networkDetails(g)
        es = list(g.edges)
        numpy.random.shuffle(es)
        M = len(es)
        imax = int(M * f)
        i = 0
        while i < imax:
            # choose a random edge
            if len(es) == 0:
                # we need more edges, re-fill the random sequence again
                es = list(g.edges)
                numpy.random.shuffle(es)
            (a, b) = es[0]
            es = es[1:]

            # check for an edge we're already rewired
            if not g.has_edge(a, b):
                continue

            # get the degrees of the endpoints
            ka = g.degree(a)
            kb = g.degree(b)

            # choose another node of degree ka, which can't be a or b
            if len(bins[ka]) == 1:
                # no other nodes with this degree, try the other way round
                if len(bins[kb]) == 1:
                    # no node of that degree either, choose again
                    continue
                else:
                    # swap a and b
                    a, b = b, a
                    ka, kb = kb, ka
            if len(bins[ka]) == 2 and ka == kb:
                # a and b have the same degree and are the only
                # nodes with that degree, draw again
                continue
            while True:
                c = bins[ka].draw()
                if c not in [a, b]:
                    break

            # choose a random neighbour of c, which mustn't be a, b, or c
            ds = DrawSet(g.neighbors(c), [a, b, c])
            if len(ds) == 0:
                # no neighbours left, draw again
                continue
            d = ds.draw()
            #print(f'{c}-{d}')

            # check for parallel edges in the proposed rewiring
            if g.has_edge(a, d) or g.has_edge(c, b):
                continue

            # rewire edge a-b and c-d to be a-d and c-b
            #print(f'{a}-{b} & {c}-{d} -> {a}-{d} & {c}-{b}')
            g.remove_edges_from([(a, b), (c, d)])
            g.add_edges_from([(a, d), (c, b)])

            # yay, success!
            i += 1

    def _networkDetails(self, g: Graph):
        '''Collect information about the network's node degrees and
        their link to edges.

        :param g: the network:
        returns: a dict from degree to a set of nodes
        '''
        bins = dict()
        for (n, d) in g.degree():
            # add node to correct bin
            if d not in bins:
                bins[d] = DrawSet()
            bins[d].add(n)

        return bins
