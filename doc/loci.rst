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

There are three four access methods defined on loci: to get the locus' name,
to get the size of the locus (the number of nodes or edges it contains); to retrieve
the elements themselves; and to draw one element at random.

.. automethod:: Locus.name

.. automethod:: Locus.__len__

.. automethod:: Locus.elements

.. automethod:: Locus.draw


Handlers
--------

There are also four methods that define the way in which
changes in the network are reflected in the populations of loci.

.. automethod:: Locus.addHandler

.. automethod:: Locus.leaveHandler

.. automethod:: Locus.enterHandler

.. automethod:: Locus.removeHandler

It is these methods that are overridden in sub-classes to provide the
behaviour of node and edge loci.


Locus sub-classes
-----------------

The two main locus sub-classes are used when modelling a :term:`compartmented model of disease`, to
capture the nodes and edges in the various compartments where dynamics occurs. These compartments
are used by :class:`CompartmentedModel`.

.. autoclass:: CompartmentedNodeLocus
   :show-inheritance:

.. autoclass:: CompartmentedEdgeLocus
   :show-inheritance:

The compartmented edge locus extends the default handler methods.

.. automethod:: CompartmentedEdgeLocus.matches

.. automethod:: CompartmentedEdgeLocus.addHandler

.. automethod:: CompartmentedEdgeLocus.enterHandler

.. automethod:: CompartmentedEdgeLocus.leaveHandler

.. automethod:: CompartmentedEdgeLocus.removeHandler

