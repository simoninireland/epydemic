# Simulation "lab notebook" for collecting results, in-memory version
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

class LabNotebook:
    '''A "laboratory notebook" recording the results of a set of
    experiments conducted across a parameter space. The intention is
    to record all the metadata necessary to re-conduct the experiment.'''

    def __init__( self, name ):
        '''Create an empty notebook.'''
        self._name = name

    def name( self ):
        '''Return the name of the notebook.

        returns: the notebook name'''
        return self._name

    def isPersistent( self ):
        '''By default notebooks are not persistent.

        returns: False'''
        return False


