# SIRS as a compartmented model
#
# Copyright (C) 2017--18 Simon Dobson
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


class SIRS(SIR):
    '''The Susceptible-Infected-Removed-Susceptible :term:`compartmented model of disease`.
    Susceptible nodes are infected by infected neighbours, and recover to removed where
    they remain for a time before returning to susceptible models the situation in which
    disease exposure confers partial immunity in time, rather than full (SIR) or no (SIS)
    immunity.'''

    # the extra model parameter
    P_RESUSCEPT = 'pResuscept' #: Parameter for probability of losing immunity

    def __init__(self):
        super(SIRS, self).__init__()

    def build(self, params):
        '''Build the SIRS model.

        :param params: the model parameters'''

        # build SIR
        super(SIRS, self).build(params)

        # add components needed for SIRS
        pResuscept = params[self.P_RESUSCEPT]
        self.trackNodesInCompartment(self.REMOVED)

        self.addEvent(self.REMOVED, pResuscept, self.resuscept)

    def resuscept(self, dyn, t, g, n):
        '''Perform a re-susceptibility event. This changes the compartment of
        the node from :attr:`REMOVED` to :attr:`SUSCEPTIBLE`.

        :param dyn: the dynamics
        :param t: the simulation time (unused)
        :param g: the network
        :param n: the node'''
        self.changeCompartment(g, n, self.SUSCEPTIBLE)



