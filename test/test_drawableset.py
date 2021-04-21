# Test bitstreams and drawable sets
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
import numpy
import unittest

class DrawableSetTest(unittest.TestCase):

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

    def testInteger(self):
        '''Test we can get random integers with the given bit-length.'''
        bs = Bitstream()

        # test zero length
        ns = []
        for _ in range(10000):
            ns.append(bs.integer(0))
        self.assertTrue(len([n for n in ns if n == 0]), len(ns))

        # test singleton length
        ns = []
        for _ in range(10000):
            ns.append(bs.integer(1))
        self.assertTrue(len([n for n in ns if n <= 1]), len(ns))

        # test bytes
        ns = []
        for _ in range(10000):
            ns.append(bs.integer(8))
        self.assertTrue(len([n for n in ns if n < 2**8]), len(ns))

        # test larger numbers
        ns = []
        for _ in range(10000):
            ns.append(bs.integer(128))
        self.assertTrue(len([n for n in ns if n < 2**128 - 1]), len(ns))

        # test arbitrary length
        ns = []
        for _ in range(10):
            ns.append(bs.integer(3))
        self.assertTrue(len([n for n in ns if n < 2**3 - 1]), len(ns))

    def testEmptySet(self):
        '''Test empty sets.'''
        s = DrawableSet()
        self.assertEqual(len(s), 0)
        self.assertFalse(1 in s)
        self.assertCountEqual(s, [])

    def testAdd(self):
        '''Test we can add individual elements.'''
        s = DrawableSet()
        s.add(1)
        self.assertEqual(len(s), 1)
        self.assertTrue(1 in s)
        s.add(2)
        self.assertEqual(len(s), 2)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertCountEqual(s.elements(), [1,2])
        self.assertCountEqual(s, [1, 2])

    def testDiscard(self):
        '''Test we can discard elements that are present.'''
        s = DrawableSet()
        s.add(1)
        s.add(2)
        s.discard(1)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])

    def testRepeateAdd(self):
        '''Test we can add the same element twice.'''
        s = DrawableSet()
        s.add(1)
        s.add(2)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.add(2)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.add(1)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])

    def testNonDiscard(self):
        '''Test we can discard when the element isn't there.'''
        s = DrawableSet()
        s.add(1)
        s.add(2)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.discard(3)
        print(list(s.elements()))
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.discard(1)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])
        s.discard(2)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(s, [])

    def testRepeatedDiscard(self):
        '''Test repeated doiscarding.'''
        s = DrawableSet()
        s.add(1)
        s.add(2)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.discard(1)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])
        s.discard(1)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])

    def testLotsOfAdds(self):
        '''Test we can add loads of elements, and get the results in order.'''
        s = DrawableSet()
        es = list(range(10))
        rs = es.copy()
        numpy.random.shuffle(es)
        for i in rs:
            s.add(i)
        self.assertEqual(len(s), len(rs))
        self.assertCountEqual(rs, s.elements())

    def testAddDeleteInOrder(self):
        '''Test we can handle an maximally inbalanced tree.'''
        s = DrawableSet()
        es = list(range(10))
        for i in es:
            s.add(i)
        self.assertEqual(len(s), len(es))
        for i in es:
            s.discard(i)
        self.assertEqual(len(s), 0)

    def testAddDeleteInReverseOrder(self):
        '''Test we can handle an maximally inbalanced tree the other way.'''
        s = DrawableSet()
        es = list(range(10))
        es.reverse()
        for i in es:
            s.add(i)
        self.assertEqual(len(s), len(es))
        for i in es:
            s.discard(i)
        self.assertEqual(len(s), 0)

    def testAddDelete(self):
        '''Test we can add in random order and then delete in order.'''
        s = DrawableSet()
        es = list(range(10))
        rs = es.copy()
        numpy.random.shuffle(es)
        for i in rs:
            s.add(i)
        l = len(s)
        for j in es:
            s.discard(j)
            l -= 1
            self.assertEqual(len(s), l)
        self.assertEqual(len(s), 0)

    def testGrow(self):
        '''Test the height calculation when adding.'''
        s = DrawableSet()
        self.assertEqual(s._height, 0)
        s.add(10)
        self.assertEqual(s._height, 0)
        s.add(20)
        self.assertEqual(s._height, 1)
        s.add(5)
        self.assertEqual(s._height, 1)
        s.add(25)
        self.assertEqual(s._height, 2)
        s.add(30)
        self.assertEqual(s._height, 3)

    def testDiscardDetail(self):
        '''Test that discarding follows the algorithm.'''
        s = DrawableSet()
        s.add(10)
        s.add(20)
        s.add(5)
        s.add(25)
        s.add(30)

        self.assertEqual(s._data, 10)
        self.assertEqual(s._height, 3)
        self.assertEqual(s._leftSize, 1)
        self.assertEqual(s._rightSize, 3)

        self.assertEqual(s._left._data, 5)
        self.assertEqual(s._left._height, 0)
        self.assertIsNone(s._left._left)
        self.assertIsNone(s._left._right)
        self.assertEqual(s._left._leftSize, 0)
        self.assertEqual(s._left._rightSize, 0)

        self.assertEqual(s._right._data, 20)
        self.assertEqual(s._right._height, 2)
        self.assertIsNone(s._right._left)
        self.assertEqual(s._right._leftSize, 0)
        self.assertEqual(s._right._rightSize, 2)

        self.assertEqual(s._right._right._data, 25)
        self.assertEqual(s._right._right._height, 1)
        self.assertIsNone(s._right._right._left)
        self.assertEqual(s._right._right._leftSize, 0)
        self.assertEqual(s._right._right._rightSize, 1)

        self.assertEqual(s._right._right._right._data, 30)
        self.assertEqual(s._right._right._right._height, 0)
        self.assertIsNone(s._right._right._right._left)
        self.assertIsNone(s._right._right._right._right)
        self.assertEqual(s._right._right._right._leftSize, 0)
        self.assertEqual(s._right._right._right._rightSize, 0)

        s.discard(10)

        self.assertEqual(s._data, 20)
        self.assertEqual(s._height, 2)
        self.assertEqual(s._leftSize, 1)
        self.assertEqual(s._rightSize, 2)

        self.assertEqual(s._left._data, 5)
        self.assertEqual(s._left._height, 0)
        self.assertIsNone(s._left._left)
        self.assertIsNone(s._left._right)
        self.assertEqual(s._left._leftSize, 0)
        self.assertEqual(s._left._rightSize, 0)

        self.assertEqual(s._right._data, 25)
        self.assertEqual(s._right._height, 1)
        self.assertIsNone(s._right._left)
        self.assertEqual(s._right._leftSize, 0)
        self.assertEqual(s._right._rightSize, 1)

        self.assertEqual(s._right._right._data, 30)
        self.assertEqual(s._right._right._height, 0)
        self.assertIsNone(s._right._right._left)
        self.assertIsNone(s._right._right._right)
        self.assertEqual(s._right._right._leftSize, 0)
        self.assertEqual(s._right._right._rightSize, 0)

        s.discard(25)

        self.assertEqual(s._data, 20)
        self.assertEqual(s._height, 1)
        self.assertEqual(s._leftSize, 1)
        self.assertEqual(s._rightSize, 1)

        self.assertEqual(s._left._data, 5)
        self.assertEqual(s._left._height, 0)
        self.assertIsNone(s._left._left)
        self.assertIsNone(s._left._right)
        self.assertEqual(s._left._leftSize, 0)
        self.assertEqual(s._left._rightSize, 0)

        self.assertEqual(s._right._data, 30)
        self.assertEqual(s._right._height, 0)
        self.assertIsNone(s._right._left)
        self.assertIsNone(s._right._right)
        self.assertEqual(s._right._leftSize, 0)
        self.assertEqual(s._right._rightSize, 0)

        s.discard(5)

        self.assertEqual(s._data, 20)
        self.assertEqual(s._height, 1)
        self.assertIsNone(s._left)
        self.assertEqual(s._leftSize, 0)
        self.assertEqual(s._rightSize, 1)

        self.assertEqual(s._right._data, 30)
        self.assertEqual(s._right._height, 0)
        self.assertIsNone(s._right._left)
        self.assertIsNone(s._right._right)
        self.assertEqual(s._right._leftSize, 0)
        self.assertEqual(s._right._rightSize, 0)

    def testShrink(self):
        '''Test the height calculation when discarding.'''
        s = DrawableSet()
        s.add(10)
        s.add(20)
        s.add(5)
        s.add(25)
        s.add(30)
        self.assertEqual(s._height, 3)
        s.discard(30)
        self.assertEqual(s._height, 2)
        s.discard(10)
        self.assertEqual(s._height, 1)

    def testDraw(self):
        '''Test the basic draw functionality.'''
        s = DrawableSet()
        es = list(range(1000))
        s.union(es)
        for _ in range(int(len(es) * 0.1)):
            j = s.draw()
            self.assertIn(j, s)

    def testDrawAll(self):
        '''Test we always draw all elements.'''
        s = DrawableSet()
        es = list(range(1000))
        s.union(es)
        ns = []
        for _ in range(len(es)):
            n = s.draw()
            ns.append(n)
            s.discard(n)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(es, ns)
