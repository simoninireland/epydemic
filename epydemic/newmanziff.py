# The Newman-Ziff algorithm for site (node) and bond (edge) percolation
#
# Copyright (C) 2017--2021 Simon Dobson
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

from epydemic import NetworkExperiment, Node, Edge
from epyc import Experiment, ResultsDict
from networkx import Graph
import numpy
import sys
from typing import Any, Dict, Union, Optional, Iterable, List, cast
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final


class NewmanZiff(NetworkExperiment):
    '''Base class for the Newman-Ziff site and bond percolation algorithm,
    as described in :cite:`Newman and Ziff 2000 <NewmanZiff>`.

    :param g: (optional) the underlying network or generator
    :param samples: (optional) number of samples or list of sample points (defaults to 100)'''

    def __init__(self, g: Graph = None, samples: Union[int, Iterable[float]] = None):
        super().__init__(g)

        # fill in default
        if samples is None:
            samples = 100
        if isinstance(samples, int):
            samples = numpy.linspace(0.0, 1.0, num=samples, endpoint=True)
        self._samples: List[float] = sorted(numpy.unique(list(cast(Iterable[float], samples))))

        # components data structure is initially empty
        self._components: numpy.ndarray = None

    def setUp(self, params : Dict[str, Any]):
        '''Set up the process.

        :param params: the experimental parameters'''
        super().setUp(params)
        self._gcc = 0
        self._ncomponents = 0

    def tearDown(self):
        '''Throw away the components data structure at tear-down.'''
        self._components = None
        super().tearDown()

    def rootOf(self, n : Node) -> Node:
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
            r = self.rootOf(np)

            # update our component record to point to the root
            self._components[n] = r

            # return the root
            return r

    def join(self, c1 : Node, c2 : Node) -> int:
        '''Join two components (as represented by their roots), returning
        the size of the combined component. The root of the combined
        component is c1.

        :param c1: the first component root
        :param c2: the second component root
        :returns: the new component's size'''

        # extract the size of the second componoent
        # sd: this will be a negative number, since that's how sizes are stored
        msize = self._components[c2]

        # join the second component to the first
        self._components[c2] = c1

        # update the size of the first component
        # sd: this adds two negative numbers
        self._components[c1] += msize

        # reduce the number of components by one
        self._ncomponents -= 1

        # return the size of the new component
        # sd: minus the new encoded size at the root
        return -self._components[c1]


    # ---------- Querying the structure ----------

    def components(self) -> int:
        '''Return the number of components in the network.

        :returns: the number of components'''
        return self._ncomponents

    def componentSize(self, n: Node) -> int:
        '''Return the size of the component containing the node.

        :param n: the node
        :returns: the size of the component of which this node is part
        '''
        r = self.rootOf(n)
        return -self._components[r]

    def largestComponentSize(self) -> int:
        '''Return the size of the largest component.

        :returns: the size of largest component'''
        return self._gcc

    def inLargestComponent(self, n: Node) -> bool:
        '''Return True if the given node is part of the largest component.
        Note that this is non-deterministic, in the sense that before
        the percolation threshold there will be more than one "largest"
        cluster (and mightr indeed be several even afterwards): in *a*
        largest cluster might be a better interpretation.

        :param n: the node
        :returns: True if the node is part of the largest component
        '''
        return (self.componentSize(n) == self.largestComponentSize())


    # ---------- Sampling ----------

    def sample(self, p: float) -> Dict[str, Any]:
        '''Take a sample. The default does nothing, and it overridden by
        sub-classes.

        :param p: the current occupation probability
        :returns: an empty dict'''
        return dict()

    def report(self, params: Dict[str, Any], meta: Dict[str, Any], res: List[Dict[str, Any]]) -> ResultsDict:
        '''Re-write the list of samples into two sequences of the percolation value
        and corresponding GCC size. It is assumed that all the samples take the same form,
        i.e., have the same keys.

        :param params: the experimental parameters
        :param meta: the metadata
        :param res: a list of individual sample results
        :returns: a results dicts'''

        # create the series
        series = dict()
        for k in res[0].keys():
            series[k] = []
        for r in res:
            for k in r.keys():
                series[k].append(r[k])

        # wrap the experiment results in a results dict
        rc = self.resultsdict()
        rc[self.PARAMETERS] = params.copy()
        rc[self.METADATA] = meta.copy()
        rc[self.RESULTS] = series
        return rc


class BondPercolation(NewmanZiff):
    '''A bond (edge) percolation experiment. This experiment computes the size of
    the giant connected component (GCC) as edges are "occupied" within the underlying network.
    It samples the GCC at a given sequence of occupation probabilities, returning
    a time series of the growth of the GCC.

    Each occupation of a bond is treated as an event.

    :param g: (optional) the underlying network or generator
    :param samples: (optional) number of samples or list of sample points (defaults to 100)'''

    # Event names
    OCCUPY: Final[str] = 'epydemic.bondpercolation.occupy'   #: Name for bond-occupation event.
    SAMPLE: Final[str] = 'epydemic.bondpercolation.sample'   #: Name for sampling event.

    # Experimental results
    P: Final[str] = 'epydemic.bondpercolation.pOccupied'     #: Result holding series of percolation values.
    GCC: Final[str] = 'epydemic.bondpercolation.gcc'         #: Result holding sizes of largest component.

    def __init__(self, g : Graph = None, samples : Union[int, Iterable[float]] = None):
        super().__init__(g, samples)

    def setUp(self, params : Dict[str, Any]):
        '''Set up the process, creating the initial components data structure from the
        underlying network.

        :param params: the experimental parameters'''
        super().setUp(params)
        N = self.network().order()
        self._components = numpy.full(N, -1, numpy.int32)
        self._gcc = 1           # all nodes are individual components, unconnected by occupied edges
        self._ncomponents = N

    def occupy(self, n : Node, m : Node) -> Optional[int]:
        '''Occupy an edge. If this causes two components to be joined,
        update the GCC and return the size of the new component; otherwise
        return None.

        This method should be overridden to collect more statistics about the network
        as components join.

        :param n: one node
        :param m: the other nodse
        :returns: the size of any newly-combined component, or None'''
        nr = self.rootOf(n)
        mr = self.rootOf(m)
        if mr != nr:
            # nodes are in different components, join them together
            csize = self.join(nr, mr)

            # update the GCC
            self._gcc = max(self._gcc, csize)

            # return the new component size
            return csize
        else:
            # no new component was formed
            return None

    def sample(self, p : float) -> Dict[str, Any]:
        '''Take a sample. The default samples the size of the GCC.

        :param p: the current occupation probability
        :returns: a dict of results'''
        res = super().sample(p)
        res[self.P] = p
        res[self.GCC] = self._gcc
        return res

    def percolate(self, es : List[Edge]) -> List[Dict[str, Any]]:
        '''Perform the bond percolation process. This runs through the
        list of edges, occupying them and taking samples of the occupied
        network's statistics at the requested sample points. The samples
        will be taken as the closest point above the requested probability.
        They will be recorded in the results as actually having been sampled at the
        requested point, however, so that all results are sampled with the same indices.

        :param es: the permuted list of edges
        :returns: a list of dicts of experiment results.'''

        # take an initial sample if requested
        samples = []
        samplePoint = 0
        if self._samples[samplePoint] == 0.0:
            samples.append(self.sample(self._samples[samplePoint]))
            samplePoint += 1

        # percolate the network
        M = len(es)
        for i in range(M):
            (n, m) = es[i]

            # occupy the edge
            self.occupy(n, m)
            self.eventFired(i, self.OCCUPY, (n, m))

            # take a sample if this is a sample point
            if  (i + 1) / M >= self._samples[samplePoint]:
                # we're at the closest probability after the requested sample point,
                # so build the sample
                samples.append(self.sample(self._samples[samplePoint]))
                self.eventFired(i, self.SAMPLE, None)

                # if we've collected all the samples we want, bail out
                samplePoint += 1
                if samplePoint > len(self._samples):
                    break

        return samples

    def do(self, params : Dict[str, Any]) -> List[Dict[str, Any]]:
        '''Perform the percolation process. This passes a permuted
        list of edges to :meth:`NewmanZiff.percolate`, which performs
        the actual operation.

        :param params: experimental parameters
        :returns: a list of dicts of experimental results'''
        # extract and shuffle the edges
        g = self.network()
        es = list(g.edges()).copy()
        numpy.random.shuffle(es)

        # percolate the network using these edges
        self.simulationStarted(params)
        res = self.percolate(es)
        self.simulationEnded(res)
        return res


class SitePercolation(NewmanZiff):
    '''A site (node) percolation experiment. This experiment computes the size of
    the giant connected component (GCC) as nodes are "occupied" within the underlying network.
    It samples the GCC at a given sequence of occupation probabilities, returning
    a time series of the growth of the GCC.

    :param g: (optional) the underlying network or generator
    :param samples: (optional) number of samples or list of sample points (defaults to 100)'''

    # Event names
    OCCUPY: Final[str] = 'epydemic.sitepercolation.occupy'   #: Name for site-occupation event.
    SAMPLE: Final[str] = 'epydemic.sitepercolation.sample'   #: Name for sampling event.

    # Experimental results
    P: Final[str] = 'epydemic.sitepercolation.pOccupied'    #: Result holding sequence of percolation values.
    GCC: Final[str] = 'epydemic.sitepercolation.gcc'        #: Result holding sizes of largest component.

    def __init__(self, g : Graph = None, samples : Union[int, Iterable[float]] = None):
        super().__init__(g, samples)

    def setUp(self, params : Dict[str, Any]):
        '''Set up the process, creating the initial components data structure from the
        underlying network.

        :param params: the experimental parameters'''
        super().setUp(params)
        N = self.network().order()
        self._unoccupied = N + 1                   # a root that can never occur
        self._components = numpy.full(N, self._unoccupied, numpy.int32)
        self._gcc = 0          # initially there are no components
        self._ncomponents = 0

    def componentSize(self, n: Node) -> int:
        '''Return the size of the component containing the node. This will
        be 0 if the node has not been occupied.

        :param n: the node
        :returns: the size of the component of which this node is part
        '''
        if self._components[n] == self._unoccupied:
            return 0
        else:
            return super().componentSize(n)

    def inLargestComponent(self, n: Node) -> bool:
        '''Return True if the given node is occupied and part of the
        largest component.

        :param n: the node
        :returns: True if the node is occupied and part of the largest component
        '''
        if self.componentSize(n) == 0:
            return False
        else:
            return super().inLargestComponent(n)

    def occupy(self, nr : Node) -> int:
        '''Occupy a node, which is then joined to all adjacent occupied nodes.
        This will update the GCC and return the size of the new component.

        This method should be overridden to collect more statistics about the network
        as components join.

        :param nr: the node
        :returns: the size of any newly-combined component'''
        g = self.network()

        # mark the node as a singleton component
        self._components[nr] = -1
        self._ncomponents += 1
        csize = 1

        # connect to all neighbouring occupied nodes
        for m in g.neighbors(nr):
            if self._components[m] != self._unoccupied:
                # neighbour is occupied, join to it
                mr = self.rootOf(m)

                if mr != nr:
                    csize = self.join(nr, mr)

        # update the GCC
        self._gcc = max(self._gcc, csize)

        # return the new component size
        return csize

    def sample(self, p : float) -> Dict[str, Any]:
        '''Take a sample. The default samples the size of the GCC.

        :param p: the current occupation probability
        :returns: a dict of results'''
        res = super().sample(p)
        res[self.P] = p
        res[self.GCC] = self._gcc
        return res

    def percolate(self, ns : List[Node]) -> List[Dict[str, Any]]:
        '''Perform the site percolation process. This runs through the
        list of nodes, occupying them and taking samples of the occupied
        network's statistics at the requested sample points. The samples
        will be taken as the closest point above the requested probability.
        They will be recorded in the results as actually having been sampled at the
        requested point, however, so that all results are sampled with the same indices.

        :param en: the permuted list of nodes
        :returns: a list of dicts of experiment results.'''
        # take an initial sample if requested
        samples = []
        samplePoint = 0
        if self._samples[samplePoint] == 0.0:
            samples.append(self.sample(self._samples[samplePoint]))
            samplePoint += 1

        # percolate the network
        N = len(ns)
        for i in range(N):
            n = ns[i]

            # occupy the edge
            self.occupy(n)
            self.eventFired(i, self.OCCUPY, n)

            # take a sample if this is a sample point
            if  (i + 1) / N >= self._samples[samplePoint]:
                # we're at the closest probability after the requested sample point,
                # so build the sample
                samples.append(self.sample(self._samples[samplePoint]))
                self.eventFired(i, self.SAMPLE, None)

                # if we've collected all the samples we want, bail out
                samplePoint += 1
                if samplePoint > len(self._samples):
                    break

        return samples

    def do(self, params : Dict[str, Any]) -> List[Dict[str, Any]]:
        '''Perform the percolation process. This passes a permuted
        list of nodes to :meth:`NewmanZiff.percolate`, which performs
        the actual operation.

        :param params: experimental parameters
        :returns: a list of dicts of experimental results'''
        # extract and shuffle the nodes
        g = self.network()
        ns = list(g.nodes()).copy()
        numpy.random.shuffle(ns)

        # percolate the network using these nodes
        self.simulationStarted(params)
        res = self.percolate(ns)
        self.simulationEnded(res)
        return res
