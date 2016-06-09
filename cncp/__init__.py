# Initialisation for "Complex networks, complex processes" package
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

# regular networks
from .lattice import lattice_graph, draw_lattice
from .ernetworks import erdos_renyi_graph_from_scratch

# networks with dynamical processes
from .networkwithdynamics import GraphWithDynamics
from .synchronousdynamics import GraphWithSynchronousDynamics
from .stochasticdynamics import GraphWithStochasticDynamics

# SIR processes under different dynamics
from .sirsynchronousdynamics import SIRSynchronousDynamics
from .sirstochasticdynamics import SIRStochasticDynamics

# experiment management
from .experiment import Experiment
from .lab import Lab

