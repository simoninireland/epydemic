:class:`DrawSet`: A set with an efficient random draw
=====================================================

.. currentmodule:: epydemic

.. autoclass:: DrawSet


The set interface
-----------------

.. automethod:: DrawSet.add

.. automethod:: DrawSet.__contains__

.. automethod:: DrawSet.empty

.. automethod:: DrawSet.__len__

.. automethod:: DrawSet.__iter__

.. automethod:: DrawSet.discard

.. automethod:: DrawSet.remove


Random drawing
--------------

The point of this class is to provide a way of drawing a random
element efficiently, which isn't possible using the standard Python
set interface.

.. automethod:: DrawSet.draw
