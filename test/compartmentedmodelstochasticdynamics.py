# Test compartmented model stochastic dynamics, using an SIR model
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

import epyc
import unittest
import networkx
import traceback


class CompartmentedModelStochasticDynamicsTest(unittest.TestCase):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        
        # single experiment
        self._params = dict(pInfect = 0.1,
                            pInfected = 0.01,
                            pRecover = 0.05)
        self._er = networkx.erdos_renyi_graph(1000, 0.005)

        # lab run
        self._lab = epyc.Lab()
        self._lab['pInfect'] = [ 0.1, 0.2, 0.3 ]
        self._lab['pInfected'] = [ 0.01 ]
        self._lab['pRecover'] = [ 0.05, 0.1, 1 ]
    
    def testPopulation( self ):
        '''Test populating a model.'''
        m = SIR()
        e = CompartmentedStochasticDynamics(m, self._er)
        e.setUp(self._params)
                
    def testLoci( self ):
        '''Test we can populate loci correctly.'''
        m = SIR()
        g = networkx.Graph()
        g.add_edges_from([ (1, 2), (2, 3), (1, 4), (3, 4) ])
        e = CompartmentedStochasticDynamics(m, g)
        params = dict(pInfect = 0.1,
                      pInfected = 1.0,    # infect all nodes initially
                      pRecover = 0.05)
        e.setUp(params)

        # keep track of the other compartments as well
        e._model.addLocus(SIR.SUSCEPTIBLE)
        e._model.addLocus(SIR.REMOVED)
        
        # all nodes in I
        self.assertItemsEqual(e._model._loci[SIR.INFECTED].elements(), [ 1, 2, 3, 4 ])

        # one node from I into S, two edges into SI
        m.changeCompartment(e.network(), 1, SIR.SUSCEPTIBLE)
        self.assertItemsEqual(e._model._loci[SIR.INFECTED].elements(), [ 2, 3, 4 ])
        self.assertItemsEqual(e._model._loci[SIR.SUSCEPTIBLE].elements(), [ 1 ])
        self.assertItemsEqual(e._model._loci[SIR.SI].elements(), [ (1, 2), (1, 4) ])

        # recover the infected node
        m.changeCompartment(e.network(), 1, SIR.REMOVED)
        self.assertItemsEqual(e._model._loci[SIR.INFECTED].elements(), [ 2, 3, 4 ])
        self.assertItemsEqual(e._model._loci[SIR.SUSCEPTIBLE].elements(), [])
        self.assertItemsEqual(e._model._loci[SIR.REMOVED].elements(), [ 1 ])
        self.assertItemsEqual(e._model._loci[SIR.SI].elements(), [ ])        
        
    def testRunSingle( self ):
        '''Test a single run of a model.'''
        m = SIR()
        e = CompartmentedStochasticDynamics(m, self._er)
        rc = e.set(self._params).run()
        if not rc[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
            print rc[epyc.Experiment.METADATA][epyc.Experiment.EXCEPTION]
            traceback.print_tb(rc[epyc.Experiment.METADATA][epyc.Experiment.TRACEBACK])
        else:
            print rc[epyc.Experiment.RESULTS]

    @unittest.skip('not yet')
    def testRunMultiple( self ):
        '''Test a run of a model over a (small) parameter space.'''
        m = SIR()
        e = CompartmentedStochasticDynamics(m, self._er)
        self._lab.runExperiment(e)
