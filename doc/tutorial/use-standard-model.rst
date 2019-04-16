.. _use-standard-model:

.. currentmodule:: epydemic

Running a process
=================

Both the process we built in :ref:`build-sir`, and ``epydemic``'s built-in processes,
take a range of parameters and use them when building the model. These are provided as
a dict, with the contents depending on the model we'll be building. Continuing with
the SIR process, we need to provide three paremeters for the infection probability,
the removal probability, and the initial seeding probability.

.. code-block:: python

    param = dict()
    param[SIR.P_INFECT] = 0.1
    param[SIR.P_REMOVE] = 0.5
    param[SIR.P_INFECTED] = 0.01

We can run the simulation over any appropriate network. A network whose degree distribution
followed a :ref:`powerlaw with cutoff <model-human-population>` would probably be most
realistic, but for now we'll just use an ER random graph model.

.. code-block:: python

    import networkx

    N = 10000                 # order (number of nodes) of the network
    kmean = 5                 # mean node degree
    phi = (kmean + 0.0) / N   # probability of attachment between two nodes chosen at random

    # create the network
    g = networkx.erdos_renyi_graph(N, phi)

We can now perform a single run of the simulation, using :term:`stochastic dynamics`.

.. code-block:: python

    # create a model and a dynamics to run it
    m = SIR()                      # the model (process) to simulate
    e = StochasticDynamics(m, g)   # use stochastic (Gillespie) dynamics

    # set the parameters we want and run the simulation
    rc = e.set(param).run()

If for some reason we wanted to use synchronous dynamics, we'd simply replace the
simulation dynamics framework: the same models work under both frameworks.

.. code-block:: python

    f = SynchronousDynamics(m, g)
    rc = f.set(param).run()

We can re-run the simulation, with or without changing the parameters.

.. code-block:: python

    # re-run with the same parameters
    e.run()

    # change something and re-run
    param[SIR.P_REMOVE] = 1.0
    e.set(param).run()

We can also change the network.

.. code-block:: python

    h = networkx.erdos_renyi_graph(N * 2, (kmean + 0.0) / (N * 2))
    e.setNetwork(h)
    e.run()


