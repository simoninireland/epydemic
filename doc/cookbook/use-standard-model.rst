.. _use-standard-model:

.. currentmodule:: epydemic

Using a standard compartmented model
====================================

`epydemic` comes with some standard epidemic models built-in. Most are examples of a
:term:`compartmented model of disease`, with nodes representing individuals that each
reside in some state -- the :term:`compartments` -- and moving between them
under the influence of some stochastic process.

The simplest example of a compartment model is given by the :class:`SIR` model
representing a disease by three states:

    - (S)usceptible nodes, which can be infected with the disease;
    - (I)nfected nodes, which will infect adjacent susceptible nodes
      with some probability; and
    - (R)emoved nodes, which are infected nodes that have recovered
      and take no further part in the epidemic.

Looking at the :class:`SIR` documentation, the process takes three parameters:

   - :attr:`SIR.P_INFECT`, the probability thaat an infected node will infect
     a given susceptible neighbour;
   - :attr:`SIR.P_REMOVE`, the probability that an infected node will recover; and
   - :attr:`SIR.P_INFECTED`, the probability a node starts the simulation infected.

A single simulation experiment consists of setting these three parameters and providing
an initial network over which to run the SIR process. The simulator will then run the
process and return its results.

We can choose the parameters as appropriate by providing a dictionary of them:

.. code-block:: python

    from epydemic import *

    param = dict()
    param[SIR.P_INFECT] = 0.1
    param[SIR.P_REMOVE] = 0.5
    param[SIR.P_INFECTED] = 0.01

We can run the simulation over any appropriate network. A network whose degree distribution
followed a :ref:`powerlaw with cutoff <model-human-population>` would probably be most
realistic, but for now we'll just use an ER random graph model:

.. code-block:: python

    import networkx

    N = 10000    # order (number of nodes) of the network
    kmean = 5    # mean degree

    g = networkx.erdos_renyi_graph(N, (kmean + 0.0) / N)

We can now perform a single run of the simulation, using :term:`stochastic dynamics`:

.. code-block:: python

    m = SIR()                      # the model (process) to simulate
    e = StochasticDynamics(m, g)   # use stochastic (Gillespie) dynamics

    rc = e.set(param).run()

If for some reason we wanted to use synchronous dynamics, we'd simply replace the
simulation dynamics framework:

.. code-block:: python

    f = SynchronousDynamics(m, g)   # same model works in both frameworks
    rc = f.set(param).run()

We can re-run the simulation, with or without changing the parameters:

.. code-block:: python

    e.run()                       # re-run with the same parameters

    param[SIR.P_REMOVE] = 1.0     # change something and re-run
    e.set(param).run()

We can also change the network:

.. code-block:: python

    h = networkx.erdos_renyi_graph(N * 2, (kmean + 0.0) / (N * 2))
    e.setNetwork(h)
    e.run()


