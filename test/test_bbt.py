# Test balanced binary trees and their DrawSet wrapper
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
import statistics
import numpy
import unittest


class BBTTest(unittest.TestCase):

    def assertInvariant(self, s):
        '''Test the invariant of tree is satisfied.'''
        if s._root is not None:
            self.assertAVLInvariant(s._root)

    def assertAVLInvariant(self, n):
        lh = n._left._height + 1 if n._left is not None else 0
        rh = n._right._height + 1 if n._right is not None else 0
        self.assertTrue(abs(lh - rh) <= 1)
        self.assertEqual(n._height, max(lh, rh))
        if lh > 0:
            self.assertIsNotNone(n._left)
            self.assertAVLInvariant(n._left)
        if rh > 0:
            self.assertIsNotNone(n._right)
            self.assertAVLInvariant(n._right)

    def testEmptySet(self):
        '''Test empty sets.'''
        s = DrawSet()
        self.assertInvariant(s)
        self.assertEqual(len(s), 0)
        self.assertFalse(1 in s)
        self.assertCountEqual(s, [])
        self.assertTrue(s.empty())

    def testAdd(self):
        '''Test we can add individual elements.'''
        s = DrawSet()
        self.assertTrue(s.empty())
        s.add(1)
        self.assertFalse(s.empty())
        self.assertInvariant(s)
        self.assertEqual(len(s), 1)
        self.assertTrue(1 in s)
        s.add(2)
        self.assertInvariant(s)
        self.assertEqual(len(s), 2)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertCountEqual(list(s), [1,2])
        s.add(3)
        self.assertInvariant(s)
        self.assertEqual(len(s), 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)
        self.assertCountEqual(list(s), [1, 2, 3])

    def testABCroot(self):
        '''Test the ABC rotation over the root.'''
        s = DrawSet()
        s.add(0)
        s.add(1)
        s.add(2)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [0, 1, 2])
        self.assertEqual(s._root._data, 1)

    def testABC(self):
        '''Test the ABC rotation below the root.'''
        s = DrawSet()
        s.add(1)
        s.add(0)
        s.add(2)
        s.add(3)
        s.add(4)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [0, 1, 2, 3, 4])
        self.assertEqual(s._root._data, 1)

    def testACBroot(self):
        '''Test the ACB rotation overt the root.'''
        s = DrawSet()
        s.add(1)
        s.add(3)
        s.add(2)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [1, 2, 3])
        self.assertEqual(s._root._data, 2)

    def testACB(self):
        '''Test the ACB rotation below the root.'''
        s = DrawSet()
        s.add(3)
        s.add(0)
        s.add(5)
        s.add(7)
        s.add(6)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [0, 3, 5, 6, 7])
        self.assertEqual(s._root._data, 3)

    def testCBAroot(self):
        '''Test the CBA rotation across the root.'''
        s = DrawSet()
        s.add(3)
        s.add(2)
        s.add(1)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [1, 2, 3])
        self.assertEqual(s._root._data, 2)

    def testCBA(self):
        '''Test the CBA rotation below the root.'''
        s = DrawSet()
        s.add(5)
        s.add(7)
        s.add(3)
        s.add(2)
        s.add(1)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [1, 2, 3, 5, 7])
        self.assertEqual(s._root._data, 5)

    def testCABroot(self):
        '''Test the CABB rotation across the root.'''
        s = DrawSet()
        s.add(4)
        s.add(2)
        s.add(3)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [2, 3, 4])
        self.assertEqual(s._root._data, 3)

    def testCAB(self):
        '''Test the CAB rotation below the root.'''
        s = DrawSet()
        s.add(2)
        s.add(1)
        s.add(8)
        s.add(5)
        s.add(6)
        self.assertInvariant(s)
        self.assertCountEqual(list(s), [1, 2, 5, 6, 8])
        self.assertEqual(s._root._data, 2)

    def testDiscard(self):
        '''Test we can discard elements that are present.'''
        s = DrawSet()
        s.add(2)
        s.add(3)
        s.discard(3)
        self.assertInvariant(s)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])

    def testDiscardEmpty(self):
        '''Test we can discard from an empty set.'''
        s = DrawSet()
        s.discard(1)
        self.assertInvariant(s)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(s, [])

    def testRemoveSuccess(self):
        '''Test successful removal.'''
        s = DrawSet()
        s.add(1)
        s.add(2)
        s.remove(2)
        self.assertInvariant(s)

    def testRemoveFailure(self):
        '''Test failing removal of a non-element.'''
        s = DrawSet()
        s.add(1)
        s.add(2)
        with self.assertRaises(KeyError):
            s.remove(3)

    def testRemoveEmpty(self):
        '''Test removal; from an empty set.'''
        s = DrawSet()
        with self.assertRaises(KeyError):
            s.remove(3)

    def testDiscardToEmpty(self):
        '''Test we can discard the last element in the set.'''
        s = DrawSet()
        s.add(1)
        s.discard(1)
        self.assertInvariant(s)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(s, [])
        self.assertTrue(s.empty())

    def testRemoveToEmpty(self):
        '''Test we can removethe last element in the set.'''
        s = DrawSet()
        s.add(1)
        s.remove(1)
        self.assertInvariant(s)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(s, [])
        self.assertTrue(s.empty())

    def testDiscardLeaves(self):
        '''Test we can discard leaf elements.'''
        s = DrawSet()
        s.add(2)
        s.add(3)
        s.discard(3)
        self.assertInvariant(s)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])
        s.add(1)
        s.discard(1)
        self.assertInvariant(s)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])
        s.discard(2)
        self.assertInvariant(s)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(s, [])

    def testDiscardSingleSubtree(self):
        '''Test we can discard nodes with a single sub-tree.'''
        s = DrawSet()
        s.add(2)
        s.add(3)
        s.add(4)
        s.add(5)
        s.discard(4)
        self.assertInvariant(s)
        self.assertEqual(len(s), 3)
        self.assertCountEqual(s, [2, 3, 5])
        s.add(1)
        s.discard(2)
        self.assertInvariant(s)
        self.assertEqual(len(s), 3)
        self.assertCountEqual(s, [1, 3, 5])

    def testDiscardTwoSubtrees(self):
        '''Test we can discard a node with two sub-trees.'''
        s = DrawSet()
        s.add(3)
        s.add(2)
        s.add(10)
        s.add(7)
        s.add(15)
        s.add(6)
        s.discard(10)
        self.assertInvariant(s)
        self.assertEqual(len(s), 5)
        self.assertCountEqual(s, [2, 3, 6, 7, 15])

    def testRepeatedAdd(self):
        '''Test we can add the same element twice.'''
        s = DrawSet()
        s.add(1)
        self.assertInvariant(s)
        s.add(2)
        self.assertInvariant(s)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.add(2)
        self.assertInvariant(s)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.add(1)
        self.assertInvariant(s)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])

    def testNonDiscard(self):
        '''Test we can discard when the element isn't there.'''
        s = DrawSet()
        s.add(1)
        s.add(2)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.discard(3)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.discard(1)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])
        s.discard(2)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(s, [])

    def testRepeatedDiscard(self):
        '''Test repeated discarding.'''
        s = DrawSet()
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

    def testRepeatedRemove(self):
        '''Test repeated removing.'''
        s = DrawSet()
        s.add(1)
        s.add(2)
        self.assertEqual(len(s), 2)
        self.assertCountEqual(s, [1, 2])
        s.remove(1)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])
        with self.assertRaises(KeyError):
            s.remove(1)

    def testLotsOfAdds(self):
        '''Test we can add loads of elements, and get the results in order.'''
        s = DrawSet()
        es = list(range(200))
        rs = es.copy()
        numpy.random.shuffle(es)
        for i in es:
            s.add(i)
            self.assertInvariant(s)
        self.assertEqual(len(s), len(rs))
        self.assertCountEqual(rs, list(s))

    def testAddRemoveInOrder(self):
        '''Test we can handle an maximally inbalanced tree.'''
        s = DrawSet()
        es = list(range(20))
        for i in es:
            s.add(i)
            self.assertInvariant(s)
        self.assertEqual(len(s), len(es))
        for i in es:
            s.remove(i)
            self.assertInvariant(s)
        self.assertEqual(len(s), 0)

    def testAddRemoveInReverseOrder(self):
        '''Test we can handle an maximally inbalanced tree the other way.'''
        s = DrawSet()
        es = list(range(100))
        es.reverse()
        for i in es:
            s.add(i)
            self.assertInvariant(s)
        self.assertEqual(len(s), len(es))
        for i in es:
            s.remove(i)
            self.assertInvariant(s)
        self.assertEqual(len(s), 0)

    def testAddRemove(self):
        '''Test we can add in random order and then remove in order.'''
        s = DrawSet()
        es = list(range(100))
        rs = es.copy()
        numpy.random.shuffle(rs)
        for i in rs:
            s.add(i)
            self.assertInvariant(s)
        l = len(s)
        for j in es:
            s.remove(j)
            self.assertInvariant(s)
            l -= 1
            self.assertEqual(len(s), l)
        self.assertEqual(len(s), 0)

    def testDraw(self):
        '''Test the basic draw functionality.'''
        s = DrawSet()
        es = list(range(1000))
        numpy.random.shuffle(es)
        for e in es:
            s.add(e)
        for _ in range(int(len(es) * 0.1)):
            j = s.draw()
            self.assertIn(j, s)

    def testDrawAll(self):
        '''Test we always draw all elements.'''
        s = DrawSet()
        es = list(range(1000))
        numpy.random.shuffle(es)
        for e in es:
            s.add(e)
        ns = []
        for _ in range(len(es)):
            n = s.draw()
            self.assertIsNotNone(n)
            self.assertNotIn(n, ns)
            ns.append(n)
            s.remove(n)
            self.assertInvariant(s)
            self.assertNotIn(n, s)
        self.assertEqual(len(s), 0)
        self.assertCountEqual(es, ns)

    def testInitial(self):
        '''Test adding an initial value from an iterator.'''
        l = [1, 2, 3, 4, 5]
        s = DrawSet(l)
        self.assertEqual(len(l), len(s))
        self.assertCountEqual(l, s)


if __name__ == '__main__':
    unittest.main()
