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

There are several ways to implement this depending on exactly what you
want to accomplish, the easiest of which is to directly code the
required behaviour in a sub-class of the model you want to
seed. (We'll assume an :class:`SIR` model: change parameter names
accordingly for other models.)


Changing the initial seeding procedure
--------------------------------------

To take control of the seeding procedure we have to account for the
compartments of *all* the nodes -- not just the infected ones. We can
do this by overriding
:meth:`CompartmentedModel.initialCompartments`. If, for example, we
wanted exactly one seed node, chosen at random, then we could do
the following:

.. code-block:: python

    from epydemic import rng       # the random number generator

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
	n = rng.integers(N)
	self.changeInitialCompartment(n, self.INFECTED)

	# mark all other nodes as susceptible
	ns.remove(n)
	for n in ns:
	    self.changeInitialCompartment(n, self.SUSCEPTIBLE)

(We've imported ``epydemic``'s :ref:`global random number generator
<rng>` from which we draw the numbers we need.) Overriding
:meth:`CompartmentedModel.build` inhibits random seeding by setting
the probability to zero. (We have to do this as the :meth:`SIR.build`
method sets the initial distribution and so accesses the
:attr:`SIR.P_INFECTED` parameter -- and fails if it isn't set. Other
compartmented models do the same.)

The overridden :meth:`CompartmentedModel.initialCompartments` first
chooses a node, marks it as infected, and then marks all other nodes
as susceptible. You would of course need to change this if there was
some other compartment that might be set from the initial compartment
distribution.
