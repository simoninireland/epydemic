Bond and site percolation
=========================

.. currentmodule:: epydemic

Percolation processes are common in physics as a way to study the gradual accretion of
nodes (site percolation) or edges (bond percolation) in a network. The process itself is
easy to describe.

**Bond percolation**: The network has all its edges labelled as "unoccupied". For a given
probability :math:`\phi` each edge is marked as occupied. At the end of this process the
occupied edges will determine a sub-graph of the original network, consisting of one or
more connected components.

**Site percolation**: The network's nodes are marked an unoccupied, and each is then occupied
with probability :math:`\phi`. At the end of the process the edges between occupied nodes
are  marked as occupied, and again define a sub-graph.

.. note ::

    To perform bond (edge) percolation in conjuction with epidemic processes
    see :class:`Percolate`.

The reason percolation is of interest is that it provides a model of a wide range of
interesting processes. (Originally it was used to study crack formation in crystals
and waterflow in soils.) It also bears a striking similarity to the ways in which
epidemics form, with the final occupied sub-graph being mathematically related to the
contact tree of an epidemic. This lets us study epidemics using percolation, an approach
pioneered by Newman :cite:`NewmanEpidemicDisease`.

While percolation can also be used in conjunction with epidemic processes, it is often
used standalone to study the size of the giant connected component (GCC) formed by the
occupied sub-graph. An algorithm due to Newman and Ziff :cite:`NewmanZiff` can generate
instances of percolated sub-graphs for *every* value of :math:`\phi` in a single
sweep through the network. The algorithm is very fast, performing (for example) a
site percolation experiment on a million-node network in under 30s.


Bond percolation
----------------

.. autoclass:: BondPercolation
   :show-inheritance:

.. autoattribute:: BondPercolation.OCCUPY

.. automethod:: BondPercolation.setUp

.. automethod:: BondPercolation.do

The percolation process returns two values:

.. autoattribute:: BondPercolation.P

.. autoattribute:: BondPercolation.GCC


Site percolation
----------------

.. autoclass:: SitePercolation
   :show-inheritance:

.. autoattribute:: SitePercolation.OCCUPY

.. automethod:: SitePercolation.setUp

.. automethod:: SitePercolation.do

The percolation process returns two values:

.. autoattribute:: SitePercolation.P

.. autoattribute:: SitePercolation.GCC


Events
------

Both bond and site percolation treat each individual occupation of a
bond or site as an event which is fed to the :ref:`event taps
interface <event-taps>`. For bond percolation, the element associated
with the event is the newly-occupied edge; for sites, it is the
newly-occupied node.
