# Test suite
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import unittest
from .experiments import *
from .labs import *

experimentsSuite = unittest.TestLoader().loadTestsFromTestCase(ExperimentTests)
labsSuite = unittest.TestLoader().loadTestsFromTestCase(LabTests)

suite = unittest.TestSuite([ experimentsSuite, labsSuite ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite)
