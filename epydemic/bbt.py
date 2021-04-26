# A AVL tree with random draw
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

from epydemic import Bitstream, Element
from typing import List, Tuple, Iterable, Optional


class TreeNode(object):
    '''A node in an AVL tree. This is used within :class:`DrawableSet`
    to maintain the contents of a locus in a way that can perform a
    random fair draw of its contents.

    :param d: the data at the tree node
    :param p: (optional) the parent node (defaults to None)

    '''

    def __init__(self, d: Element, p: Optional['TreeNode'] = None):
        self._left: Optional['TreeNode'] = None    # left sub-tree
        self._right: Optional['TreeNode'] = None   # right sub-tree
        self._parent: Optional['TreeNode'] = p     # parent nodes
        self._data: Element = d                    # value at this node
        self._height: int = 0                      # height of the tree

    def __len__(self) -> int:
        '''Return the size of the tree. This is intended for testing only,
        as it's a slow recursive count: :class:`DrawableSet` maintains
        its size itself.

        :returns: the size of the tree'''
        s = 1
        if self._left is not None:
            s += len(self._left)
        if self._right is not None:
            s += len(self._right)
        return s

    def add(self, e: Element) -> Tuple[bool, Optional['TreeNode']]:
        '''Add an element to the tree.

        This method performs two tasks. It adds the element, testing
        whether it was in fact added or was a repetition; and it
        potentially replaces trhe overall tree root.

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
        '''Walk back to the root updating the heights of nodes.'''
        if self._updateHeight() and self._parent is not None:
            self._parent._updateHeights()

    def _updateHeight(self) -> bool:
        '''Update the node height.

        :returns: True if the height of the node changed'''
        lh = self._left._height + 1 if self._left is not None else 0
        rh = self._right._height + 1 if self._right is not None else 0
        h = max(lh, rh)
        if h != self._height:
            self._height = h
            return True
        else:
            return False

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
        '''Return the taller of teh node's sub-trees.

        :returns: the smaller sub-tree'''
        lh = self._left._height + 1 if self._left is not None else 0
        rh = self._right._height + 1 if self._right is not None else 0
        if lh > rh:
            return self._left
        else:
            return self._right

    def _rebalance(self, recursive: bool = False) -> Optional['TreeNode']:
        '''Re-balance the tree after addition of a node. If the re-balancing
        is recursive (which is needed after deletions, but not after
        additions) then the re-balancing proceeds up the tree to the
        root.

        :param recursive: (optional) True to recursively re-balance (defaults to False)
        :returns: the new overall root, or None if the root hasn't been changed

        '''

        # find the shallowest unbalanced node
        z = self._findUnbalanced()
        if z is None:
            # tree is balanced all the way up
            return None
        else:
            root = z._rotate()

            if root._parent is None:
                return root
            elif recursive:
                # call again on the parent
                return root._parent._rebalance(True)
            else:
                return None

    def _rotate(z) -> Optional['TreeNode']:
        '''Perform a single rotation to re-balance the node.

        :returns: the new overall root, or None if the root hasn't been changed

        '''

        # we use z instead of the more usual self as the name for
        # the node on which the method is called, to match the
        # normal usage when describing AVL operations for which
        # z is always the root node.

        # find the two other nodes for the rotation
        y = z._tallerSubtree()
        x = y._tallerSubtree()

        # grab the parent to which we'll re-attach the new root
        # after rotation
        parent = z._parent

        # perform the appropriate rotation
        if z._data < y._data:
            if x._data < y._data:
                root = x
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
                z._updateHeight()
                y._updateHeight()
                if z.isUnbalanced():
                    z._rotate()
                if y.isUnbalanced():
                    y._rotate()
                x._updateHeight()
            else:
                root = y
                #print('a-b-c about ' + str(z._data))
                z._right = y._left
                if y._left is not None:
                    y._left._parent = z
                y._left = z
                z._parent = y
                z._updateHeight()
                if z.isUnbalanced():
                    z._rotate()
                y._updateHeight()
        elif x._data < y._data:
            root = y
            #print('c-b-a about ' + str(z._data))
            z._left = y._right
            if y._right is not None:
                y._right._parent = z
            y._left = x
            x._parent = y
            y._right = z
            z._parent = y
            z._updateHeight()
            if z.isUnbalanced():
                z._rotate()
            y._updateHeight()
        else:
            root = x
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
            z._updateHeight()
            y._updateHeight()
            if z.isUnbalanced():
                z._rotate()
            if y.isUnbalanced():
                y._rotate()
            x._updateHeight()

        # re-parent the new root
        root._parent = parent
        if parent is not None:
            # glue new local root into the parent in place of z,
            # the old root
            if parent._left == z:
                parent._left = root
            else:
                parent._right = root

            # update the heights back up to the root
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

    def inOrderTraverse(self) -> List[Element]:
        '''Perform an iun-order traverse opf the tree, which generates
        all the elements in order.

        :returns: a list of elements'''
        es = []
        if self._left is not None:
            es.extend(self._left.inOrderTraverse())
        es.append(self._data)
        if self._right is not None:
            es.extend(self._right.inOrderTraverse())
        return es

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
        '''Draw an element from the tree at random.

        This implementation isn't fair (yet).

        :returns: a random element, or none if the set is empty'''
        bs = Bitstream.default_rng()
        pathlength = bs.integer(self._height)
        n = self
        bits = iter(bs)
        for _ in range(pathlength):
            b = next(bits)
            if b == 0:
                n = n._left
            else:
                n = n._right
            if n is None:
                n = self
        return n._data
