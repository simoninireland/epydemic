# Tests of SIR under stochastic dynamics
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

from cncp import *
from .sir import SIRTests

import epyc
import unittest
import networkx

class SIRConsistency(SIRStochasticDynamics):
    '''An extension of the SIRStochasticDynamics class that performs sanity
    checks on the internal data structures after every event.'''
    
    def sanity( self ):
        g = self.network()
        
        # check that all nodes on the infected list are infected
        infecteds = [ n for n in self._infected if g.node[n][self.DYNAMICAL_STATE] != self.INFECTED ]
        if len(infecteds) > 0:
            raise Exception('Un-infected node in infected list')

        # check that all infected nodes are on the infected list
        infecteds = [ n for n in g.nodes_iter() if g.node[n][self.DYNAMICAL_STATE] == self.INFECTED ]
        if set(infecteds) != set(self._infected):
            raise Exception('Infected node not in infected list')

        # check that all SI edges do indeed connect an I to an S (specifically in that order)]
        for (n, m, data) in self._si:
            if (g.node[n][self.DYNAMICAL_STATE] != self.INFECTED) or (g.node[m][self.DYNAMICAL_STATE] != self.SUSCEPTIBLE):
                raise Exception('SI edge not properly formed')

        # check that all SI edges are in the SI edge list
        for n in self._infected:
            for (_, m) in g.edges_iter(n):
                if (g.node[m][self.DYNAMICAL_STATE] == self.SUSCEPTIBLE):
                    if len([ (np, mp, datap) for (np, mp, datap) in self._si if n == np and m == mp ]) == 0:
                        raise Exception('Umanaged SI edge')

    def infect( self, t, params ):
        '''Check sanity of infect event.'''
        ni = len(self._infected)
        super(SIRConsistency, self).infect(t, params)
        if len(self._infected) != ni + 1:
            raise Exception("Infection event didn't generate one new infected node")
        self.sanity()

    def recover( self, t, params ):
        '''Check sanity of recover event.'''
        ni = len(self._infected)
        super(SIRConsistency, self).recover(t, params)
        if len(self._infected) != ni - 1:
            raise Exception("Recovery event didn't recover one infected node")
        self.sanity()

    def at_equilibrium( self, t ):
        '''Check sanity of equilibrium check.'''
        rc = super(SIRConsistency, self).at_equilibrium(t)
        if rc:
            if len(self._si) > 0:
                raise Exception('Termination still leaves SI edges')
        return rc

    
class SIRStochasticTests(SIRTests):

    def setUp( self ):
        super(SIRStochasticTests, self).setUp()
        self._experiment = SIRStochasticDynamics(self._er)
 
    def testConsistency( self ):
        '''Test the data structure consistency over a simulation (slow).'''
        self._experiment.set(self._params).run()
        res = self._experiment.results()
