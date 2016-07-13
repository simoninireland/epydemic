# Simulation "lab notebook" for collecting results, JSON version
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp
import os
import json


class JSONLabNotebook(cncp.LabNotebook):
    '''A lab notebook that persists intself to a JSON file.'''

    def __init__( self, name, create = False, description = None ):
        '''Create a new JSON notebook, using the notebook's name
        as the JSON file. If this file exists, it will be opened
        and loaded unless create is True, in which case it will
        be erased.

        name: JSON file to persist the notebook to
        create: if True, erase existing file (defaults to False)
        description: free text description of the notebook'''
        cncp.LabNotebook.__init__(self, name, description)

        # check for the file already existing
        if os.path.isfile(self.name()):
            # file exists, do we load it or create into it?
            if create:
                # empty the file
                with open(self.name(), 'w') as f:
                    f.write('')

                # preserve any description we were passed
                self._description = description
            else:
                # load notebook from file
                self._load(self.name())

    def isPersistent( self ):
        '''Return True to indicate the notebook is persisted to a JSON file.

        returns: True'''
        return True

    def commit( self ):
        '''Persist to disc.'''
        self._save(self.name())
        
    def _load( self, fn ):
        '''Retrieve the notebook from the given file.

        fn: the file name'''

        # if file is empty, create an empty notebook
        if os.path.getsize(fn) == 0:
            self._description = None
            self._results = dict()
            self._pending = dict()
        else:
            # load the JSON object
            with open(fn, "r") as f:
                s = f.read()

                # parse back into appropriate variables
                j = json.loads(s)
                self._description = j['description']
                self._pending = j['pending']
                self._results = j['results']
        
    def _save( self, fn ):
        '''Persist the notebook to the given file.

        fn: the file name'''

        # create JSON object
        j = json.dumps({ "description": self.description(),
                         "pending": self._pending,
                         "results": self._results },
                       indent = 4)
        
        # write to file
        with open(fn, 'w') as f:
            f.write(j)
            

    
