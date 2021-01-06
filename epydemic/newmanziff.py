# The Newman-Ziff algorithm for bond (edge) percolation
#
# Copyright (C) 2017--2020 Simon Dobson
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

from epydemic import NetworkExperiment, Node
from epyc import Experiment, ResultsDict
from networkx import Graph
import numpy
import sys
from typing import Any, Dict, Union, Iterable, List, cast
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final


class NewmanZiffPercolation(NetworkExperiment):
    '''A bond percolation experiment that explores all percolation probabilities.
    The algorithm is described by :ref:`Newman and Ziff <NZ00>`.

    This experiment behaves like a repeated experiment, in the sense that the size
    of the largest connected component (GCC) is sampled at a range of occupation
    probabilities in a single sweep, with each sample getting its own entry
    as an experimental result. The sample point appears as a parameter to the
    corresponding experiment.
    
    :param g: (optional) the underlying network or generator
    :param samples: (optional) number of samples or list of sample points (defaults to 100)'''

    # Synthesised parameters
    P : Final[str] = 'epydemic.newmanziffpercolation.pOccupied'    #: Parameter holding percolation threshold.

    # Experimental results
    GCC : Final[str] = 'epydemic.newmanziffpercolation.gcc'        #: Result holding size of GCC.

    def __init__(self, g : Graph =None, samples : Union[int, Iterable[float]] =None):
        super(NewmanZiffPercolation, self).__init__(g)

        # fill in default
        if samples is None:
            samples = 100
        if isinstance(samples, int):
            samples = numpy.linspace(0.0, 1.0, num=samples, endpoint=True)

        # save arguments
        self._components : numpy.ndarray = None
        self._samples : List[float] = sorted(numpy.unique(list(cast(Iterable[float], samples))))


    # ---------- The experiment ----------

    def setUp(self, params : Dict[str, Any]):
        '''Set up the process, creating the initial components data structure from the
        underlying network.

        :param params: the experimental parameters'''
        super(NewmanZiffPercolation, self).setUp(params)
        N = self.network().order()
        self._components = numpy.full(N, -1, numpy.int32)

    def tearDown(self):
        '''Throw away the components data structure at tear-down.'''
        self._components = None
        super(NewmanZiffPercolation, self).tearDown()

    def _rootOf(self, n : Node) -> Node:
        '''Return the root of the component containing node n, updating
        the tree accordingly.

        :param n: the node in the component
        :returns: the root of the component'''
        np = self._components[n]
        if np < 0:
            # n is the root, return it
            return n
        else:
            # n has a parent, follow the tree to it
            r = self._rootOf(np)

            # update our component record to point to the root
            self._components[n] = r

            # return the root
            return r

    def do(self, params : Dict[str, Any]) -> List[Dict[str, Any]]:
        '''Perform the bond percolation process.

        :param params: experimental parameters
        :returns: a list of dicts of experimental results'''

        # extract and shuffle the edges
        g = self.network()
        es = list(g.edges()).copy()
        numpy.random.shuffle(es)
        M = len(es)

        # percolate the network
        gcc = -1
        samples = []
        samplePoint = 0
        if self._samples[samplePoint] == 0.0:
            # an initial sample at p=0.0 implies a unit gcc
            res = dict()
            res[self.P] = 0.0
            res[self.GCC] = -gcc
            samples.append(res)
            samplePoint += 1
        for i in range(M):
            (n, m) = es[i]
            nr = self._rootOf(n)
            mr = self._rootOf(m)
            if mr != nr:
                # nodes are in different components
                msize = self._components[mr]
                self._components[mr] = nr
                self._components[nr] += msize
                gcc = min(gcc, self._components[nr])

            # take a sample if this is a sample point
            if  (i + 1) / M >= self._samples[samplePoint]:
                # we're at the closest probability after the requested sample point,
                # so build the sample
                res = dict()
                res[self.P] = self._samples[samplePoint]
                res[self.GCC] = -gcc                        # gcc holds 0 - (size of GCC)
                samples.append(res)

                # if we've collected all the samples we want, bail out
                samplePoint += 1
                if samplePoint > len(self._samples):
                    break

        return samples

    def report(self, params : Dict[str, Any], meta : Dict[str, Any], res : List[Dict[str, Any]]) -> List[ResultsDict]:
        '''Re-write the list of results into a list of individual experiments by
        wrapping them up as results dicts.

        :param params: the experimental parameters
        :param meta: the metadata
        :param res: a list of individual sample results
        :returns: a list of results dicts'''
        rcs = []
        for r in res:
            # wrap the experiment results in their own results dict
            rc = self.resultsdict()
            rc[self.PARAMETERS] = params.copy()
            rc[self.METADATA] = meta.copy()
            rc[self.RESULTS] = r.copy()

            # move the sample point probability from being a result to being a parameter 
            rc[self.PARAMETERS][self.P] = r[self.P]
            del rc[self.RESULTS][self.P]

            rcs.append(rc)
        return rcs
