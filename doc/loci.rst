:class:`Locus`: Loci of disease dynamics
========================================

.. currentmodule:: epydemic

Loci are an abstraction of where disease happens within a model. The
dynamics of a model defines what events are called; the loci define
the population of nodes or edges that may be subject to a particular
event.

There will seldom be any need to understand (or even interact with)
loci except if, for example, defining new dynamics. For building and
operating model simulations, loci are transparent for the programmer. 


:class:`Locus`: The base class
------------------------------

.. autoclass:: Locus
   :show-inheritance:

.. automethod:: Locus.name

There are three main access methods defined on loci: to get the length
of the locus (the number of nodes or edges it contains); to retrieve
the elements themselves; and to draw one element at random.

.. automethod:: Locus.__len__

.. automethod:: Locus.elements

.. automethod:: Locus.draw

Events are attached to loci with a given probability.

.. automethod:: Locus.addEvent

.. automethod:: Locus.events

There are also two abstract methods that define the way in which
changes in node compartments are reflected in the populations of loci.

.. automethod:: Locus.leaveHandler

.. automethod:: Locus.enterHandler

It is these methods that are overridden in sub-classes to provide the
behaviour of node and edge loci.


:class:`Singleton`: A locus for the network
-------------------------------------------

.. autoclass:: Singleton
   :show-inheritance:

.. automethod:: Singleton.__len__

.. automethod:: Singleton.elements

.. automethod:: Singleton.draw

.. automethod:: Singleton.leaveHandler

.. automethod:: Singleton.enterHandler


:class:`AllNodes`: A locus holding all the nodes in a network
-------------------------------------------------------------

.. autoclass:: AllNodes
   :show-inheritance:

.. automethod:: AllNodes.__len__

.. automethod:: AllNodes.elements

.. automethod:: AllNodes.draw

.. automethod:: AllNodes.leaveHandler

.. automethod:: AllNodes.enterHandler


:class:`AllEdges`: A locus holding all the edges in a network
-------------------------------------------------------------

.. autoclass:: AllEdges
   :show-inheritance:

.. automethod:: AllEdges.__len__

.. automethod:: AllEdges.elements

.. automethod:: AllEdges.draw

.. automethod:: AllEdges.leaveHandler

.. automethod:: AllEdges.enterHandler



:class:`CompartmentedNodeLocus`: Loci for node-level dynamics
------------------------------------------------

.. autoclass:: CompartmentedNodeLocus
   :show-inheritance:

.. automethod:: CompartmentedNodeLocus.leaveHandler

.. automethod:: CompartmentedNodeLocus.enterHandler



:class:`CompartmentedEdgeLocus`: Loci for edge-level dynamics
------------------------------------------------

.. autoclass:: CompartmentedEdgeLocus
   :show-inheritance:

.. automethod:: CompartmentedEdgeLocus.leaveHandler

.. automethod:: CompartmentedEdgeLocus.enterHandler
