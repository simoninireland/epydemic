# Test suite
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import unittest
#from .ernetworks import *
#from .lattices import *
from .sirsynchronous import SIRSynchronousTests
from .sirstochastic import SIRStochasticTests

#ernetworksSuite = unittest.TestLoader().loadTestsFromTestCase(ERNetworkTests)
sirsynchronousSuite = unittest.TestLoader().loadTestsFromTestCase(SIRSynchronousTests)
sirstochasticSuite = unittest.TestLoader().loadTestsFromTestCase(SIRStochasticTests)

suite = unittest.TestSuite([ sirsynchronousSuite, sirstochasticSuite
                              ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite)
