:class:`Locus`: Loci of disease dynamics
========================================

.. currentmodule:: epydemic

Loci are an abstraction of where disease happens within a model. The
dynamics of a model defines what events are called; the loci define
the population of nodes or edges that may be subject to a particular
event. The :class:`CompartmentedModel` class keeps track of these
populations automatically from the definition of a model.

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

There are also two abstract methods that define the way in which
changes in node compartments are reflected in the populations of loci.

.. automethod:: Locus.leaveHandler

.. automethod:: Locus.enterHandler

It is these methods that are overridden in sub-classes to provide the
behaviour of node and edge loci.


:class:`NodeLocus`: Loci for node-level dynamics
------------------------------------------------

.. autoclass:: NodeLocus
   :show-inheritance:

.. automethod:: NodeLocus.leaveHandler

.. automethod:: NodeLocus.enterHandler



:class:`EdgeLocus`: Loci for edge-level dynamics
------------------------------------------------

.. autoclass:: EdgeLocus
   :show-inheritance:

.. automethod:: EdgeLocus.leaveHandler

.. automethod:: EdgeLocus.enterHandler
