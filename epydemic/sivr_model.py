# SIR model that incorporates vaccination, reducing infection.
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
from typing import Dict, Any
if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final
from epydemic import SIR, rng, Node, Edge


class SIvR(SIR):
    """Reduced susceptiblility vaccination model

    This model extends :class:`SIR` with a simppe model of vaccination.
    A node may be vaccinated or not. When a vaccinated susceptible node undergoes
    an :meth:`infect` event it only actually becomes infected in
    a proportiion of cases, controlled by the :attr:`EFFICACY` attribute: a
    high vaccine efficacy means that more infections will fail. The
    vaccine onnly becomes effective after an optional time offset
    determined by :attr:`T_OFFSET`: before this time after vaccination,
    vaccinated and unvaccinated individuals behave the same.

    The model maintains two additional loci, containing vaccinated-but-infected-anyway
    individuals (:attr:`INFECTED_V`) and unvaccinated-and-infected individuals
    (:attr:`INFECTED_N`). These do noit affect the dynamics, but make it easy
    to monitor (using :class:`Monitor`) the relative sizes of these classes within
    the infected population.

    The :meth:`vaccinateNode` method is defined to vaccinate a given node. It isn't called
    by any events within this model, but can be called by another process to initiate
    vaccination.
    """

    # Experimental parameters
    EFFICACY: Final[str] = 'epydemic.SIvR.pEfficacy'   #: Experimental parameter for vaccine efficacy.
    T_OFFSET: Final[str] = 'epydemic.SIvR.tOffset'     #: Experimental parameter for delay in applying vaccine.

    # Loci
    INFECTED_N: Final[str] = 'epydemic.SIvR.In'        #: Tracker for infected unvaccinated nodes.
    INFECTED_V: Final[str] = 'epydemic.SIvR.Iv'        #: Tracker for infected vaccinated nodes.

    # Node attributes
    VACCINATED: Final[str] = 'vaccincated'             #: Node attribute storing vaccine status.
    VACCINATION_TIME: Final[str] = 'vaccination_time'  #: Node attribute for vaccination time..


    # ---------- Managing vaccination data ----------

    def vaccinateNode(self, t: float, n: Node):
        '''Vaccinate an individual. This updates the process to
        include the vaccination of the given individual (node).

        :param t: the simulation time
        :param n: the node'''
        g = self.network()

        # we use SIvR.VACCINATED here rather than self.VACCINATED to allow
        # other models to call this method while passing themselves in
        # as self (since they typically won't have a reference to the SIvR
        # process thatt's running in parallel)
        g.nodes[n][SIvR.VACCINATED] = True
        g.nodes[n][SIvR.VACCINATION_TIME] = t

    def nodeVaccinated(self, n: Node) -> bool:
        '''Tests the vaccination status of a node.

        :param n: the node
        :returns: True if the node has been vaccinated'''
        return self.network().nodes[n].get(SIvR.VACCINATED, False)

    def nodeVaccinatedAt(self, n: Node) -> float:
        '''Return the vaccination time of a node. This is defined to be
        -1 -- an illegal simulation time -- if the node has not been vaccinated.

        :param n: the node
        :returns: the vaccination time or -1'''
        return self.network().nodes[n].get(SIvR.VACCINATION_TIME, -1)


    # ---------- Building the model ----------

    def build(self, params: Dict[str, Any]):
        """
        Build the SIvR model. This uses the same paraneters as :class:`SIR`, and adds
        vaccine efficacy (:attr:`EFFICACY`) and (optionally) a time delay (:attr:`T_OFFSET`).

        :param params: experimental parameters
        """
        super().build(params)

        # stash the efficacy
        self._efficacy = params[self.EFFICACY]

        # default to no time offset
        self._offset = params.get(self.T_OFFSET, 0.0)

        # track (un)vaccinated nodes
        self.addLocus(self.INFECTED_N)    # infected but unvaccinated nodes
        self.addLocus(self.INFECTED_V)    # infected and vaccinated nodes

    def setUp(self, params: Dict[str, Any]):
        '''Set up the simulation. All nodes are initially marked
        as unvaccinated.

        :param params: the experimental parameters'''
        super().setUp(params)
        g = self.network()
        for n in g.nodes:
            g.nodes[n][self.VACCINATED] = False


    # ---------- Events ----------

    def infect(self, t: float, e: Edge):
        """Extends :meth:`SIR.infect` with functionality to reduce the
        probability of infection for vaccinated nodes according to
        :attr:`EFFICACY`. The vaccination effect only kicks-in after
        a time :attr:`T_OFFSET` from administration.

        t: the simulation time
        e: the edge transmitting the infection, susceptible->infected
        """
        (n, _) = e
        g = self.network()
        if g.nodes[n][self.VACCINATED] and g.nodes[n][self.VACCINATION_TIME] + self._offset < t:
            # node is vaccinated, test for effect
            if rng.random() > self._efficacy:
                # infect anyway
                self.changeCompartment(n, self.INFECTED)
                self.markOccupied(e, t)

                # log in the infected-despite-vaccinated locus
                self.locus(self.INFECTED_V).enterHandler(g, n)
        else:
            # node is not vaccinated, infect as normal
            self.changeCompartment(n, self.INFECTED)
            self.markOccupied(e, t)

            # log as infected-but-unvaccinated
            self.locus(self.INFECTED_N).enterHandler(g, n)

    def remove(self, t: float, n: Node):
        '''Perform the remove event and also remove from the marker loci.

        :param t: the simulation time (unused)
        :param n: the node'''
        super().remove(t, n)

        # remove from whichever tracker
        g = self.network()
        self.locus(self.INFECTED_V).leaveHandler(g, n)
        self.locus(self.INFECTED_N).leaveHandler(g, n)
