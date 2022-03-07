.. _no-multiple-inheritance:

.. currentmodule:: epydemic

Multiple inheritance (or not)
=============================

One might consider that Python's multiple inheritance would be an
easier way to compose processes rather than using a
:class:`ProcessSequence`.  We don't recommend this approach as it's a
lot harder to control the sequences of interactions that need to
occur.

.. warning::

   Versions of ``epydemic`` prior to 1.8.1 used multiple inheritance
   internally, as well as in examples and the test suite.

The issue is that multiple inheritance imposes a single order on the
compositions of methods, defined by the method resolution order or
MRO. These restrictions don't always align with what's needed by
``epydemic``. In particular it can make it hard to correctly define
when a process has reached equilibrium.

A more serious restriction is that further composition --
whether by sequence or by further inheritance -- can create a
situation in which one need to change the order of the previous
multiply-inherited methods. While this can be done, it's liable to
lead to errors and even in the best case requires code duplication and
awkward calls that jump-around the inheritance hierarchy.

All things considered, using a :class:`ProcessSequence` makes
classes more re-usable and easier to compose when building more
complex processes.
