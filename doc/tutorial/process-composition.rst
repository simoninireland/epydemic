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
both processes. Python offers a couple of ways to do this, and ``epydemic``
supports both.

The first way is using multiple inheritance. We construct a :class:`Process`
that has as its base classes the :class:`Process` sub-classes defining the
processesd we want to compose. Using our first example, we might define
a class:

.. code-block :: python

    class DynamicSIR(epydemic.SIR, epydemic.AddDelete):

        def __init__(self):
            super(DynamicSIR, self).__init__()

As it stands there is no new functionality in the combined class, and the
two processes will simply operate independently of each other. We might however
also add or override methods in the new class to provide code to "glue" the two
underlying processes together more closely. (See
:ref:`dynamic-population` to see this example explored in more detail.) 

The second way is to chain processes together using a :class:`ProcessSequence`,
for example:

.. code-block :: python

    p = epydemic.ProcessSequence(epydemic.SIR, epydemic.Monitor)

In this example the two processes will be built, set up, run, torn down,
and their results collected. (See :ref:`monitoring-progress` to see this
example in more detail.)

Which approach to choose? If you simply want to combine independent processes
together, with little interaction between them, then the :class:`ProcessSequence` 
is probably easiest to understand. The :class:`Monitor` and :class:`NetworkStatistics`
processes both work well when combined like this.

If however you need to provide some glue code to make the processes work together,
you generally need to sub-class one or more processes. This provides a place to
hang the glue code, and results in a :class:`Process` that can, if desired, be formed
into part of a :class:`ProcessSequence` subsequently.



