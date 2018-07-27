# Test suite
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

import unittest
from .test_networkdynamics import NetworkDynamicsTest
from .test_compartmentedmodel import CompartmentedModelTest
from .test_sir import SIRTest
from .test_sis import SISTest
from .test_fixed_recovery import FixedRecoveryTest

ndsuite = unittest.TestLoader().loadTestsFromTestCase(NetworkDynamicsTest)
cmsuite = unittest.TestLoader().loadTestsFromTestCase(CompartmentedModelTest)
sirsuite = unittest.TestLoader().loadTestsFromTestCase(SIRTest)
sissuite = unittest.TestLoader().loadTestsFromTestCase(SISTest)
fixedsuite = unittest.TestLoader().loadTestsFromTestCase(FixedRecoveryTest)

suite = unittest.TestSuite([ ndsuite,
                             cmsuite,
                             sirsuite,
                             sissuite,
                             fixedsuite,
                            ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite)
