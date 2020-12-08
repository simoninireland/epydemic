# SIRS as a compartmented model
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

from epydemic import SIR
import sys
if sys.version_info >= (3, 7):
    from typing import Final, Dict, Any
else:
    # backport compatibility with older typing
    from typing import Dict, Any
    from typing_extensions import Final


class SIRS(SIR):
    '''The Susceptible-Infected-Removed-Susceptible :term:`compartmented model of disease`.
    Susceptible nodes are infected by infected neighbours, and recover to removed where
    they remain for a time before returning to susceptible models the situation in which
    disease exposure confers partial immunity in time, rather than full immunity
    (as for :class:`SIR`) or no immunity ( as for :class:`SIS`).'''

    # Extra model parameter
    P_RESUSCEPT : Final[str] = 'epydemic.SIRS.pResuscept'    #: Parameter for probability of losing immunity

    def __init__(self):
        super(SIRS, self).__init__()

    def build(self, params : Dict[str, Any]):
        '''Build the SIRS model.

        :param params: the model parameters'''
        super(SIRS, self).build(params)

        # add components needed for SIRS
        pResuscept = params[self.P_RESUSCEPT]
        self.trackNodesInCompartment(self.REMOVED)

        self.addEventPerElement(self.REMOVED, pResuscept, self.resuscept)

    def resuscept(self, t : float, n : Any):
        '''Perform a re-susceptibility event. This changes the compartment of
        the node from :attr:`REMOVED` to :attr:`SUSCEPTIBLE`.

        :param t: the simulation time (unused)
        :param n: the node'''
        self.changeCompartment(n, self.SUSCEPTIBLE)



