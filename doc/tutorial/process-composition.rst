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

There are more complicated ways of composing processes together where
the component processes can interact with each other directly by
name. See the :ref:`cookbook recipe <dynamic-population>` for an example.


Multiple inheritance
--------------------

We :ref:`no longer recommend using multiple inheritance
<no-multiple-inheritance>` to compose processes.
