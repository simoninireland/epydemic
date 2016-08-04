# Tests of SIR under stochastic dynamics
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

from cncp import *
from .sir import SIRTests

import epyc
import unittest
import networkx


class SIRStochasticTests(SIRTests):

    def setUp( self ):
        super(SIRStochasticTests, self).setUp()
        self._experiment = SIRStochasticDynamics(self._er)
 
