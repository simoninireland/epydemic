# Test basic loci functions
#
# Copyright (C) 2017--2021 Simon Dobson
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


class LociTest(unittest.TestCase):

    def testName(self):
        '''Test name retrieval.'''
        l = Locus('test')
        self.assertEqual(l.name(), 'test')

    def testAdd(self):
        '''Test we can add elements.'''
        l = Locus('test')
        self.assertEqual(len(l), 0)
        l.add(1)
        self.assertEqual(len(l), 1)
        l.add(2)
        self.assertEqual(len(l), 2)

    def testDelete(self):
        '''Test we can remove elements.'''
        l = Locus('test')
        l.add(1)
        l.add(2)
        l.discard(1)
        self.assertEqual(len(l), 1)
        l.discard(2)
        self.assertEqual(len(l), 0)

    def testDrawEmpty(self):
        '''Test we can't draw from an empty locus.'''
        l = Locus('test')
        with self.assertRaises(ValueError):
            l.draw()

    def testDraw(self):
        '''Test the basic draw functionality.'''
        l = Locus('test')
        es = list(range(100))
        for i in es:
            l.add(i)
        j = l.draw()
        self.assertIn(j, l)

    def testDrawOne(self):
        '''Test we can draw an element without changing the locus.'''
        l = Locus('test')
        l.addHandler(None, 1)
        l.addHandler(None, 2)
        self.assertEqual(len(l), 2)
        self.assertCountEqual(l, [1, 2])

        # duplicate entries are ignored
        l.addHandler(None, 2)
        self.assertCountEqual(l, [1, 2])

        # drawing leaves the population unchanged
        e = l.draw()
        self.assertIn(e, [1, 2])
        self.assertCountEqual(l, [1, 2])


if __name__ == '__main__':
    unittest.main()
