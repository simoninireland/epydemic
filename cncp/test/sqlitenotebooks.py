# Tests of Sqlite notebooks
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


class SqlliteLabNotebookTests(unittest.TestCase):

    def testCreateDatabaseInMemory( self ):
        '''Test creation of notebook using SQLite database in memory'''
        db = SqliteLabNotebook('test')
        self.assertFalse(db.isPersistent())
        self.assertEqual(db.name(), 'test')

    def testCreateDatabase( self ):
        '''Test creation of notebook using SQLite database in a file'''
        tf = NamedTemporaryFile()
        tf.close()
        fn = tf.name
        
        db = SqliteLabNotebook('test', fn)
        self.assertTrue(db.isPersistent())
        self.assertEqual(db.name(), 'test')
        self.assertTrue(os.path.isfile(fn))
        os.remove(fn)
