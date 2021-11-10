.. _process-composition:

.. currentmodule:: epydemic

Composing processes
===================

Epidemic models can sometimes require processes that are quite
complicated in structure. For example we might want to model a disease
running over a changing network, perhaps one with a background
rate of birth and death. It would make sense to describe these
two aspects of the system separately, since they might be re-usable
in different contexts. As another example, we might want to
perform an analysis at the end of an experiment that is shared between
different processes, and again it makes sense to define these
independently so they can be re-used. This is simply good software
engineering practice, separating concerns and modularising the simulation code.

To make this approach work, we need to be able to take network
process definitions (instances of :class:`Process`) and combine them
together to create another :class:`Process` instance that performs
both processes.


Process sequencing
------------------

The best way to chain processes together uses a :class:`ProcessSequence`,
for example:

.. code-block:: python

    p = epydemic.ProcessSequence(epydemic.SIR, epydemic.Monitor)

In this example the two processes will be built, set up, run, torn down,
and their results collected. (See :ref:`monitoring-progress` to see this
example in more detail.)


.. _no-multiple-inheritance:

Multiple inheritance
--------------------

Another way to compose processes is to use Python's multiple
inheritance, We don't recommend this approach as it's a lot harder to
control the sequences of interactions that need to occur.

.. warning::

   Versions of ``epydemic`` prior 1.8.1 used multiple inheritance
   internally, as well as in examples.

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
