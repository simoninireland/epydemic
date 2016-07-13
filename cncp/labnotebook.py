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
    value, or can be deleted.

    Notebooks support both len() and iterator access.'''

    def __init__( self, name = None, description = None ):
        '''Create an empty notebook.

        name: the notebook's name
        description a free text description'''
        self._name = name
        self._description = description
        self._results = dict()
        self._pending = dict()

    def name( self ):
        '''Return the name of the notebook. If the notebook is persistent,
        this likely relates to its storage in some way (for example a
        file name).

        returns: the notebook name'''
        return self._name

    def description( self ):
        '''Return the free text description of the notebook.

        returns: the notebook description'''
        return self._description

    def isPersistent( self ):
        '''By default notebooks are not persistent.

        returns: False'''
        return False

    def commit( self ):
        '''Commit to persistent form. By default does nothing. This should
        be called periodically to save intermediate results: it may happen
        automatically in some sub-classes, depending on their implementation.'''
        pass
    
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
        substituted for the identifier to "finalise" the result.

        result: the result'''
        k = self._parametersAsIndex(result[cncp.Experiment.PARAMETERS])

        # check if result is pending
        if k in self._pending.keys():
            # pending, so finalise it by writing the result and removing the pending record
            self._results[k] = result
            del self._pending[k]
        else:
            # not pending, check if we have a result already
            if k in self._results.keys():
                raise KeyError("Can't overwrite result in notebook")
            else:
                # new result, add to notebook
                self._results[k] = result

    def addPendingResult( self, ps, jobid = None ):
        '''Add a "pending" result that we expect to get results for.

        ps: the parameters for the result
        jobid: an identifier for the pending result (defaults to None)'''
        k = self._parametersAsIndex(ps)

        # check if we already have a result for these parameters
        if k in self._results.keys():
            # yes, can't generate another
            raise KeyError("Already have result")
        else:
            # record job id
            self._pending[k] = jobid

    def cancelPendingResult( self, ps ):
        '''Cancel a pending result. Note that this only affects the
        notebook's record, not any job running in a lab.

        ps: parameters or job id for pending result'''
        if isinstance(ps, dict):
            # parameters, try to remove
            k = self._parametersAsIndex(ps)
            if k in self._pending.keys():
                del self._pending[k]
            else:
                raise KeyError("No pending result for given parameters")
        else:
            # job id, search for it
            for k in self._pending.keys():
                if self._pending[k] == ps:
                    del self._pending[k]
                    return

    def cancelPendingResults( self ):
        '''Cancel all pending results. Note that this only affects the
        notebook's record, not any job running in a lab.'''
        self._pending = dict()

    def pendingResults( self ):
        '''Return the job ids of all pending results.

        returns: a list of job ids'''
        jobs = []
        for k in self._pending.keys():
            jobs.append(self._pending[k])
        return jobs

    def resultPending( self, ps ):
        '''Test whether a result is pending.

        ps: parameters of job id of the result
        returns: True if the result is pending'''
        if isinstance(ps, dict):
            # parameters, check whether they're pending
            k = self._parametersAsIndex(ps)
            return (k in self._pending.keys())
        else:
            # job id, search for it
            for k in self._pending.keys():
                if self._results[k] == ps:
                    return True
                
        # if we get here, there's no pending record
        return False
        
    def result( self, ps ):
        '''Retrieve the result associated with the given parameters.

        ps: the parameters
        returns: the result, or None if the result is pending or not present'''
        k = self._parametersAsIndex(ps)
        if k in self._results.keys():
            return self._results[k]
        else:
            return None

    def results( self ):
        '''Return a list of all the results currently available. This
        excludes pending results.

        returns: a list of results'''
        return [ self._results[k] for k in self._results.keys() ]

    def __len__( self ):
        '''The length of a notebook is the number of results it currently
        has available at present.

        returns: the number of results available'''
        return len(self._results)

    def parameterSpaceSize( self ):
        '''Return the size of the parameter space, i.e., the number of results
        we can eventually expect, the sum of the available and pending results.

        returns: the total size of the experimental parameter space'''
        return len(self._results) + len(self._pending)
    
    def __iter__( self ):
        '''Return an iterator over the results available.

        returns: an iteration over the results'''
        return self.results().__iter__()
    
