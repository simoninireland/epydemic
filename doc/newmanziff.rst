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


The Newman-Ziff algorithm
-------------------------

While percolation can also be used in conjunction with epidemic processes, it is often
used standalone to study the size of the giant connected component (GCC) formed by the
occupied sub-graph. An algorithm due to Newman and Ziff :cite:`NewmanZiff` can generate
instances of percolated sub-graphs for *every* value of :math:`\phi` in a single
sweep through the network. The algorithm is very fast, performing (for example) a
site percolation experiment on a million-node network in under 30s.

Newman-Ziff has variants for both bond (occupying edges) and site
(occupying nodes) percolation. Both derive from the same base class,
which isn't used directly.

.. autoclass:: NewmanZiff
   :show-inheritance:

Two methods control the lifecycle of the percolation experiment.

.. automethod:: NewmanZiff.setUp

.. automethod:: NewmanZiff.tearDown

Two other methods control sampling and reporting.

.. automethod:: NewmanZiff.sample

.. automethod:: NewmanZiff.report

There are several methods that can be used to query the progress of a
percolation process or to create new percolation process variants.

.. automethod:: NewmanZiff.components

.. automethod:: NewmanZiff.componentSize

.. automethod:: NewmanZiff.largestComponentSize

.. automethod:: NewmanZiff.inLargestComponent

These are mainly used either for sub-classing when creating new
percolation experiments, or in defining :ref:`events <nz-events>` for
use with :ref:`event taps <event-taps>`


Results
-------

Percolation is a very detailed process, occupying edges or nodes one
at a time. This makes it both time-consuming and data-rich: *too*
data-rich in the main. For this reason the constructors take either a
number or a sequence of sample points at which to return data about
the progress of the process.

Both bond and site percolation processes result in two time series:
one consisting of the percolation probabilities at which the process
was sampled; and the other holding the sizes of the largest connected
component at these probabilities.

.. warning::

   Versions of ``epydemic`` prior to 1.9.1 laid-out the results of
   percolation processes slightly differently.


Bond percolation
----------------

.. autoclass:: BondPercolation
   :show-inheritance:

.. automethod:: BondPercolation.setUp

.. automethod:: BondPercolation.do

The percolation process returns two time series:

.. autoattribute:: BondPercolation.P

.. autoattribute:: BondPercolation.GCC

The process has two events:

.. autoattribute:: BondPercolation.OCCUPY

.. autoattribute:: BondPercolation.SAMPLE


Site percolation
----------------

.. autoclass:: SitePercolation
   :show-inheritance:

.. autoattribute:: SitePercolation.OCCUPY

.. automethod:: SitePercolation.setUp

.. automethod:: SitePercolation.do

The percolation process returns two time series:

.. autoattribute:: SitePercolation.P

.. autoattribute:: SitePercolation.GCC

The process has two events:

.. autoattribute:: SitePercolation.OCCUPY

.. autoattribute:: SitePercolation.SAMPLE


.. _nz-events:

Events
------

Both bond and site percolation have two types of event:

- A "occupation" event, occurring whenever an edge or node is occupied
  as part of the percolation; and
- A "sampling" event, which occurs every time the largest component is
  sampled according to the schedule set in the constructor.

Each event is fed to the :ref:`event taps interface <event-taps>`. The
occupation event passes whichever element was occupied, the sampling
event always passes `None`.
