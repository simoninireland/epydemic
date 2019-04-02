:class:`AddDelete`: The addition-deletion process
=================================================

.. currentmodule:: epydemic

.. autoclass:: AddDelete

Addition-deletion networks are networks in which nodes are added and removed by some
random process. They can be used for a number of purposes, perhaps most obviously to
model births and deaths, They can be combined (with care) with disease processes to model
situations where the underlying network is changing independently of the disease itself.

The canonical work on addition-deletion networks is due to :ref:`Moore, Ghosal, and Newman
<MGN06>`, which also showed that the process is very complex in its most general case.
Specific solutions are solvable, however: most notably,


Parameters
----------

The addition-deletion process is controlled by three parameters:

.. autoattribute:: AddDelete.P_ADD

.. autoattribute:: AddDelete.P_DELETE

.. autoattribute:: AddDelete.DEGREE


Dynamics
--------

The addition-deletion process works independently of the size of the network: it
simply adds and delete nodes according to the probabilities given by the
:attr:`AddDelete.P_ADD` and :attr:`AddDelete.P_DELETE` parameters.


Building the model
------------------

Building the model adds the add and remove events, independent of the network size.

.. automethod:: AddDelete.build


Event methods
-------------

There are two events that can be triggered: one to add a node, and one to remove a node.

.. automethod:: AddDelete.add

.. automethod:: AddDelete.remove

