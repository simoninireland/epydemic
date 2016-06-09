# Tests of sequential lab class
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

from cncp import *

import unittest
import numpy


class SampleExperiment(Experiment):
    '''A very simple experiment that adds up its parameters.'''

    def do( self, param ):
        total = 0
        for k in param:
            total = total + param[k]
        return dict(total = total)
            
        
class LabTests(unittest.TestCase):

    def setUp( self ):
        '''Create a lab in which to perform tests.'''
        self._lab = Lab()
        
    def testMixup( self ):
        '''Test that parameter spaces are suitably mixed, defined as not
        more than 0.5% of elements landing in their original place'''
        n = 1000
        
        l = numpy.arange(0, n)
        self._lab._mixup(l)
        sp = [ v for v in (l == numpy.arange(0, n)) if v ]
        self.assertTrue(len(sp) <= (n / 0.005))

    def testParameterOne( self ):
        '''Test that we can set a single parameter.'''
        self._lab['a'] = numpy.arange(0, 100)
        
        self.assertEqual(len(self._lab['a']), len(numpy.arange(0, 100)))
        for i in numpy.arange(0, 100):
            self.assertIn(i, self._lab['a'])

    def testParameterThree( self ):
        '''Test that we can set several parameters.'''
        self._lab['a'] = numpy.arange(0, 100)
        self._lab['b'] = numpy.arange(0, 1000)
        self._lab['c'] = numpy.arange(10, 50, 10)
        
        self.assertEqual(len(self._lab['a']), len(numpy.arange(0, 100)))
        for i in numpy.arange(0, 100):
            self.assertIn(i, self._lab['a'])
        self.assertEqual(len(self._lab['b']), len(numpy.arange(0, 1000)))
        for i in numpy.arange(0, 1000):
            self.assertIn(i, self._lab['b'])
        self.assertEqual(len(self._lab['c']), len(numpy.arange(10, 50, 10)))
        for i in numpy.arange(10, 50, 10):
            self.assertIn(i, self._lab['c'])

    def testRunOne( self ):
        '''Test that a simple experiment runs against a 1D parameter space.'''
        n = 100

        r = numpy.arange(0, n)
        self._lab['a'] = r
        res = self._lab.runExperiment(SampleExperiment())

        # check that the whole parameter space has a result
        self.assertEqual(len(res), n)
        for p in res:
            self.assertIn(p['parameters']['a'], r)

        # check that each result corresponds to its parameter
        for p in res:
            self.assertEqual(p['parameters']['a'], p['total'])

    def testRunTwo( self ):
        '''Test that a simple experiment runs against a 2D parameter space.'''
        n = 100

        r = numpy.arange(0, n)
        self._lab['a'] = r
        self._lab['b'] = r
        res = self._lab.runExperiment(SampleExperiment())

        # check that the whole parameter space has a result
        self.assertEqual(len(res), n * n)
        for p in res:
            self.assertIn(p['parameters']['a'], r)
            self.assertIn(p['parameters']['b'], r)

        # check that each result corresponds to its parameter
        for p in res:
            self.assertEqual(p['parameters']['a'] + p['parameters']['b'], p['total'])
 
        
