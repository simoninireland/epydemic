# Loci for dynamics epidemic model
#
# Copyright (C) 2017--2020 Simon Dobson
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
from networkx import Graph
from typing import Iterator


class Locus():
    '''The locus of dynamics, where changes can happen. Loci
    are filled with nodes or edges from a network and represent some (possibly
    complete) sub-set of the elements, typically being populated and re-populated as
    a process over the network evolves.

    A locus is basically a set with some additional methods to allow
    or more complex behaviours, including customisable drawing random
    selection of elements. The underlying set is implemented as a
    balanced binary tree to ensure scalability, especially of the
    :meth:`draw` method whose performance is critical.

    :param name: the locus name

    '''

    def __init__(self, name: str):
        super().__init__()
        self._name: str = name
        self._root: TreeNode = None
        self._size = 0

    def name(self) -> str:
        '''Returns the name of the locus.

        :returns: the locus' name'''
        return self._name


    # ---------- Basic access ----------

    def add(self, e: Element):
        '''Add an element to the set. This is a no-op if the element is already
        in the set.

        :param e: the element to add'''
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

    def __contains__(self, e: Element) -> bool:
        '''Check whether the given element is a member of the locus.

        :param e: the element
        :returns: True if the element is in the locus'''
        if self._root is None:
            return False
        else:
            return self._root.find(e) is not None

    def empty(self) -> bool:
        '''Test if the locus is empty.

        :returns: True if the locus is empty'''
        return self._root is None

    def __len__(self) -> int:
        '''Return the size of the locus.

        :returns: the size of the locus'''
        return self._size

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
            (present, empty, r) = self._root.discard(e)
            if present:
                self._size -= 1
            if empty:
                # tree has been emptied
                self._root = None
            elif r is not None:
                # the tree was rotated about the root
                self._root = r

    def remove(self, e: Element):
        '''Remove the given element from the locus, raising
        an exception if it wasn't present: use :meth:`discard`
        to allow the removal of non-elements.

        :param e: the element'''
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
        '''Draw an element from the locus at random.

        :returns: a random element, or none if the set is empty'''
        if self._root is None:
            raise ValueError('Drawing from an empty locus')
        else:
            return self._root.draw()


    # ---------- Handlers ----------

    def addHandler(self, g : Graph, e : Element):
        '''Handler called when an element is added to the network. This is used to indicate
        the the population of nodes or edges has changed.

        :param g: the network
        :param e: the element'''
        self.add(e)

    def leaveHandler(self, g : Graph, e : Element):
        '''Handler for when an element leaves the locus due to changes in circumstances,
        not changes in population.

        :param g: the network
        :param e: the element'''
        self.discard(e)

    def enterHandler(self, g : Graph, e : Element):
        '''Handler for when an element enters the locus due to changes in circumstances,
        not changes in population.

        :param g: the network
        :param e: the element'''
        self.add(e)

    def removeHandler(self, g : Graph, e : Element):
        '''Handler called when an element is removed from the network.  This is used to indicate
        the the population of nodes or edges has changed.

        :param g: the network
        :param e: the element'''
        self.discard(e)
