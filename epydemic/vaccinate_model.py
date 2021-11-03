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
from typing import Dict, Any
if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final
from epydemic import Opinion, SIvR, Node


class Vaccinate(Opinion):
    """An opinion model where the opinion is pro- or anti-vaccination, and
    nodes that are pro-vaccination are vaccinated at a certain rate.

    Internally, the opinion being spread is anti-vaccination. Those who have
    been affected by the opinion (spreaders) will refuse vaccination; those
    who have either not heard the opinion or have changed their opinion (ignorants
    and stiflers) will be vaccinated at a given rate.

    The actual vacciination functionality is provided as an event by :class:`SIvR`.
    Tnis class simply provides the mechanism whereby vaccination events happen.
    """

    # Experimental parameters
    P_VACCINATE: Final[str] = 'epydemic.vaccinate.pVaccinate'  #: Experimental parameter for rate of vaccination.

    def build(self, params: Dict[str, Any]):
        """Builds vaccination model. This extends the :class:`Opinion` parameters
        with a vaccination rate :attr:`P_VACCINATE`.

        :param params: experimenrtal parameters
        """
        super().build(params)

        # add vaccination events for ignorant and stifler individuals
        self.addPerElementEvent(self.IGNORANT, params[self.P_VACCINATE], self.vaccinate)
        self.addPerElementEvent(self.STIFLER, params[self.P_VACCINATE], self.vaccinate)

    def vaccinate(self, t: float, n: Node):
        '''Perform the vaccination operation. The actual functionality is
        outsourced to :meth:`SIvR.vaccinateNode`.

        :param t: the simulation time
        :param n: the node'''
        SIvR.vaccinateNode(self, t, n)
