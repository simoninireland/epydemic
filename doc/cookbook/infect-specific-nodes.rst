.. _infect-specific-nodes:

.. currentmodule:: epydemic

Seeding the network with specific points of infection
=====================================================

**Problem**: You want to control where the infection initially starts, for example to 
put the infected nodes in an "unusual" place to study how that affects the epidemic.

**Solution**: Let's assume we're running an SIR model. By default the
:class:`CompartmentedModel` infects a random fraction of nodes according to the value
of the :attr:`SIR.P_INFECTED` parameter. If you want to take control then
two things need to happen:

1. Inhibit random infections
2. Decide on and infect the specific nodes of interest

The first is easy: set the parameter :attr:`SIR.P_INFECTED` to 0 and no nodes will be
randomly infected.

The second involves choosing nodes and then placing them into the :attr:`SIR.INFECTED`
compartment. If we have a model ``m`` and a set of nodes ``ns`` that we want to infect,
then:

.. code-block:: python

    for n in ns:
        m.changeCompartment(n, SIR.INFECTED)

will do the trick, and will keep track of the numbers of nodes in the various compartments.
This is probably best done by extending :meth:`SIR.setUp` so that, after the initial setup
has been done, we change the compartments of the selected nodes and then proceeds with
the simulation.

(The parameters you use depend on the model you're using: if you were working with an SIS model
then substitute :attr:`SIS.P_INFECTED` and so forth as appropriate.)
