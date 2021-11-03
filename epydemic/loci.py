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

from epydemic import Element, DrawSet, Process
from networkx import Graph
from typing import Iterator


class Locus(DrawSet):
    '''The locus of dynamics, where changes can happen. Loci
    are filled with nodes or edges from a network and represent some (possibly
    complete) sub-set of the elements, typically being populated and re-populated as
    a process over the network evolves.

    A locus is basically a set with some additional methods to allow
    or more complex behaviours, including customisable drawing random
    selection of elements. The underlying set is implemented as a
    :class:`DrawSet` to ensure scalability, especially of the
    :meth:`draw` method whose performance is critical.

    :param name: the locus name

    '''

    def __init__(self, name: str):
        super().__init__()
        self._name: str = name
        self._process: Process = None

    def name(self) -> str:
        '''Returns the name of the locus.

        :returns: the locus' name'''
        return self._name

    def setProcess(self, p: Process):
        '''Associate the locus with the given process.

        :param p: the process'''
        self._process = p

    def process(self) -> Process:
        '''Return the process this locus is associated with.

        :returns: the process'''
        return self._process


    # ---------- Handlers ----------

    def addHandler(self, g: Graph, e: Element):
        '''Handler called when an element is added to the network. This is used to indicate
        the the population of nodes or edges has changed.

        :param g: the network
        :param e: the element'''
        self.add(e)

    def leaveHandler(self, g: Graph, e: Element):
        '''Handler for when an element leaves the locus due to changes in circumstances,
        not changes in population.

        :param g: the network
        :param e: the element'''
        self.discard(e)

    def enterHandler(self, g: Graph, e: Element):
        '''Handler for when an element enters the locus due to changes in circumstances,
        not changes in population.

        :param g: the network
        :param e: the element'''
        self.add(e)

    def removeHandler(self, g: Graph, e: Element):
        '''Handler called when an element is removed from the network.  This is used to indicate
        the the population of nodes or edges has changed.

        :param g: the network
        :param e: the element'''
        self.discard(e)
