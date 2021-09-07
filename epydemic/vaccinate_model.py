# author: Liberty Askew
# last modified: 17/08/2021

import sys
import random
import epydemic
import numpy as np
import networkx as nx
from opinion import Opinion

if sys.version_info >= (3, 8):
    from typing import Dict, Any, List, Final, Tuple, Callable
else:
    from typing import Dict, Any, List, Tuple, Callable
    from typing_extensions import Final

"""
Vaccination model from paper. Inherits from Opinion model to included vaccination process running
over network.
"""
class Vaccinate(Opinion):

    R_VACC : Final[str] = 'Vaccinate.rVacc'         #: rate of vaccination

    ANTI_VACC : Final[str] = 'antivacc'             #: tracker for antivaccination nodes
    PRO_UN_VACC : Final[str] = 'unvacc_provacc'     #: tracker for unvaccinated nodes pro-vaccination
    VACCED : Final[str] = 'vacced'                  #: vaccinated nodes locus

    def __init__(self):

        super().__init__()

    def build(self, params):
        """
        Buils vaccination model
        params: dictionary
            params['Opinion.pAffected']
            params['Opinion.pAffect']
            params['Opinion.pStifle']
            params['Vaccinate.rVacc']
        """

        rVacc = params[self.R_VACC] * self.network().number_of_nodes() #scales up rate of vaccination for number of nodes in network.
        self.addLocus(self.ANTI_VACC)
        self.addLocus(self.PRO_UN_VACC)
        self.addLocus(self.VACCED)

        self.addFixedRateEvent(self.PRO_UN_VACC, rVacc, self.vaccinate) # vaccination occurs at fixed rate to unvaccinate & provaccination nodes.

        nx.set_node_attributes(self.network(), values = False, name="vacced")
        nx.set_node_attributes(self.network(), values = 0, name="t_vacc") # used when combined with SIvR in dynamic model to check vaccination status between models at time t.

        super(Vaccinate, self).build(params)


    def vaccinate(self, t, n ):
        """
        Performs vaccination event. Updated nodes 'vacced' and 't_vacced' attributes. Adds nodes to
        VACCED locus and removes from PRO_UN_VACC locus.
        t: time of vaccination
        n: node being vaccinated
        """

        self.network().nodes[n]['vacced'] = True
        self.network().nodes[n]['t_vacc'] = t
        self.locus(self.PRO_UN_VACC).leaveHandler(self.network(),n)
        self.locus(self.VACCED).addHandler(self.network(),n)


    def changeCompartment(self, n, c):
        """
        Overrides opinion.changeCompartment to manually add and remove nodes from PRO_UN_VACC and
        ANTI_VACC compartments.
        n: node changing compartment
        c: compartment node is changing to
        """

        if c == self.IGNORANT: #if being added to ignorant in inital set up of model.
            self.locus(self.PRO_UN_VACC).addHandler(self.network(),n)
        if c == self.SPREADER: # once affected by antivacc opinion, handles trackers.
            self.locus(self.PRO_UN_VACC).leaveHandler(self.network(),n)
            self.locus(self.ANTI_VACC).addHandler(self.network(),n)

        super(Vaccinate, self).changeCompartment(n, c)


    def results(self):
        """
        Grabs final results of network and stores the final network as class attribute _finalNetwork
        for analysis.
        returns: results dictionary
        """
        res = super().results()
        self._finalNetwork = self.network().copy()
        return res
