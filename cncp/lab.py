# Simulation "lab" experiment management, sequential version
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import cncp


class Lab:
    '''A laboratory for computational experiments. The lab conducts an
    experiment at different points in a multi-dimensional parameter space.
    The default performs all the experiments locally; sub-classes exist
    to perform remote parallel experiments.'''

    def __init__( self, name = None ):
        '''Create an empty lab.
 
        name: an identifier for this lab, only used for documentation'''
        self._name = name
        self._parameters = dict()
        self._results = None

    def name( self ):
        '''Return the lab's name.

        returns: the lab name'''
        return self._name
    
    def addParameter( self, k, r ):
        '''Add a parameter to the experiment's parameter space. k is the
        parameter name, and r is its range.

        k: parameter name
        r: parameter range'''
        self._parameters[k] = r

    def parameters( self ):
        '''Return a list of parameter names.

        returns: a list of names'''
        return self._parameters.keys()

    def __len__( self ):
        '''The length of an experiment is the total number of data points
        that will be explored. 

        returns: the length of the experiment'''
        n = 1
        for p in self.parameters():
            n = n * len(self._parameters[p])
        return n
        
    def __getitem__( self, k ):
        '''Access a parameter range using array notation.

        k: parameter name
        returns: the parameter range'''
        return self._parameters[k]

    def __setitem__( self, k, r ):
        '''Add a parameter using array notation.

        k: the parameter name
        r: the parameter range'''
        return self.addParameter(k, r)

    def _crossProduct( self, ls ):
        '''Internal metod to generate the cross product of all parameter
        values, creating the parameter space for the experiment.

        ls: an array of parameter names
        returns: list of dicts'''
        p = ls[0]
        ds = []
        if len(ls) == 1:
            # last parameter, convert range to a dict
            for i in self._parameters[p]:
                dp = dict()
                dp[p] = i
                ds.append(dp)
        else:
            # for other parameters, create a dict combining each value in
            # the range to a copy of the dict of other parameters
            ps = self._crossProduct(ls[1:])
            for i in self._parameters[p]:
                for d in ps:
                    dp = d.copy()
                    dp[p] = i
                    ds.append(dp)

        # return the complete parameter space
        return ds
           
    def parameterSpace( self ):
        '''Return the parameter space of the experiment as a list of dicts,
        with each dict mapping each parameter name to a value.

        returns: the parameter space as a list of dicts'''
        ps = self.parameters()
        if len(ps) == 0:
            return []
        else:
            return self._crossProduct(ps)
    
    def runExperiment( self, e ):
        '''Run an experiment over all the points in the parameter space.

        e: the experiment'''

        # create the parameter space
        ps = self.parameterSpace()

        # run the experiment at each point
        self._results = []
        for p in ps:
            res = e.runExperiment(p)
            self._results.append(res)

    def results( self ):
        '''Retrieve the list of result dicts (each of which contains the
        point at which the experiment was evaluated to get this
        result).

        returns: a list of experimental results'''
        return self._results
    
    def ready( self ):
        '''Test whether all the results are ready. For this sequential
        implementation all results are either ready or not.

        returns: Trus if the results are in'''
        return (self.results() is not None)
        
    
