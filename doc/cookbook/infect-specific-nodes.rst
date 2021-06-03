.. _infect-specific-nodes:

.. currentmodule:: epydemic

Seeding the network with specific points of infection
=====================================================

**Problem**: You want to control where the infection initially starts,
for example to put the infected nodes in an "unusual" place to study
how that affects the epidemic.

**Solution**: Let's assume we're running an SIR model. By default the
:class:`CompartmentedModel` infects a random fraction of nodes
according to the value of the :attr:`SIR.P_INFECTED` parameter. If you
want to take control then two things need to happen:

1. Inhibit random infections
2. Decide on and infect the specific nodes of interest

A common sub-case of this approach is to infect exactly one node at
random. One could do this by setting :attr:`SIR.P_INFECTED` to
:math:`\frac{1}{N}`, but that runs the risk of infecting not *exactly*
one node -- and if you happen to infect no nodes, everything will
break.

There are (at least) two ways to implement this depending on exactly
what you want to accomplish. (We'll assume an :class:`SIR` model:
change parameter names accordingly for other models.)


Solution 1: By hand
-------------------

First inhibit random seeding by setting the parameter
:attr:`SIR.P_INFECTED` to 0 so that no nodes will be randomly
infected.

We then need to choose the seed nodes and place them into the
:attr:`SIR.INFECTED` compartment. If we have a model ``m`` and a set
of nodes ``ns`` that we want to infect, then:

.. code-block:: python

    for n in ns:
	m.changeCompartment(n, SIR.INFECTED)

will do the trick, and will keep track of the numbers of nodes in the
various compartments. This is probably best done by extending
:meth:`CompartmentedModel.setUp` so that, after the initial setup has been done, we
change the compartments of the selected nodes and then proceeds with
the simulation.

This approach has the advantage of minimally intruding on the initial
compartment distribution: it just takes control of the setting of
nodes in one compartment.


Solution 2: By changing the initial seeding procedure
-----------------------------------------------------

The alternative way, which is arguably cleaner, is to change the way
in which initial compartments are assigned. To do this we have to
account for the compartments of *all* the nodes -- not just the
infected ones. We can do this by overriding
:meth:`CompartmentedModel.initialCompartments` like this:

.. code-block:: python

    def build(self, params):
	'''Build the network without any initial random infection.

	:param params: the experimental parameters'''
	params[self.P_INFECTED] = 0.0
	super().build(params)

    def initialCompartments(self):
	'''Infect exactly one node, chosen at random.'''
	g = self.network()
	ns = set(g.nodes())
	N = len(ns)

	# choose one node and infect it
	rng = numpy.random.default_rng()
	n = rng.integers(N)
	self.changeInitialCompartment(n, self.INFECTED)

	# mark all other nodes as susceptible
	ns.remove(n)
	for n in ns:
	    self.changeInitialCompartment(n, self.SUSCEPTIBLE)

Overriding :meth:`CompartmentedModel.build` inhibits random seeding by
setting the probability to zero. (We have to do this as the
:meth:`SIR.build` method sets the initial distribution and so accesses
the :attr:`SIR.P_INFECTED` parameter -- and fails if it isn't
set. Other compartmented models do the same.)

The overridden :meth:`CompartmentedModel.initialCompartments` first
chooses a node, marks it as infected, and then marks all other nodes
as susceptible. You would of course need to change this if there was
some other compartment that might be set from the initial compartment
distribution.
