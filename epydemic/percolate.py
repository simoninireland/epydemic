# Bond percolation process
#
# Copyright (C) 2020 Simon Dobson
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

from epydemic import Process, Edge
import numpy                      # type: ignore
import sys
if sys.version_info >= (3, 7):
    from typing import Final, Dict, Any, List
else:
    # backport compatibility with older typing
    from typing import Dict, Any, List
    from typing_extensions import Final


class Percolate(Process):
    '''A process that bond percolates a network with a given occupation probability. This
    can be used independently as a basis for percolation experiments, or as a precursor
    to other processes that need to run on a percolated network.
    
    Note that the percolation process defines no events: it performs percolation during
    the :meth:`build` method.'''
    
    # Experimental parameters
    T : Final[str] = 'epydemic.percolate.T'   #: Experimental parameter for the occupation probability of an edge.
    
    
    def __init__(self):
        super(Percolate, self).__init__()
    
    def percolate(self, T : float) -> List[Edge]:
        '''Percolate the network. Edges are retained ("occupied") with probability :math:`T`,
        with other edges being "unoccupied" with probability :math:`(1 - T)`.
        
        :param params: the experimental parameters
        :returns: the set of edges to be removed, i.e., those that are unoccupied'''
        rng = numpy.random.default_rng()
        g = self.network()
        
        # percolate the network
        unoccupied = []
        for e in g.edges():
            # edges are occupied with probability T
            if rng.random() > T:
                # retain unoccupied edges
                unoccupied.append(e)
                
        # return the unoccupied edges
        return unoccupied
        
    def unoccupy(self, unoccupied : List[Edge]):
        '''Handle edges, given the set that is left unoccupied by the percolation
        process. The default removes the unoccupied edges. This can be overridden to
        change the action.
        
        :param unoccupied: set of unoccupied'''''
        g = self.network()
        g.remove_edges_from(unoccupied)

    def build(self, params : Dict[str, Any]):
        '''Percolate the network.
        
        :param params: the experimental parameters'''
        super(Percolate, self).build(params)
        
        # percolate the network
        T = params[self.T]
        unoccupied = self.percolate(T)
        self.unoccupy(unoccupied)

