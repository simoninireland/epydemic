:class:`Locus`: Loci of disease dynamics
========================================

.. currentmodule:: epydemic

Loci are an abstraction of where events happens within a model. The
dynamics of a model defines what events are called; the loci define
the population of nodes or edges that may be subject to a particular
event.

The management of loci is automated as far as possible within the procedural
interface for evolving the working network within :class:`Process`. Using these
methods (and the methods extended in sub-classes) hopefully renders the machinery
largely transparent.

.. autoclass:: Locus
   :show-inheritance:

There are three four access methods defined on loci: to get the locus' name,
to get the size of the locus (the number of nodes or edges it contains); to retrieve
the elements themselves; and to draw one element at random.

.. automethod:: Locus.name

.. automethod:: Locus.__len__

.. automethod:: Locus.elements

.. automethod:: Locus.draw

There are also two abstract methods that define the way in which
changes in node compartments are reflected in the populations of loci.

.. automethod:: Locus.leaveHandler

.. automethod:: Locus.enterHandler

It is these methods that are overridden in sub-classes to provide the
behaviour of node and edge loci.


Locus sub-classes
-----------------

The two main locus sub-classes arev used when modelling a :term:`compartmented model of disease`, to
capture the nodes and edges in the various compartments where dynamics occurs.

.. autoclass:: CompartmentedNodeLocus
   :show-inheritance:

.. autoclass:: CompartmentedEdgeLocus
   :show-inheritance:

.. automethod:: CompartmentedEdgeLocus.matches

.. automethod:: CompartmentedEdgeLocus.enterHandler

.. automethod:: CompartmentedEdgeLocus.leaveHandler

