# Simulation "lab notebook" for collecting results, in-memory version
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp


class LabNotebook:
    '''A "laboratory notebook" recording the results of a set of
    experiments conducted across a parameter space. The intention is
    to record all the metadata necessary to re-conduct the experiment.

    Notebooks are immutable: once entered, a result can't be deleted
    or changed.

    Notebooks support "pending" results, llowing us to record experiments
    in progress. A pending result can be finalised by providing it with a
    value, or can be deleted.'''

    def __init__( self, name = None ):
        '''Create an empty notebook.'''
        self._name = name
        self._results = dict()

    def name( self ):
        '''Return the name of the notebook.

        returns: the notebook name'''
        return self._name

    def isPersistent( self ):
        '''By default notebooks are not persistent.

        returns: False'''
        return False

    def _parametersAsIndex( self, ps ):
        '''Private method to turn a parameter dict into a string suitable for
        keying a dict.

        ps: the parameters as a hash
        returns: a string key'''
        k = ""
        for p in sorted(ps.keys()):
            v = ps[p]
            k = k + "{p}=[[{v}]];".format(p = p, v = v)
        return k
        
    def addResult( self, result ):
        '''Add a result. This should be a dict as returned from an instance of Experiment,
        that contains metadata, parameters, and result. Results cannot be overridden, as
        notebooks are immutable: however, if the result is pending, the result is
        substitued for the identifier to "finalise" the result.

        result: the result'''
        k = self._parametersAsIndex(result[cncp.Experiment.PARAMETERS])
        if (k in self._results.keys()) and isinstance(self._results[k], dict):
            raise KeyError("Can't overwrite result in notebook")
        else:
            self._results[k] = result

    def addPendingResult( self, ps, jobid = None ):
        '''Add a "pending" result that we expect to get results for.

        ps: the parameters for the result
        jobid: an identifier for the pending result (defaults to None)'''
        k = self._parametersAsIndex(ps)
        self._results[k] = jobid

    def cancelPendingResult( self, ps ):
        '''Cancel a pending result.

        ps: parameters or job id for pending result'''
        if isinstance(ps, dict):
            # parameters, try to remove
            k = self._parametersAsIndex(ps)
            if k in self._results.keys():
                if isinstance(self._results[k], dict):
                    raise KeyError("Can't delete existing result from notebook")
                else:
                    del self._results[k]
            else:
                raise KeyError("No result for given parameters in notebook")
        else:
            # job id, search for it
            for k in self._results.keys():
                if not isinstance(self._results[k], dict):
                    if self._results[k] == ps:
                        del self._results[k]
                        return
                    
            # if we get here, fail
            raise KeyError("No result for given parameters in notebook")

    def pendingResults( self ):
        '''Return the job ids of all pending results.

        returns: a list of job ids'''
        jobs = []
        for k in self._results.keys():
            jobid = self._results[k]
            if (not isinstance(jobid, dict)) and (jobid is not None):
                jobs.append(jobid)
        return jobs
         
    def resultPending( self, ps ):
        '''Test whether a result is pending.

        ps: the parameters of the result
        returns: True if the result is pending'''
        k = self._parametersAsIndex(ps)
        if k in self._results.keys():
            return (not isinstance(self._results[k], dict))
        else:
            return False
        
    def result( self, ps ):
        '''Retrieve the result associated with the given parameters.

        ps: the parameters
        returns: the result, or None if the result is pending or not present'''
        k = self._parametersAsIndex(ps)
        if (k in self._results.keys()) and (isinstance(self._results[k], dict)):
            return self._results[k]
        else:
            return None

    def results( self ):
        '''Return a list of all the results currently available. This
        excludes pending results.

        returns: a list of results'''
        return [ self._results[k] for k in self._results.keys() if isinstance(self._results[k], dict) ]
    
       
