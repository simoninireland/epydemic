# Base class for tests of SIR under various simulation dynamics
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

from cncp import *
#
import epyc
import unittest
import networkx


class SIRTests(unittest.TestCase):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        
        # single experiment
        self._params = dict(pInfect = 0.01,
                            pInfected = 0.001,
                            pRecover = 0.02)
        self._er = networkx.erdos_renyi_graph(5000, 0.004)

        # lab run
        self._lab = epyc.Lab()
        self._lab['pInfect'] = [ 0.01 ]
        self._lab['pInfected'] = [ 0.001, 0.002, 0.005 ]
        self._lab['pRecover'] = [ 0.02 ]
 
    
    def testSingle( self ):
        '''Test a single run of SIR.'''
        self._experiment.set(self._params).run()
        res = self._experiment.results()
        #print res
        
        self.assertIn('timesteps', res[epyc.Experiment.RESULTS])
        self.assertIn('events', res[epyc.Experiment.RESULTS])
        self.assertTrue(res[epyc.Experiment.RESULTS]['events'] > 0)
        self.assertIn('mean_outbreak_size', res[epyc.Experiment.RESULTS])

    def testLab( self ):
        '''Test successful SIR experiments across a parameter space.'''       
        self._lab.runExperiment(self._experiment)
        rcs = self._lab.results()
        #print rcs

        self.assertTrue(len(rcs), 3)
        for res in rcs:
            self.assertIn('timesteps', res[epyc.Experiment.RESULTS])
            self.assertIn('events', res[epyc.Experiment.RESULTS])
            self.assertTrue(res[epyc.Experiment.RESULTS]['events'] > 0)
            self.assertIn('mean_outbreak_size', res[epyc.Experiment.RESULTS])

    def testInfection( self ):
        '''Test that an experiment converges.'''
        self._experiment.set(self._params).run()
        res = self._experiment.results()
        #print res
        
        self.assertTrue(res[epyc.Experiment.RESULTS]['mean_outbreak_size'] > 0.5)
        
        
