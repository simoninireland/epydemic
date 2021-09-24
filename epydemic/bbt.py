2# An AVL tree with random draw
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

from numpy.random import default_rng
from epydemic import Bitstream, Element
from typing import List, Tuple, Iterator, Optional


class TreeNode():
    '''A node in an AVL tree. This is used within :class:`DrawSet`
    to maintain the contents of a set in a way that can perform a
    random fair draw of its contents.

    :param d: the data at the tree node
    :param p: (optional) the parent node (defaults to None)

    '''

    # Random number generator shared by all instances
    rng = default_rng()


    def __init__(self, d: Element, p: Optional['TreeNode'] = None):
        self._left: Optional['TreeNode'] = None    # left sub-tree
        self._right: Optional['TreeNode'] = None   # right sub-tree
        self._parent: Optional['TreeNode'] = p     # parent nodes
        self._data: Element = d                    # value at this node
        self._height: int = 0                      # height of the tree
        self._leftSize: int = 0                    # left sub-tree size
        self._rightSize: int = 0                   # right sub-tree size

    def __len__(self) -> int:
        '''Return the size of the tree. This is a local operation
        as the left and right sub-tree sizes are maintained locally.

        :returns: the size of the tree'''
        return self._leftSize + 1 + self._rightSize

    def add(self, e: Element) -> Tuple[bool, Optional['TreeNode']]:
        '''Add an element to the tree.

        This method performs two tasks. It adds the element, testing
        whether it was in fact added or was a repetition; and it
        potentially replaces the overall tree root.

        :returns: a pair (wasadded, newroot)'''
        if e == self._data:
            return (False, None)
        elif e < self._data:
            if self._left is None:
                self._left = TreeNode(e, self)
                self._updateHeights()
                return (True, self._left._rebalance())
            else:
                return self._left.add(e)
        else:
            if self._right is None:
                self._right = TreeNode(e, self)
                self._updateHeights()
                return (True, self._right._rebalance())
            else:
                return self._right.add(e)

    def _updateHeights(self):
        '''Walk back to the root updating the heights and sizes of nodes.'''
        n = self
        while n is not None:
            n._updateHeightAndSizes()
            assert(n._parent != n)
            n = n._parent

    def _updateHeightAndSizes(self):
        '''Update the node height and its left and right sizes.'''

        # heights
        lh = self._left._height + 1 if self._left is not None else 0
        rh = self._right._height + 1 if self._right is not None else 0
        self._height = max(lh, rh)

        # sizes
        self._leftSize = len(self._left) if self._left is not None else 0
        self._rightSize = len(self._right) if self._right is not None else 0

    def isUnbalanced(self) -> bool:
        '''Test whether the node is unbalanced, defined as its
        sub-tree heights differing by more than one.

        :returns: True if the node is unbalanced'''
        lh = self._left._height + 1 if self._left is not None else 0
        rh = self._right._height + 1 if self._right is not None else 0
        return abs(lh - rh) > 1

    def _findUnbalanced(self) -> Optional['TreeNode']:
        '''Walk back up the tree looking for the shallowest unbalanced
        node.

        :returns: the shallowest unbalanced node, or None if the tree is completely balanced'''
        if self.isUnbalanced():
            return self
        elif self._parent is None:
            return None
        else:
            return self._parent._findUnbalanced()

    def _tallerSubtree(self) -> 'TreeNode':
        '''Return the taller of the node's sub-trees.

        :returns: the smaller sub-tree'''
        lh = self._left._height + 1 if self._left is not None else 0
        rh = self._right._height + 1 if self._right is not None else 0
        if lh > rh:
            return self._left
        else:
            return self._right

    def _rebalance(self, recursive: bool = False) -> Optional['TreeNode']:
        '''Re-balance the tree after addition or deletion of a node. If the
        re-balancing is recursive (which is needed after deletions,
        but not after additions) then the re-balancing proceeds up the
        tree to the root.

        :param recursive: (optional) True to recursively re-balance (defaults to False)
        :returns: the new overall root, or None if the root hasn't been changed

        '''

        # find the shallowest unbalanced node
        z = self._findUnbalanced()
        if z is None:
            # tree is balanced all the way up
            return None
        else:
            # tree is unbalanced, rotate and find the (local) root
            root = z._rotate()

            if root._parent is None:
                # we have a new global root
                return root
            elif recursive:
                # call again on the parent
                return root._parent._rebalance(True)
            else:
                # root is unchanged
                return None

    def _rotate(z) -> Optional['TreeNode']:
        '''Perform a single rotation to re-balance the node.

        :returns: the new overall root, or None if the root hasn't been changed

        '''

        # we use z instead of the more usual self as the name for
        # the node on which the method is called, to match the
        # normal usage when describing AVL operations for which
        # z is always the root node of the rotation.

        # find the two other nodes for the rotation
        y = z._tallerSubtree()
        x = y._tallerSubtree()

        # grab the parent to which we'll re-attach the new root
        # after rotation
        parent = z._parent

        # perform the appropriate rotation
        # we disconbnect the root node from the rest of the tree
        # to prevent infinite recursions when re-computing sizes
        if z._data < y._data:
            if x._data < y._data:
                root = x
                root._parent = None
                #print('a-c-b about ' + str(z._data))
                y._left = x._right
                if x._right is not None:
                    x._right._parent = y
                z._right = x._left
                if x._left is not None:
                    x._left._parent = z
                x._left = z
                z._parent = x
                x._right = y
                y._parent = x
                z._updateHeightAndSizes()
                y._updateHeightAndSizes()
                if z.isUnbalanced():
                    z._rotate()
                if y.isUnbalanced():
                    y._rotate()
            else:
                root = y
                root._parent = None
                #print('a-b-c about ' + str(z._data))
                z._right = y._left
                if y._left is not None:
                    y._left._parent = z
                y._left = z
                z._parent = y
                z._updateHeightAndSizes()
                if z.isUnbalanced():
                    z._rotate()
        elif x._data < y._data:
            root = y
            root._parent = None
            #print('c-b-a about ' + str(z._data))
            z._left = y._right
            if y._right is not None:
                y._right._parent = z
            y._left = x
            x._parent = y
            y._right = z
            z._parent = y
            z._updateHeightAndSizes()
            if z.isUnbalanced():
                z._rotate()
        else:
            root = x
            root._parent = None
            #print('c-a-b about ' + str(z._data))
            y._right = x._left
            if x._left is not None:
                x._left._parent = y
            z._left = x._right
            if x._right is not None:
                x._right._parent = z
            x._left = y
            y._parent = x
            x._right = z
            z._parent = x
            z._updateHeightAndSizes()
            y._updateHeightAndSizes()
            if z.isUnbalanced():
                z._rotate()
            if y.isUnbalanced():
                y._rotate()

        # update heights and sizes on the new root
        root._updateHeightAndSizes()

        # re-parent the new root
        root._parent = parent
        if parent is not None:
            # glue new local root into the parent in place of z,
            # the old root
            if parent._left == z:
                parent._left = root
            else:
                parent._right = root

            # update the heights and sizes back up to the root
            parent._updateHeights()

        # return the new root of the rotated tree
        return root

    def find(self, e: Element) -> 'TreeNode':
        '''Search for an element in the tree, returning its node..

        :param e: the element
        :returns: the node holding the element, or None'''
        if e == self._data:
            return self
        elif e < self._data:
            if self._left is None:
                return None
            else:
                return self._left.find(e)
        else:
            if self._right is None:
                return None
            else:
                return self._right.find(e)

    def __iter__(self) -> Iterator[Element]:
        '''Return an iterator that returns elements in order.

        :returns: an iterator'''
        return self._inOrder()

    def _inOrder(self) -> Element:
        '''Generator t oreturn the elements of the tree
        in order using an in-order traverse.

        :returns: the next element'''
        if self._left is not None:
            yield from self._left._inOrder()
        yield self._data
        if self._right is not None:
            yield from self._right._inOrder()

    def _leftmost(self) -> 'TreeNode':
        '''Return the leftmost node in a tree. This by definition
        holds the smallest element.

        :returns: the leftmost node'''
        if self._left is None:
            return self
        else:
            return self._left._leftmost()

    def _rightmost(self) -> 'TreeNode':
        '''Return the rightmost node in a tree. This by defintion holds
        the largest element.

        :returns: the rightmost node'''
        if self._right is None:
            return self
        else:
            return self._right._rightmost()

    def discard(self, e) -> Tuple[bool, bool, 'TreeNode']:
        '''Delete the given element from the tree, if it is present.

        This method performs three integrated tasks. If the element
        is present, it is removed; the resulting set is tested
        for emptiness; and any change to the overall root is detected.
        These three tasks each form an element of the return value.

        :returns: a triple (waspresent, nowempty, newroot)'''
        if e == self._data:
            # grab the parent node that will need to have
            # the replacement re-attached
            parent = self._parent

            # switch on the states of sub-trees
            if self._left is None:
                if self._right is None:
                    # leaf node, can be deleted immediately
                    #print('leaf')
                    if parent is None:
                        # we're the last node in the tree
                        return (True, True, None)
                    else:
                        # delete from parent
                        if parent._left == self:
                            #print('on left')
                            parent._left = None
                        else:
                            #print ('on right')
                            parent._right = None
                        parent._updateHeights()
                        return (True, False, parent._rebalance(True))
                else:
                    #print('right sub-tree only')
                    # only a right sub-tree, slide up to replace
                    if parent is None:
                        # we're the root, replace us
                        self._right._parent = None
                        return (True, False, self._right)
                    else:
                        # replace us with our sub-tree
                        if parent._left == self:
                            parent._left = self._right
                            self._right._parent = parent
                        else:
                            parent._right = self._right
                            self._right._parent = parent
                        parent._updateHeights()
                        return (True, False, parent._rebalance(True))
            elif self._right is None:
                #print('left sub-tree only')
                # only a left sub-tree, slide up to replace
                if self._parent is None:
                    # we're the root, replace us
                    self._left._parent = None
                    return (True, False, self._left)
                else:
                    # replace us with our sub-tree
                    if parent._left == self:
                        parent._left = self._left
                        self._left._parent = parent
                    else:
                        parent._right = self._left
                        self._left._parent = parent
                    parent._updateHeights()
                    return (True, False, parent._rebalance(True))
            else:
                #print('two sub-trees')
                # two sub-trees, choose the least disruptive element
                # from the taller as replacement
                if self._left._height > self._right._height:
                    r = self._left._rightmost()
                    #print('replace with ' + str(r._data))
                else:
                    r = self._right._leftmost()
                    #print('replace with ' + str(r._data))
                self._data = r._data
                return r.discard(r._data)

        elif e < self._data:
            if self._left is None:
                return (False, False, None)
            else:
                return self._left.discard(e)
        else:
            if self._right is None:
                return (False, False, None)
            else:
                return self._right.discard(e)

    def draw(self) -> Element:
        '''Draw an element from the tree at random. This is the "textbook"
        solution to random draw:

        0.  If this node is a leaf, return the data on this node
        1.  Compute the total nodes beneath this one, including itself
        2.  Pick a random number between 0 and this value inclusive
        3a. If the value is less than or equal to the number of nodes
            in the left sub-tree, recursively draw from that sub-tree
        3b. Else, if the value is equal to one more than the number of nodes
            in the left sub-tree, return the data on this node
        3c. Else, recursively draw from the right sub-tree

        :returns: a random element'''
        l = len(self)
        if l == 1:
            return self._data
        else:
            i = self.rng.integers(l)
            if i < self._leftSize:
                return self._left.draw()
            elif i == self._leftSize:
                return self._data
            else:
                return self._right.draw()
