# Helper types
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

from typing import Union, Tuple, Any

# the parts of a network (graph)
Node = Any                   #: A node in a network, which may be any object.
Edge = Tuple[Node, Node]     #: An edge in a network, connecting exactly two nodes (which may be the same).
Element = Union[Node, Edge]  #: An element in a simulation, either a node or an edge.


