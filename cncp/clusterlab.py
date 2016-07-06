# Simulation "lab" experiment management, parallel cluster version
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp
import numpy
import pickle
import dill
from ipyparallel import Client


class ClusterLab(cncp.Lab):
    '''A laboratory running over a cluster. Experiments are submitted to
    engines in the cluster for execution in parallel, with the experiments
    being performed asynchronously to allow for disconnection and subsequent
    retrieval of results. Combined with a persistent LabNotebook, this
    allows for fully decoupled access to an on-going computational
    experiment with pircewis retrieval.

    This class requires a cluster to already be set up and running, configured
    for persistent access, with access to the necessary code and libraries,
    and with appropriate security information available.'''

    def __init__( self, name = None, robust = False, url_file = None, profile = None, profile_dir = None, ipython_dir = None, context = None, debug = False, sshserver = None, sshkey = None, password = None, paramiko = None, timeout = 10, cluster_id = None, **extra_args ):
        '''Create an empty lab attached to the given cluster. most of the arguments
        are as expected by the ipyparallel.Client class, and are used to create the
        underlying connection to the cluster.

        Lab arguments:
           name: the lab name, used for documentation
           robust: if True, ignores individual job failures (defaults to False)

        Cluster client arguments:
           url_file: file containing connection information for accessing cluster
           profile: name of the IPython profile to use
           profile_dir: directory containing the profile's connection information
           ipython_dir: directory containing profile directories
           context: ZMQ context
           debug: whether to issue debugging information (defaults to False)
           sshserver: username and machine for ssh connections
           sshkey: file containing ssh key
           password: ssh password
           paramiko: True to use paramiko for ssh (defaults to False)
           timeout: timeout in seconds for ssh connection (defaults to 10s)
           cluster_id: string added to runtime files to prevent collisions'''
        cncp.Lab.__init__(self, name)
        self._robust = robust
        
        # record all the connection arguments for later
        self._arguments = dict(url_file = url_file,
                               profile = profile,
                               profile_dir = profile_dir,
                               ipython_dir = ipython_dir,
                               context = context,
                               debug = debug,
                               sshserver = sshserver,
                               sshkey = sshkey,
                               password = password,
                               paramiko = paramiko,
                               timeout = timeout,
                               cluster_id = cluster_id,
                               **extra_args)
        self._client = None

        # connect to the cluster
        self.open()
        
        # make us use Dill as pickler by default
        #self.use_dill()

    def open( self ):
        '''Connect to the cluster.'''
        if self._client is None:
            self._client = Client(**self._arguments)
        
    def close( self ):
        '''Close down the connection to the cluster.'''
        if self._client is not None:
            self._client.close()
            self._client = None
        
    def numberOfEngines( self ):
        '''Return the number of engines available to this lab.

        returns: the number of engines'''
        self.open()
        return len(self._client[:])

    def engines( self ):
        '''Return a list of the available engines.

        returns: a list of engines'''
        self.open()
        return self._client[:]

    def use_dill( self ):
        '''Make the cluster use Dill as pickler for transferring results.'''
        with self.sync_imports():
            import dill
        self._client.direct_view().use_dill()

    def sync_imports( self ):
        '''Return a context manager to control imports onto all the engines
        in the underlying cluster. This method is used within a with statement.

        returns: a context manager'''
        self.open()
        return self._client[:].sync_imports()
    
    def _mixup( self, ps ):
        '''Private method to mix up a list of values in-place using a Fisher-Yates
        shuffle (see https://en.wikipedia.org/wiki/Fisher-Yates_shuffle).

        ps: the array
        returns: the array, shuffled in-place'''
        for i in xrange(len(ps) - 1, 0, -1):
            j = int(numpy.random.random() * i)
            temp = ps[i]
            ps[i] = ps[j]
            ps[j] = temp
        return ps
     
    def runExperiment( self, e ):
        '''Run the experiment across the parameter space in parallel using
        all the engines in the cluster. This method returns immediately.
        The experiments are run asynchronously, with the points in the parameter
        space being explored randomly so that intermediate retrievals of results
        are more representative of the overall result. Put another way, for a lot
        of experiments the results available will converge towards a final
        answer, so we can plot them and see the answer emerge.        

        e: the experiment'''
        
        # create the parameter space, randomising so that we evaluate across
        # the space as we go along to make intermediate (incomplete) result
        # sets more representative of the overall result set
        ps = self._mixup(self.parameterSpace())

        # connect to the cluster
        self.open()

        # submit an experiment at each point in the parameter space to the cluster
        view = self._client.load_balanced_view()
        sim = lambda p: e.runExperiment(p)
        jobs = view.map_async(sim, ps)

        # record the mesage ids of all the jobs as submitted but not yet completed
        self._jobs = dict()
        for j in jobs.msg_ids:
            self._jobs[j] = None

        # close our connection to the cluster
        self.close()

    def _updateResults( self ):
        '''Update the jobs record with any newly-completed jobs.

        returns: the number of jobs completed at this call'''

        # sd: this may not be the most efficient way: may be better to
        # work out the ready jobs and then grab them all in one network transaction
        try:
            self.open()
            n = 0
            for j in self._jobs.keys():
                try:
                    if self._client.get_result(j).ready():
                        self._jobs[j] = (self._client.get_result(j).get())[0] # wrangle the list
                                                                              # that gets returned
                                                                              # into a single value
                        n = n + 1
                except Exception as x:
                    if self._robust:
                        # we're running robustly, so elide the exception with
                        # a warning (there seems to sometimes be a race condition
                        # the makes retrieval fail, but succeed later)
                        print "Job id {id} inaccessible, will try again".format(id = j)
                    else:
                        # we're not running robustly, pass on the exception
                        raise x
        finally:
            # whatever happens, close the connection to the cluster 
            self.close()
        return n
                
    def results( self ):
        '''Return all the results we have at present.

        returns: a list of available results'''

        # grab any results that have come in recently
        self._updateResults()

        # collect the results into a list, losing the job ids
        results = []
        for j in [ j for j in self._jobs.keys() if self._jobs[j] is not None ]:
            results.append(self._jobs[j])
        return results

    def _availableResults( self ):
        '''Private method to return the number of results available.
        This does not update the results fetched from the cluster.

        returns: the number of available results'''
        return len([ j for j in self._jobs.keys() if self._jobs[j] is not None ])

    def _availableResultsFraction( self ):
        '''Private method to return the fraction of results available, as a real number
        between 0 and 1. This does not update the results fetched from the cluster.

        returns: the fraction of available results'''
        return ((self._availableResults() + 0.0) / len(self._jobs.keys()))
    
    def readyFraction( self ):
        '''Test what fraction of results are available. This will change over
        time as the results come in.

        returns: the fraction from 0 to 1'''

        # grab any results that have come in recently
        self._updateResults()
        
        # return the fraction
        return self._availableResultsFraction()
    
    def ready( self ):
        '''Test whether all the results are available. This will change over
        time as the results come in.

        returns: True if all the results are available'''
        return (self.readyFraction() == 1)
