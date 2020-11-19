Helper types
============

``epydemic`` uses ``networkx`` to represent the underlying networks. ``networkx`` is
extremely fleible in how it represents the nmodes of a network (graph): pretty much
any object can be used, although in practice one often encounters either strings or
integers. (The latter are especially common in network science, as the nodes don't
actually represent "real" objects and so don't have meaningful names.)

``epydemic`` also uses `Python type annotations <https://docs.python.org/3/library/typing.html>`_
on methods and attributes to improve programming safety. Since using ``Any`` types
extensively isn't very intuitive, we provide three "helper" types for describing
the structure of networks:

* ``Node``, the type of nodes, aliased to ``Any``
* ``Edge``, the type of edges, represented as a tuple of two ``Node`` objects
* ``Element``, a union of ``Node`` and ``Edge``

You'll find these types used for each :term:`event function`, and in the examples.
Since they're type aliases you can always use the underlying ``Any`` types
if you prefer, but future versions of ``epydemic`` may make these types stronger
rather than simply being aliases.


