# Tests of in-memory notebooks
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

from cncp import *

import unittest
import os
from tempfile import NamedTemporaryFile


class SampleExperiment(Experiment):
    '''A very simple experiment that adds up its parameters.'''

    def do( self, param ):
        total = 0
        for k in param:
            total = total + param[k]
        return dict(total = total)

    
class LabNotebookTests(unittest.TestCase):

    def testEmptyNotebook( self ):
        '''Test creating an empty notebook'''
        nb = LabNotebook("test")
        self.assertEqual(nb.name(), "test")
        self.assertFalse(nb.isPersistent())
        
    def testAddingResult( self ):
        '''Test adding and retrieving a result'''
        nb = LabNotebook()

        e = SampleExperiment()
        params = dict(a  = 1, b = 2)
        rc = e.runExperiment(params)

        nb.addResult(rc)

        self.assertFalse(nb.resultPending(params))
        self.assertNotEqual(nb.result(params), None)

        params2 = dict(b = 2, a  = 1)
        self.assertNotEqual(nb.result(params2), None)

        res = nb.results()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][Experiment.RESULTS]['total'], params['a'] + params['b'])

    def testAddingPendingResult( self ):
        '''Test adding, finalising, and retrieving a pending result'''
        nb = LabNotebook()

        e = SampleExperiment()
        params = dict(a  = 1, b = 2)
        rc = e.runExperiment(params)

        nb.addPendingResult(params, 1)
        self.assertEqual(nb.result(params), None)
        self.assertEqual(len(nb.results()), 0)
        self.assertEqual(nb.pendingResults(), [ 1 ])

        nb.addResult(rc)
        self.assertEqual(nb.result(params), rc)
        self.assertEqual(len(nb.results()), 1)
        self.assertEqual(len(nb.pendingResults()), 0)

    def testCancellingPendingResult( self ):
        '''Test cancelling a pending result'''
        nb = LabNotebook()

        params = dict(a  = 1, b = 2)
        nb.addPendingResult(params, 1)
        self.assertEqual(nb.result(params), None)
        self.assertEqual(len(nb.results()), 0)
        self.assertEqual(nb.pendingResults(), [ 1 ])

        nb.cancelPendingResult(params)
        self.assertEqual(nb.result(params), None)
        self.assertEqual(len(nb.results()), 0)
        self.assertEqual(len(nb.pendingResults()), 0)
    
    def testRealAndPendingResults( self ):
        '''Test a sequence of real and pending results'''
        nb = LabNotebook()

        e = SampleExperiment()
        
        params1 = dict(a  = 1, b = 2)
        rc1 = e.runExperiment(params1)

        params2 = dict(a  = 10, b = 12)
        rc2 = e.runExperiment(params2)

        params3 = dict(a  = 45, b = 11)
        rc3 = e.runExperiment(params3)

        nb.addResult(rc1)
        self.assertEqual(nb.result(params1), rc1)
        self.assertEqual(len(nb.results()), 1)
        self.assertEqual(nb.pendingResults(), [ ])
        
        nb.addPendingResult(params2, 2)
        self.assertEqual(nb.result(params1), rc1)
        self.assertEqual(nb.result(params2), None)
        self.assertEqual(len(nb.results()), 1)
        self.assertEqual(nb.pendingResults(), [ 2 ])
        
        nb.addPendingResult(params3, 3)
        self.assertEqual(nb.result(params1), rc1)
        self.assertEqual(nb.result(params2), None)
        self.assertEqual(nb.result(params3), None)
        self.assertEqual(len(nb.results()), 1)
        self.assertEqual(len(nb.pendingResults()), 2)

        nb.addResult(rc2)
        self.assertEqual(nb.result(params1), rc1)
        self.assertEqual(nb.result(params2), rc2)
        self.assertEqual(nb.result(params3), None)
        self.assertEqual(len(nb.results()), 2)
        self.assertEqual(nb.pendingResults(), [ 3 ])

        nb.cancelPendingResult(3)
        self.assertEqual(nb.result(params1), rc1)
        self.assertEqual(nb.result(params2), rc2)
        self.assertEqual(nb.result(params3), None)
        self.assertEqual(len(nb.results()), 2)
        self.assertEqual(nb.pendingResults(), [ ])

        nb.addPendingResult(params3, 3)
        self.assertEqual(nb.result(params1), rc1)
        self.assertEqual(nb.result(params2), rc2)
        self.assertEqual(nb.result(params3), None)
        self.assertEqual(len(nb.results()), 2)
        self.assertEqual(nb.pendingResults(), [ 3 ])

        nb.cancelPendingResult(params3)
        self.assertEqual(nb.result(params1), rc1)
        self.assertEqual(nb.result(params2), rc2)
        self.assertEqual(nb.result(params3), None)
        self.assertEqual(len(nb.results()), 2)
        self.assertEqual(nb.pendingResults(), [ ])
