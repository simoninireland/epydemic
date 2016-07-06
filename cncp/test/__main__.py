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
from .clusterlabs import *
from .notebooks import *

experimentsSuite = unittest.TestLoader().loadTestsFromTestCase(ExperimentTests)
labsSuite = unittest.TestLoader().loadTestsFromTestCase(LabTests)
clusterlabsSuite = unittest.TestLoader().loadTestsFromTestCase(ClusterLabTests)
notebooksSuite = unittest.TestLoader().loadTestsFromTestCase(NotebookTests)

suite = unittest.TestSuite([ experimentsSuite, labsSuite, clusterlabsSuite, notebooksSuite ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite)
