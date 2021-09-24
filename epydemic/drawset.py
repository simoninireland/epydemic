# A set with an efficient random draw, wrapping a balanced binary tree
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

from epydemic import Element, TreeNode
from typing import Iterator


class DrawSet():
    '''A set re-implementation.

    This class provides a re-implementation of sets that also provides
    an efficient (:math:`O(\log N)`) method for drawing an element at random.

    We implement only those parts of the set API that we need: perhaps
    ought to add the rest, for future-proofing.

    :param including: (optional) iterator of elements to add
    :param excluding: (optional) elements to exclude from the initialisation
    '''

    def __init__(self, including: Iterator[Element] = None, excluding: Iterator[Element] = None):
        self._root = None

        # if we have an initial value, add all elements from the iterator
        if including is not None:
            os = set(including)

            # exclude any excluded elements
            if excluding is not None:
                es = set(excluding)
                os.difference_update(es)

            for e in os:
                self.add(e)

    def add(self, e: Element):
        '''Add an element to the set. This is a no-op if the element is already
        in the set.

        :param e: the element to add'''
        if self._root is None:
            # we're the root, store here
            self._root = TreeNode(e)
        else:
            (added, r) = self._root.add(e)
            if r is not None:
                # the tree was rotated about the root
                self._root = r

    def __contains__(self, e: Element) -> bool:
        '''Check whether the given element is a member of the set.

        :param e: the element
        :returns: True if the element is in the set'''
        if self._root is None:
            return False
        else:
            return self._root.find(e) is not None

    def empty(self) -> bool:
        '''Test if the set is empty.

        :returns: True if the set is empty'''
        return self._root is None

    def __len__(self) -> int:
        '''Return the size of the set.

        :returns: the size of the set'''
        return len(self._root) if self._root is not None else 0

    def __iter__(self) -> Iterator[Element]:
        '''Return an iterator that returns elements in order.

        :returns: an iterator'''
        if self._root is None:
            return iter([])
        else:
            return iter(self._root)

    def discard(self, e: Element):
        '''Discard the given element from the locus. If the element
        isn't in the set, this is a no-op: use :meth:`remove`
        to detect removal of non-elements.

        :param e: the element'''
        if self._root is not None:
            (_, empty, r) = self._root.discard(e)
            if empty:
                # tree has been emptied
                self._root = None
            elif r is not None:
                # the tree was rotated about the root
                self._root = r

    def remove(self, e: Element):
        '''Remove the given element from the set, raising
        an exception if it wasn't present: use :meth:`discard`
        to allow the removal of non-elements.

        :param e: the element'''
        if self._root is None:
            raise KeyError(e)
        else:
            (present, empty, r) = self._root.discard(e)
            if not present:
                raise KeyError(e)
            if empty:
                # tree has been emptied
                self._root = None
            elif r is not None:
                # the tree was rotated about the root
                self._root = r

    def draw(self) -> Element:
        '''Draw an element from the set at random.

        :returns: a random element, or none if the set is empty'''
        if self._root is None:
            raise ValueError('Drawing from an empty set')
        else:
            return self._root.draw()
