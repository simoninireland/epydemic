# Test balanced binary trees
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


class BBTHelper(object):
    '''Set wrapper to make testign easier.'''

    def __init__(self):
        self._root = None

    def __len__(self):
        if self._root is None:
            return 0
        else:
            return len(self._root)

    def __iter__(self):
        return iter(self.elements())

    def elements(self):
        if self._root is None:
            return []
        else:
            return self._root.inOrderTraverse()

    def add(self, e):
        if self._root is None:
            # we're the root, store here
            self._root = TreeNode(e)
            self._size = 1
        else:
            (added, r) = self._root.add(e)
            if added:
                self._size += 1
            if r is not None:
                # the tree was rotated about the root
                self._root = r

    def __contains__(self, e  ) -> bool:
        if self._root is None:
            return False
        else:
            return self._root.find(e) is not None

    def empty(self) -> bool:
        return self._root is None

    def discard(self, e  ):
        if self._root is not None:
            (present, empty, r) = self._root.discard(e)
            if present:
                self._size -= 1
            if empty:
                # tree has been emptied
                self._root = None
            elif r is not None:
                # the tree was rotated about the root
                self._root = r

    def remove(self, e):
        if self._root is None:
            raise KeyError(e)
        else:
            (present, empty, r) = self._root.discard(e)
            if present:
                self._size -= 1
            else:
                raise KeyError(e)
            if empty:
                # tree has been emptied
                self._root = None
            elif r is not None:
                # the tree was rotated about the root
                self._root = r

    def draw(self) -> Element:
        if self._root is None:
            raise ValueError('Drawing from an empty locus')
        else:
            return self._root.draw()


class BBTTest(unittest.TestCase):

    def testEmptySet(self):
        '''Test empty sets.'''
        s = BBTHelper()
        self.assertEqual(len(s), 0)
        self.assertFalse(1 in s)
        self.assertCountEqual(s, [])

    def testAdd(self):
        '''Test we can add individual elements.'''
        s = BBTHelper()
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
        s = BBTHelper()
        s.add(1)
        s.add(2)
        s.discard(1)
        self.assertEqual(len(s), 1)
        self.assertCountEqual(s, [2])

    def testRepeateAdd(self):
        '''Test we can add the same element twice.'''
        s = BBTHelper()
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
        s = BBTHelper()
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
        '''Test repeated doiscarding.'''
        s = BBTHelper()
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
        s = BBTHelper()
        es = list(range(1000))
        rs = es.copy()
        numpy.random.shuffle(es)
        for i in rs:
            s.add(i)
        self.assertEqual(len(s), len(rs))
        self.assertCountEqual(rs, s.elements())

    def testAddDeleteInOrder(self):
        '''Test we can handle an maximally inbalanced tree.'''
        s = BBTHelper()
        es = list(range(1000))
        for i in es:
            s.add(i)
        self.assertEqual(len(s), len(es))
        for i in es:
            s.discard(i)
        self.assertEqual(len(s), 0)

    def testAddDeleteInReverseOrder(self):
        '''Test we can handle an maximally inbalanced tree the other way.'''
        s = BBTHelper()
        es = list(range(1000))
        es.reverse()
        for i in es:
            s.add(i)
        self.assertEqual(len(s), len(es))
        for i in es:
            s.discard(i)
        self.assertEqual(len(s), 0)

    def testAddDelete(self):
        '''Test we can add in random order and then delete in order.'''
        s = BBTHelper()
        es = list(range(100))
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

    def testDraw(self):
        '''Test the basic draw functionality.'''
        s = BBTHelper()
        es = list(range(100))
        for i in es:
            s.add(i)
        j = s.draw()
        self.assertIn(j, s)
