# Initialisation for epydemic
#
# Copyright (C) 2017 Simon Dobson
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

'''`epydemic` is a library for performing simulations for a range of
epidemic spreeading (and other) processes, simulated over networks
represented using `networkx`.

Epidemic processes are very important in both network science and its
applications. The most common application is to study the was in which
diseases progress in different network conditions, depending on their
infectiousness and other properties. Typically such processes are
modelled as a :term:`compartmented model of disease` (familiar to
computer scientists as finite state machines) with conditional
probabilities for moving between compartments.

`epydemic` provides the basic simulation machinery for performing
epidemic simulations under two different simulation regimes:
synchronous :term:`discrete time` simulation in which time proceeds in
discrete time intervals, and stochastic or Gillespuie :term:`continuous
time` simulations which are better for handling a wider range of
:term:`event` probabilities (but which are slightly harder to
specify).

'''
 
# networks with dynamical processes
from .networkdynamics import Dynamics
#from .synchronousdynamics import SynchronousDynamics
from .stochasticdynamics import StochasticDynamics

# SIR processes under different dynamics
#from .sirsynchronousdynamics import SIRSynchronousDynamics
#from .sirstochasticdynamics import SIRStochasticDynamics

# SIS processes under different dynamics
#from .sissynchronousdynamics import SISSynchronousDynamics
#from .sisstochasticdynamics import SISStochasticDynamics

# new compartmented models
from .compartmentedmodel import CompartmentedModel
from .sir_model import SIR
from .compartmentedstochasticdynamics import CompartmentedStochasticDynamics
