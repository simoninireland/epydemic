:class:`AddDelete`: The addition-deletion process
=================================================

.. currentmodule:: epydemic

.. autoclass:: AddDelete

Addition-deletion networks are networks in which nodes are added and removed by some
random process. They can be used for a number of purposes, perhaps most obviously to
model births and deaths, They can be combined (with care) with disease processes to model
situations where the underlying network is changing independently of the disease itself.

The canonical work on addition-deletion networks is :ref:`Moore, Ghosal, and Newman
<MGN06>`, which also showed that the process is very complex in its most general case.
Specific solutions are analytically solvable, however: most notably the case where
newly-added nodes are connected to a fixed number of neighbours selected randomly, which
is the default behaviour of this class. Other behaviours can be implemented by overriding
the :meth:`AddDelete.add` method (and, less commonly, the :meth:`AddDelete.remove` method).
Note that this is a slightly different formulation to that in the paper, which defines
an "addition kernel" as a function independent of the actions of the process:
implementationally it seems to make more sense to provide this functionality by
sub-classing rather than through a separate object.


Parameters
----------

The addition-deletion process is controlled by three parameters:

.. autoattribute:: AddDelete.P_ADD

.. autoattribute:: AddDelete.P_DELETE

.. autoattribute:: AddDelete.DEGREE


Loci
----

The addition-deletion process works independently of the size of the network: it
simply adds and delete nodes according to the probabilities given by the
:attr:`AddDelete.P_ADD` and :attr:`AddDelete.P_DELETE` parameters. Sincve it's
expensive in `networkx` to draw a random node, we keep track of them in a locus.

.. autoattribute:: AddDelete.NODES


Building the model
------------------

Building the model adds the add and remove events, independent of the network size.

.. automethod:: AddDelete.build

.. automethod:: AddDelete.setUp


Evolving the network
--------------------

Addition-deletion networks are intrinsically dynamic, so we override some methods from the
:class:`Process` evolution interface to keep track of the nodes added and deleted.

.. automethod:: AddDelete.addNode

.. automethod:: AddDelete.addNewNode

.. automethod:: AddDelete.newNodeName

.. automethod:: AddDelete.removeNode


Events
------

There are two events that can be triggered: one to add a node, and one to remove a node.
These two events provide the "kernel" of the addiiton-deletion process and can be specialised
to explore new behaviours.

.. automethod:: AddDelete.add

.. automethod:: AddDelete.remove

