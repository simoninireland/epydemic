# Vaccination model
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
from typing import Dict, Any, List, Final, Tuple, Callable
if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final
from epydemic import Opinion


class Vaccinate(Opinion):
    """
    Vaccination model from paper. Inherits from Opinion model to
    included vaccination process running over network.
    """

    # Experimental parameters
    R_VACC: Final[str] = 'Vaccinate.rVacc'         #: Experimental parameter for rate of vaccination

    # Compartments
    ANTI_VACC: Final[str] = 'antivacc'             #: tracker for antivaccination nodes
    PRO_UN_VACC: Final[str] = 'unvacc_provacc'     #: tracker for unvaccinated nodes pro-vaccination
    VACCED: Final[str] = 'vacced'                  #: vaccinated nodes locus

    def __init__(self):
        super().__init__()

    def build(self, params: Dict[str, Any]):
        """
        Builds vaccination model
        :param params: experimenrtal parameters
        """
        super().build(params)

        self.addLocus(self.ANTI_VACC)
        self.addLocus(self.PRO_UN_VACC)
        self.addLocus(self.VACCED)

        # scales up probability to a rate
        rVacc = params[self.R_VACC] * self.network().number_of_nodes()
        self.addFixedRateEvent(self.PRO_UN_VACC, rVacc, self.vaccinate)

        g = self.network()
        g.set_node_attributes(values=False, name="vacced")
        g.set_node_attributes(values=0, name="t_vacc")

    def vaccinate(self, t: float, n: Node):
        """Performs vaccination event. Updates nodes' :attr:'VACCED' and
        :attr:'T_VACCED' attributes, and adds nodes to :attr:`VACCED` locus and
        removes from PRO_UN_VACC locus.

        :param t: time of vaccination
        :param n: node being vaccinated

        """
        g = self.network()
        g.nodes[n]['vacced'] = True
        g.nodes[n]['t_vacc'] = t
        self.locus(self.PRO_UN_VACC).leaveHandler(self.network(), n)
        self.locus(self.VACCED).addHandler(self.network(), n)


    def changeCompartment(self, n: Node, c: str):
        """
        Overrides opinion.changeCompartment to manually add and remove nodes from PRO_UN_VACC and
        ANTI_VACC compartments.

        :param n: node changing compartment
        :param c: compartment node is changing to
        """

        if c == self.IGNORANT: #if being added to ignorant in inital set up of model.
            self.locus(self.PRO_UN_VACC).addHandler(self.network(), n)
        if c == self.SPREADER: # once affected by antivacc opinion, handles trackers.
            self.locus(self.PRO_UN_VACC).leaveHandler(self.network(), n)
            self.locus(self.ANTI_VACC).addHandler(self.network(), n)

        super().changeCompartment(n, c)
