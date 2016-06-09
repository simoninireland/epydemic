# Base class for experiments
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import time


class Experiment:
    '''Base class for experiments conducted in a lab. An experiment
    consists of four phases: set up, do the experiment, tear down, and
    report. Each of these can be overridden to create suites of experiments.'''

    # Common elements reported
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    ELAPSED_TIME = 'elapsed_time'
    SETUP_TIME = 'setup_time'
    EXPERIMENT_TIME = 'experiment_time'
    TEARDOWN_TIME = 'teardown_time'
    PARAMETERS = 'parameters'
    STATUS = 'status'
    EXCEPTION = 'exception'
    
    def __init__( self ):
        '''Create a new experiment.'''
        self._timings = dict()
        self._parameters = dict()

    def setUp( self ):
        '''Set up the experiment. Default does nothing.'''
        pass

    def tearDown( self ):
        '''Tear down the experiment. Default does nothing.'''
        pass
    
    def do( self, params ):
        '''Do the body of the experiment. This should be overridden
        by sub-classes.

        params: a dict of parameters for the experiment
        returns: a dict of results'''
        raise NotYetImplementedError('do()')

    def report( self, res ):
        '''Return a dict of results. The default adds timing information
        to the dict returned by the do() method. Overriding this method can
        be used to record extra metadata, but be sure to call the base method
        as well.
 
        res: the results of do()
        returns: a dict of extended results'''
        extres = dict(self._timings, **res)
        extres[self.PARAMETERS] = self._parameters
        return extres

    def runExperiment( self, params ):
        '''Run the experiment's set up, do, tear down, and reporting
        phases. Any exceptions taised will be caught and recorded.

        params: dict of the experiment's parameters
        returns: dict of reported results'''

        # record the parameters for reporting
        self._parameters = params

        # perform the experiment protocol
        res = None
        doneSetupTime = doneExperimentTime = doneTeardownTime = 0
        try:
            # do the phases in order, recording the wallclock times at each phase
            startTime = time.clock()
            self.setUp()
            doneSetupTime = time.clock()
            res = self.do(params)
            doneExperimentTime = time.clock() 
            self.tearDown()
            doneTeardownTime = time.clock() 

            # record the various timings
            self._timings[self.START_TIME] = startTime
            self._timings[self.END_TIME] = doneTeardownTime
            self._timings[self.ELAPSED_TIME] = doneTeardownTime - startTime
            self._timings[self.SETUP_TIME] = doneSetupTime - startTime
            self._timings[self.EXPERIMENT_TIME] = doneExperimentTime - doneSetupTime
            self._timings[self.TEARDOWN_TIME] = doneTeardownTime - doneExperimentTime

            # set the success flag
            self._timings[self.STATUS] = True
        except Exception as e:
            # decide on the cleanup actions that need doing
            if (doneSetupTime > 0) and (doneExperimentTime == 0):
                # we did the setup and then failed in the experiment, so
                # we need to do the teardown
                try:
                    self.tearDown()
                except:
                    pass
                
            # set the failure flag and record the exception
            # (there will be no timing information recorded)
            self._timings[self.STATUS] = False
            self._timings[self.EXCEPTION] = e

        # report the results
        if res is None:
            res = dict()
        self._results  = self.report(res)
        return self._results 

    def results( self ):
        '''Return the results of the experiment.

        returns: a dict of results'''
        return self._results
    
    def success( self ):
        '''Test whether the experiment has been run successfully.

        returns: True if the experiment has been run successfully'''
        if self.STATUS in self._timings:
            return self._timings[self.STATUS]
        else:
            return False
    

    
        
    
