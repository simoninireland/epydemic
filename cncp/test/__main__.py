# Test suite
#
# Copyright (C) 2014-2016 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Noncommercial-Share
# Alike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
#

import unittest
from .experiments import *

experimentsSuite = unittest.TestLoader().loadTestsFromTestCase(ExperimentTests)

suite = unittest.TestSuite([ experimentsSuite ])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite)
