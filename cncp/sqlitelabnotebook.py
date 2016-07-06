# Simulation "lab notebook" for collecting results, persistent version using SQLite
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp
import sqlite3
import os
import os.path

class SqliteLabNotebook(cncp.LabNotebook):
    '''A "laboratory notebook" recording the results of a set of
    experiments conducted across a parameter space. The intention is
    to record all the metadata necessary to re-conduct the experiment.'''

    # names of significant database elements
    EXPERIMENT_METADATA_TABLE = "experiment_metadata"
    EXPERIMENT_ID = "id"
    RESULTS_ID = "job"
    
    def __init__( self, name, dbfile = ':memory:', create = False ):
        '''Create an empty notebook in the given database file, or in
        memory by default.

        dbfile: name of the database. By default creates an in-memory database
        create: if True, overwrite any existing database in the named file.
                By default opens the database'''
        cncp.LabNotebook.__init__(self, name)
        
        self._dbfile = dbfile
        self._connection = None

        # if file exists, open or create the database
        if os.path.isfile(self._dbfile):
            # file exists, open or create?
            if create:
                # creating, erase the file and create a new database
                os.remove(self._dbfile)
                self.open()
                self._createDatabase()
            else:
                # re-using, open the database
                self.open()
        else:
            # file doesn't exist or is in memory, create database
            self.open()
            self._createDatabase()

    def isPersistent( self ):
        '''Tests whether the notebook is persistent (i.e., stored on disc).

        returns: True if notebook is persistent, False otherwise'''
        return not (self._dbfile == ':memory:')
        
    def open( self ):
        '''Open the database connection.'''
        if self._connection is None:
            self._connection = sqlite3.connect(self._dbfile)

    def close( self ):
        '''Close the database connection.'''
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def commit( self ):
        '''Private method to commit changes to database.'''
        self._connection.commit()
        
    def _createDatabase( self ):
        '''Private method to create the SQLite database file.'''

        # create experiment metadata table
        command = """
                  CREATE TABLE {tn} (
                  {k}             INT PRIMARY KEY NOT NULL,
                  START_TIME      INT             NOT NULL,
                  END_TIME        INT             NOT NULL,
                  ELAPSED_TIME    INT             NOT NULL,
                  SETUP_TIME      INT             NOT NULL,
                  EXPERIMENT_TIME INT             NOT NULL,
                  TEARDOWN_TIME   INT             NOT NULL,
                  STATUS          BOOLEAN         NOT NULL)
                  """
        self._connection.execute(command.format(tn = self.EXPERIMENT_METADATA_TABLE,
                                                k = self.EXPERIMENT_ID))
        
        # commit the changes
        self.commit()
        
    def addExperiment( self, rc ):
        '''Add the results of an experiment to the notebook. The dict
        of results should be structured according to the Experiment
        class, with metadata and results stored separately. The
        metadata is placed into the experiment_metadata table,
        the results into the experiment_results table; and the two
        linked through the experiment_instances table.

        rc: the dict of experimental results'''
        pass
