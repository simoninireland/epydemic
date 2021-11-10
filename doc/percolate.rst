:class:`Percolate`: Perform bond percolation
============================================

.. currentmodule:: epydemic

.. autoclass:: Percolate


Using percolation
-----------------

One can use percolation as an end in itself: percolation is often used
as a substitute for spidemic simulation, following the well-known
similarity between the contact network arising from epidemic infection
and the edges occupied by bond percolation.

A different usage comes when percolating a network prior to (or
possibly after) some other process being run. This takes a base
network and runs a percolation process on it first, before running
another process on the remaining ("residual") network. The cleanest
way to structure this sort of code is to use a
:class:`ProcessSequence` with an instance of :class:`Percolate`
followed by the process for the residual network. This will run the
:meth:`Process.build` methods in order, percolating the base network
before building the second process' structures.


Percolation
-----------

The probability that an edge is retained is given by an experimental parameter.

.. autoattribute:: Percolate.T

Given this, the percolation process itself simply registers edges as either
occupied or unoccupied. It then executes an action for each of these sets.

.. automethod:: Percolate.percolate


Actions
-------

The actions of percolation concern what to do with the occupied and unoccupied
edges.

.. automethod:: Percolate.occupy

.. automethod:: Percolate.unoccupy

Building
--------

.. automethod:: Percolate.build
