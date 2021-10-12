# SIvR model that incorporates vaccination
#
# Copyright (C) 2021 Liberty Askew
# Integrated into main codebase by Simon Dobson
#
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published byf
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

import sys
import random
from networkx import Graph
from typing import Dict, Any, List, Tuple, Callable
if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final
from epydemic import SIR


class SIvR(epydemic.SIR):
    """Reduced susceptiblility SIvR model from paper.

    Inherits from epydemic.SIR and based on this class
    structure. Monitor features have been integrated into the class.

    """

    INFECTED_N : Final[str] = 'SIvR.In'            #: Tracker for infected unvaccinated nodes.
    INFECTED_V : Final[str] = 'SIvR.Iv'            #: Tracker for infected vaccinated nodes.

    def __init__(self, effic = 0.8, offset = 0):

        super().__init__()
        self.effic = effic                          #efficacy of the vaccine.
        self.offset = offset                        # if there is an offset start of vaccination cycle when run from dynamic.
        self._finalNetwork : Graph = None           #stores final network as class attribute for analysis.

    def build(self, params):
        """
        Builds the SIvR model.
        params: dictionary
            params[epydemic.SIR.P_INFECTED]
            params[epydemic.SIR.P_INFECT]
            params[epydemic.SIR.P_REMOVE]
        """

        super(SIvR, self).build(params)

        self.addLocus(self.INFECTED_N) # adds locus to track infected unvaccinated nodes.
        self.addLocus(self.INFECTED_V) # adds locus to track infected vaccinated nodes.

        self.trackNodesInCompartment(epydemic.SIR.SUSCEPTIBLE) # monitors simulation for results
        self.trackNodesInCompartment(epydemic.SIR.REMOVED) # monitors simulation for results


    def infect(self, t, e):
        """
        Overrides epydemic.SIR.infect to perform an infection event. This method has additional
        functionality of reducing probability of infection for vaccinated nodes according to
        self.efficacy. Also checks node vaccination time with offset to see if it vaccinated at
        time t -  used when combined in dynamic model.

        t: the simulation time
        e: the edge transmitting the infection, susceptible-infected
        """
        (n, o) = e
        if (self.network().nodes[n]['vacced'] == True) & (self.network().nodes[n]['t_vacc'] + self.offset < t) : #when combined with dynamic model need to check time vaccinated with offset.
            if random.random() > self.effic: #implements efficacy of the vaccine.
                self.changeCompartment(n, self.INFECTED, True)
                self.markOccupied(e, t)
        else:
            self.changeCompartment(n, self.INFECTED, False)
            self.markOccupied(e, t)

    def changeCompartment(self, n, c, v = False):
        """
        Change the compartment of a node. Overrides epydemic.SIR.changeCompartment because handles
        manually adding and removing nodes from INFECTED_V and INFECTED_N locus.
        n: the node
        c: the new compartment for the node
        """
        g = self.network()
        oc = g.nodes[n][self.COMPARTMENT] #old compartment of node.
        if oc is not None:
            self._callLeaveHandlers(n, oc)
        g.nodes[n][self.COMPARTMENT] = c
        self._callEnterHandlers(n, c)
        if c == 'epydemic.SIR.I': # if being infected.
            if v:
                self.locus(self.INFECTED_V).addHandler(self.network(),n)
            if not v:
                self.locus(self.INFECTED_N).addHandler(self.network(),n)
        if oc == 'epydemic.SIR.I': # if recovering.
            if self.locus(self.INFECTED_V).__contains__(n):
                self.locus(self.INFECTED_V).leaveHandler(self.network(),n)
            if self.locus(self.INFECTED_N).__contains__(n):
                self.locus(self.INFECTED_N).leaveHandler(self.network(),n)


    def results(self):
        """
        Grabs final results of network and stores the final network as class attribute _finalNetwork
        for analysis.
        returns: results dictionary
        """
        res = super().results()
        self._finalNetwork = self.network().copy()
        return res
