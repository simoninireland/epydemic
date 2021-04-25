# Test bitstreams
#
# Copyright (C) 2021 Simon Dobson
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

from epydemic import *
import unittest

class BitstreamTest(unittest.TestCase):

    # ---------- Bitstream tests ----------

    def testBits(self):
        '''Test bitstreams carry on regardless.'''
        bs = Bitstream()
        bss = iter(bs)
        bits = []
        for _ in range(100000):
            bits.append(next(bss))
        ones = len([b for b in bits if b == 1])
        zeros = len([b for b in bits if b == 0])
        self.assertEqual(ones + zeros, len(bits))
        self.assertAlmostEqual(ones, zeros, delta=int(len(bits) * 0.05))
