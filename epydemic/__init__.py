# Initialisation for epydemic
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

'''`epydemic` is a library for performing simulations for a range of
epidemic spreading (and other) processes, simulated over networks
represented using `networkx`.

Epidemic processes are very important in both network science and its
applications. The most common application is to study the was in which
diseases progress in different network conditions, depending on their
infectiousness and other properties. Typically such processes are
modelled as a :term:`compartmented model of disease` with conditional
probabilities for moving between compartments (familiar to
computer scientists as stochastic finite state machines).

`epydemic` provides the basic simulation machinery for performing
epidemic simulations under two different simulation regimes:
synchronous :term:`discrete time` simulation in which time proceeds in
discrete time intervals, and stochastic or Gillespie :term:`continuous
time` simulations which are better for handling a wider range of
:term:`event` probabilities (but which are slightly harder to
specify).

`epydemic` also provides processes not directly connected with epidemic modelling
but which are often used alongside disease models. This includes
support for add/delete networks and percolation processes, as well as
support for studying the percolation transition in networks. Individual
network processes can be combined in different ways to encourage good
software engineering practices.
'''

# helper types
from .types import Node, Edge, Element
from .bitstream import Bitstream
from .drawableset import DrawableSet

# network processes
from .loci import Locus
from .process import Process, EventFunction, EventDistribution

# network generators
from .generator import NetworkGenerator
from .standard_generators import FixedNetwork, ERNetwork, BANetwork
from .plc_generator import PLCNetwork

# networks with dynamical processes
from .networkexperiment import NetworkExperiment
from .networkdynamics import Dynamics
from .synchronousdynamics import SynchronousDynamics
from .stochasticdynamics import StochasticDynamics

# compartmented models
from .compartmentedmodel import CompartmentedModel, CompartmentedLocus, CompartmentedNodeLocus, CompartmentedEdgeLocus

# reference disease models
from .sir_model import SIR
from .sis_model import SIS
from .sirs_model import SIRS
from .seir_model import SEIR

# variant disease models
from .sir_model_fixed_recovery import SIR_FixedRecovery
from .sis_model_fixed_recovery import SIS_FixedRecovery

# other processes
from .adddelete import AddDelete
from .percolate import Percolate
from .monitor import Monitor
from .statistics import NetworkStatistics

# process combinators
from .processsequence import ProcessSequence

# other experiments
from .newmanziff import BondPercolation, SitePercolation
