.. _build-network-in-experiment:

.. currentmodule:: epydemic

Creating random networks in the experiment
==========================================

**Problem**: Rather than create a random network and pass it into the experimental dynamics,
you want to create it as part of the experiment itself. This will typically happen for one
of two reasons:

1. The structure of the network is a function of one of the experimental parameters
   you're varying; or
2. You're running experiments on an ``epyc`` distributed cluster, and you want to
   create the network worker-side to avoid passing it over the network.

**Solution**: To solve this problem we need to understand how ``epyc`` experiments work. When
an experiment is created, it has no parameters on which to work. before the experiment is run,
its parameters are set by calling the ``set`` method. If this is the first time parameters
have been set, the ``configure`` method gets called to configure the experiment with the
given parameters. If this *isn't* the first time parameters have been set, the ``deconfigure`` method
gets called first to tear-down the current configuration, followed by a call to ``configure``.

The correct place to create the network is in the :class:`Dynamics` class that runs the experiment.
Rather than pass a prototype network to the dynamics (as we would normally do, either at
construction or by calling :meth:`Dynamics.setPrototypeNetwork`), we instead provide code
to create (and delete) a network at appropriate points in the experimental lifecycle.
We sub-class the dynamics class we want to use and override its ``configure`` method.
For example, using :class:`StochasticDynamics` we would have:

.. code-block:: python

    class StochasticDynamicsOverER(epydemic.StochasticDynamics):

         def __init__(self, p):
            super(StochasticDynamicsOverER, self).__init__(p)

         def configure(self, params):
            '''Create a prototype ER network when parameters are set. This expects a
            parameter N for the number of nodes in the network, and one of
            kmean (average degree) or phi (connection probability).

            :param params: the experimental parameters'''
            super(StochasticDynamicsOverER, self).configure(params)

            # extract ER network parameters
            N = params['N']
            kmean = params['kmean']
            if 'phi' in params.keys():
               phi = params['phi']
            else:
               phi = (kmean + 0.0) / N

            # create a network with no self-loops
            g = networkx.gnp_random_graph(N, phi)
            g.remove_edges_from(list(networkx.selfloop_edges(g)))

            # store the network as the prototype for experiments
            self.setNetworkPrototype(g)

         def deconfigure(self):
            '''Undo the current experimental configuration.'''
            super(StochasticDynamicsOverER, self).deconfigure()
            self.setNetworkPrototype(None)

What we've done here is add a ``configure`` method that creates a network based on values provided
as experimental parameters -- additional to those that the experiment expects anyway. In this case
we expect a parameter "N" for the network size and either a mean degree "kmean" or a link probability
"phi", from which we construct an ER network as the prototype. (In practice you'd probably want to name
these parameters using constants, just for good practice.)

Notice that both the ``configure`` and the ``deconfigure`` method call the underlying method
that they override, to make sure that the basic (de)configuration behaviour is still done.
