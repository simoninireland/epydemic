# Synchronous dynamics base class
#
# Copyright (C) 2017 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from epydemic import *

import epyc
import networkx
import numpy
from copy import copy

class CompartmentedSynchronousDynamics(SynchronousDynamics):
    '''A :term:`synchronous dynamics` running a compartmented model. The
    behaviour of the simulation is completely described within the model
    rather than here.'''
        
    def __init__( self, m, g = None ):
        '''Create a dynamicsover the given disease model, optionally
        initialised to run on the given prototype network.
        
        :param m: the model
        :param g: prototype network to run over (optional)'''
        super(CompartmentedSynchronousDynamics, self).__init__(g)
        self._model = m

    def setUp( self, params ):
        '''Set up the experiment for a run. This performs the default action
        of copying the prototype network and then builds the model and
        uses it to initialise the nodes into the various compartments
        according to the parameters.

        :params params: the experimental parameters'''
        
        # perform the default setup
        super(CompartmentedSynchronousDynamics, self).setUp(params)

        # build the model
        self._model.build(params)

        # initialise the network from the model
        g = self.network()
        self._model.setUp(g, params)

    def dynamics( self, t, params ):
        '''Run a single step of the model over the network.
        
        :param t: the current timestep
        :param params: the parameters of the simulation
        :returns: the number of dynamic events that happened in this timestep'''
        g = self.network()
        events = 0
        
        # retrieve all the events, their loci, probabilities, and event functions
        dist = self._model.eventDistribution(t)

        # run through all the events
        for (l, p, f) in dist:
            # run through every possible element on which this event may occur
            for e in copy(l.elements()):
                # test for occurrance of the event on this element
                if numpy.random.random() < p:
                    # yes, perform the event
                    f(t, g, e)

                    # update the event count
                    events = events + 1

        return events

    def experimentalResults( self ):
        '''Report the model's experimental results.

        :returns: the results as seen by the model'''
        return self._model.results(self.network())
