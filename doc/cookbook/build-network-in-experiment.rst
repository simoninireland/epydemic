.. _build-network-in-experiment:

.. currentmodule:: epydemic

Creating random networks in the experiment
------------------------------------------

*Problem*: Rather than create a random network and pass it into the experimental dynamics,
you want to create it as part of the experiment itself. This will typically happen for one
of two reasons:

1. The structure of the network is a function of one of the experimental parameters
   you're varying; or
2. You're running experiments on an ``epyc`` distributed cluster, and you want to
   create the network worker-side to avoid passing it over the network.

*Solution*: To solve this problem we need to understand how ``epyc`` experiments work. When
an experiment is created, it has no parameters on which to work. before the experiment is run,
its parameters are set by calling the ``set`` method. If this is the first time parameters
have been set, the ``configure`` method gets called to configure the experiment with the
given paraneters. If this *isn't* the first time parameters have been set, the ``deconfigure`` method
gets called first to tear-down the current configuration, followed by a call to ``configure``.

To generate a network from a given set of parameters, then, we simply sub-class the dynamics
class and override its ``configure`` method to create a network and store it using
:meth:`Dynamics.setNetworkPrototype`. For example,

.. code-block:: python

    class ERPopulation(epydemic.CompartmentedStochasticDynamics):

        def configure( self, params ):
            '''Create a prototype ER network when parameters are set. This expects a
            parameter N for the number of nodes in the network, and one of
            kmean (average degree) or phi (connection probability).

            :param params: the experimental parameters'''

            # extract ER network parameters
            N = params['N']
            kmean = params['kmean']
            phi = params['phi']
            if phi is None:
                phi = (kmean + 0.0) / N

            # create a connected network with no self-loops
            g = networkx.erdos_renyi_network(N, phi)
            g = g.subgraph(max(networkx.connected_components(g), key = len)).copy()
            g.remove_edges_from(list(g.selfloop_edges()))

            # store the network for use
            self.setNetworkPrototype(g)

         def deconfigure( self ):
            '''Undo the current experimental configuration.'''
            self.setNetworkPrototype(None)
