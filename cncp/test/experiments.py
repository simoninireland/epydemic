# Tests of experiments class
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

from cncp import *

import unittest
import time


class SampleExperiment0(Experiment):
    '''A base experiment that records the phases of the experiment.'''
    
    def __init__( self ):
        Experiment.__init__(self)
        self._ps = []
        
    def setUp( self ):
        self._ps.append('setup')

    def tearDown( self ):
        self._ps.append('teardown')
        
    def do( self, params ):
        self._ps.append('do')
        return dict()

    def report( self, res ):
        ext = Experiment.report(self, res)
        ext[self.METADATA]['phases'] = self._ps
        return ext

class SampleExperiment1(Experiment):
    '''An experiment that does literally nothing.'''
    
    def do( self, params ):
        pass

class SampleExperiment2(SampleExperiment0):
    '''An experiment that does nothing for 1s and returns a results dict.'''
    
    def do( self, params ):
        time.sleep(1)
        return SampleExperiment0.do(self, params)

class SampleExperiment3(SampleExperiment0):
    '''An experiment that does a calculation.'''
    
    def do( self, params ):
        return dict(result = params['a'] + params['b'])

class SampleExperiment4(SampleExperiment0):
    '''An experiment that makes sure there are timings to test.'''
    
    def setUp( self ):
        time.sleep(1)

    def tearDown( self ):
        time.sleep(1)

    def do( self, params ):
        time.sleep(1)
        return dict()

class SampleExperiment5(SampleExperiment0):
    '''An experiment that fails in its main action.'''
    
    def do( self, params ):
        raise Exception('We failed (on purpose)')
   
class SampleExperiment6(SampleExperiment0):
    '''An experiment that fails in its setup, and so should not do a teardown.'''
    
    def setUp( self ):
        raise Exception('We failed (on purpose)')

class SampleExperiment7(SampleExperiment0):
    '''An experiment that fails in its teardown.'''
    
    def tearDown( self ):
        raise Exception('We failed (on purpose)')


class ExperimentTests(unittest.TestCase):

    def testNoResults( self ):
        '''Test do() not returning results.'''
        e = SampleExperiment1()
        params = dict()
        res = e.runExperiment(params)
        self.assertTrue(res[Experiment.METADATA][Experiment.STATUS])

    def testPhases( self ):
        '''Test that phases execute correctly.'''
        e = SampleExperiment2()
        params = dict()
        res = e.runExperiment(params)
        self.assertTrue(res[Experiment.METADATA][Experiment.STATUS])
        self.assertIn('phases', res[Experiment.METADATA].keys())
        self.assertEqual(res[Experiment.METADATA]['phases'], [ 'setup', 'do', 'teardown' ])

    def testParameters( self ):
        '''Test that parameters are recorded properly.'''
        e = SampleExperiment2()
        params = dict(a = 1, b = 1.0, c = 'hello world')
        res = e.runExperiment(params)
        self.assertTrue(res[Experiment.METADATA][Experiment.STATUS])
        self.assertIn(Experiment.PARAMETERS, res.keys())
        for k in params.keys():
            self.assertEqual(res[Experiment.PARAMETERS][k], params[k])

    def testReporting( self ):
        '''Test that results are reported properly.'''
        e = SampleExperiment3()
        params = dict(a = 1, b = 2, c = 'hello world')
        res = e.runExperiment(params)
        self.assertTrue(res[Experiment.METADATA][Experiment.STATUS])
        self.assertIn('result', res[Experiment.RESULTS].keys())
        self.assertEqual(res[Experiment.RESULTS]['result'], params['a'] + params['b'])

    def testTiming( self ):
        '''Test that timings are plausible.'''
        e = SampleExperiment4()
        params = dict()
        res = e.runExperiment(params)
        self.assertTrue(res[Experiment.METADATA][Experiment.STATUS])

        timing = res[Experiment.METADATA]
        self.assertTrue(timing[Experiment.END_TIME] > timing[Experiment.START_TIME])
        self.assertTrue(timing[Experiment.ELAPSED_TIME] > 0)
        self.assertTrue(timing[Experiment.SETUP_TIME] > 0)
        self.assertTrue(timing[Experiment.EXPERIMENT_TIME] > 0)
        self.assertTrue(timing[Experiment.TEARDOWN_TIME] > 0)
        self.assertTrue(timing[Experiment.ELAPSED_TIME] >= timing[Experiment.SETUP_TIME] + timing[Experiment.TEARDOWN_TIME] + timing[Experiment.EXPERIMENT_TIME])

    def testException( self ):
        '''Test that exceptions are caught and reported in-line.'''
        e = SampleExperiment5()
        params = dict()
        res = e.runExperiment(params)
        self.assertFalse(res[Experiment.METADATA][Experiment.STATUS])
        self.assertIn('phases', res[Experiment.METADATA].keys())
        self.assertEqual(res[Experiment.METADATA]['phases'], [ 'setup', 'teardown' ])

    def testExceptionInSetup( self ):
        '''Test that exceptions in setup are caught and not torn down.'''
        e = SampleExperiment6()
        params = dict()
        res = e.runExperiment(params)
        self.assertFalse(res[Experiment.METADATA][Experiment.STATUS])
        self.assertIn('phases', res[Experiment.METADATA].keys())
        self.assertEqual(res[Experiment.METADATA]['phases'], [ ])

    def testExceptionInTeardown( self ):
        '''Test that exceptions in teardown are caught.'''
        e = SampleExperiment7()
        params = dict()
        res = e.runExperiment(params)
        self.assertFalse(res[Experiment.METADATA][Experiment.STATUS])
        self.assertIn('phases', res[Experiment.METADATA].keys())
        self.assertEqual(res[Experiment.METADATA]['phases'], [ 'setup', 'do' ])

    def testRecordingOnObject( self ):
        '''Test that everything is also available through the experiment object.'''
        e = SampleExperiment3()
        params = dict(a = 1, b = 1.0, c = 'hello world')
        e.runExperiment(params)
        res = e.results()
        self.assertTrue(res[Experiment.METADATA][Experiment.STATUS])
        self.assertEqual(res[Experiment.METADATA][Experiment.STATUS], e.success())
        self.assertIn('result', res[Experiment.RESULTS].keys())
        self.assertEqual(res[Experiment.RESULTS]['result'], params['a'] + params['b'])

