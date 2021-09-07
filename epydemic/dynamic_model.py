# author: Liberty Askew
# last modified: 17/08/2021

import epydemic
import random
import copy
import sys
from sivr import SIvR
from vaccinate import Vaccinate
import networkx as nx
import numpy as np

if sys.version_info >= (3, 8):
    from typing import Dict, Any, List, Final, Tuple, Callable
else:
    # backport compatibility with older typing
    from typing import Dict, Any, List, Tuple, Callable
    from typing_extensions import Final


class Dynamic():
    """
    Model combining SIvR and Vaccination models. When class is called, initiates running SIvR then
    opinion model. Stores results and graph as attributes.

    V_params: dict of parameters for Vaccinate model
        V_params[epydemic.PLCNetwork.N]
        V_params[epydemic.PLCNetwork.EXPONENT]
        V_params[epydemic.PLCNetwork.CUTOFF]
        V_params['Opinion.pAffected']
        V_params['Opinion.pAffect']
        V_params['Opinion.pStifle']
        V_params['Vaccinate.rVacc']

    S_params: dict of parameters for SIvR model
        S_params[epydemic.SIR.P_INFECTED]
        S_params[epydemic.SIR.P_INFECT]
        S_params[epydemic.SIR.P_REMOVE]
    """

    def __init__(self, V_params, S_params, delta=10, max_time=1000, effic=0.8, offset=0):

        super().__init__()

        # resultant network after vaccination and opinions run and rewired.
        self._vaccNetwork: Graph = None
        # resultant network after SIvR run on vaccNetwork.
        self._finalNetwork: Graph = None
        # results dictionary from both monitored vaccination and SIvR model.
        self._results: Dict = None

        self.delta = delta                          # time interval for results observations
        self.max_time = max_time                    # maximum time for simulation
        self.effic = effic                          # efficacy of vaccine.
        # probability of rejoining nodes for second network.
        self.reset = 0.5
        # time difference btween start of vaccination and SIvR model.
        self.offset = int(offset / self.delta)
        # number of observations there should be.
        self.obs_no = (self.max_time / self.delta) + 1

        self.run_VacModel(V_params)
        self.run_SIvR(S_params)

    def run_VacModel(self, V_params):
        """
        Runs Vaccinate model on PLCNetwork and passes V_params. Resets the network from vaccination model
        and stores it as _vaccNetwork
        V_params: parameters for vaccination model
        """
        m = Vaccinate()
        V_params[epydemic.Monitor.DELTA] = self.delta
        p = epydemic.ProcessSequence([m, epydemic.Monitor()])
        e = epydemic.StochasticDynamics(p, epydemic.PLCNetwork())
        e.process().setMaximumTime(self.max_time)
        rc = e.set(V_params).run()
        self._results = rc
        if (len(rc['results']['epydemic.monitor.observations']) != self.obs_no):
            self.fit(rc['results'])
        # still shift if 0 because scale up list length if short.
        if(self.offset > 0):
            self.shift(rc['results'])
        self._vaccNetwork = self.resetGraph(m._finalNetwork)


    def run_SIvR(self, S_params):
        """
        Runs SIvR model on _vaccNetwork and passes S_params. Stores results dict as _results and
        final network as _finalNetwork.
        S_params: parameters for SIvR model.
        """
        m = SIvR(offset=self.offset, effic=self.effic)
        S_params[epydemic.Monitor.DELTA] = self.delta
        p = epydemic.ProcessSequence([m, epydemic.Monitor()])
        e = epydemic.StochasticDynamics(p, self._vaccNetwork)
        e.process().setMaximumTime(self.max_time)
        rc = e.set(S_params).run()
        # only store 'parameters' and 'results'.
        self._results['parameters'].update(rc['parameters'])
        # if terminated early or late will trim results so all uniform.
        if (len(rc['results']['epydemic.monitor.observations']) != self.obs_no):
            self.fit(rc['results'])
        if(self.offset < 0):
            self.shift(rc['results'])
        rc['results']['epydemic.monitor.observations'] = np.arange(
            0, (self.obs_no) * self.delta, self.delta)  # hard code incase falls short
        self._results['results'].update(rc['results'])
        self._finalNetwork = m._finalNetwork


    def fit(self, results):
        """
        Adjusts resutls lists to be exact number of observations expected if too short / long. Lenght of
        observations not always uniform due to epydemic's stochastic process. Needs to be uniform in dynamic
        model so the sets of results can be joined.
        """
        offset = abs(self.offset)
        for k in results.keys():
            if 'epydemic.monitor.timeseries' in k:
                l = results[k]
                if len(l) < self.obs_no:  # terminated early
                    l = l + [l[-1]] * int(self.obs_no - len(l))
                # sometimes longer due to 'how events are drawn' in epydemic.
                elif len(l) > self.obs_no:
                    l = l[:int(self.obs_no)]
                results.update({k: l})


    def shift(self, results):
        """
        Applys time delay shift to results. Sorted according to negative / positive before reaching method.
        Returns none.
        results: results dictionary to be shifted by self.offset.
        """
        offset = abs(self.offset)
        for k in results.keys():
            if 'epydemic.monitor.timeseries' in k:
                l = results[k]
                if offset >= len(l):
                    l = [l[0]] * len(l)
                if len(l) > offset:
                    l = [l[0]] * offset + l[:(-offset)]
                results.update({k: l})


    def resetGraph(self, graph):
        """
        Resets graph after Vaccinate model is run, before SIvR model. Randomly reconnects edges with
        default probability 0.5. Clears occupied edges and stores compartment as 'opinion' attribute so
        not overwritten by SIvR.
        graph: graph to be reset.
        returns: reset graph.
        """
        N = len(graph.nodes())
        # needs to be copy because when iterating to arearranging edges, change the iteration
        g = copy.deepcopy(graph)
        # add 'opinion' attribute to each node.
        nx.set_node_attributes(g, values=False, name="opinion")
        rm = []  # list of nodes to remove at end
        ad = []  # list of nodes to add at end
        f = 0
        for n in g.nodes():
            # to store opinion after SIvaR assignment
            g.nodes[n]['opinion'] = g.nodes[n]['compartment']

        for (p, q, data) in g.edges(data=True):  # can't connect edge to same node on each end)
            if random.random() > 0.5:
                if (p, q) in rm:
                    continue
                # random to reduce posisblity of duplicates in ad
                L = random.sample(range(p + 1, N), (N - p - 1))
                for c in L:
                    if (g.degree(c) == g.degree(p)) & (c != q):
                        ed = list(g.edges(c))
                        random.shuffle(ed)
                        (C, D) = ed[0]
                        (c, d) = (min(C, D), max(C, D))
                        i = 1
                        while ((d == p) or ((c, d) in rm)) and i < len(ed):
                            (C, D) = ed[i]
                            (c, d) = (min(C, D), max(C, D))
                            i += 1
                        if i == len(ed):
                            break  # if cannot find a suitable edge from c
                        data2 = g.get_edge_data(c, d)
                        rm.append((c, d))
                        rm.append((p, q))
                        ad.append((p, d, data))
                        ad.append((c, q, data2))
                        break

        g.remove_edges_from(rm)
        g.add_edges_from(ad)

        for (n, m, data) in g.edges(data=True):
            # reset occupied status for next model.
            data[epydemic.SIR.OCCUPIED] = False

        return g
