.. _use-standard-model:

.. currentmodule:: epydemic

Running a process
=================

The easiest way to understand how ``epydemic`` works is to use one of
the in-built disease processes to perform a simulation. After that
we'll look at :ref:`how to run large-scale simulations <run-at-scale>`
and how to :ref:`build disease models from scratch <build-sir>`.

We first need to import the basic classes.

.. code-block:: python

   from epydemic import SIR, StochasticDynamics, ERNetwork


Providing parameters
--------------------

All ``epydemic``'s processes take a range of parameters and
use them when building the model. These are provided as a dict, with
the contents depending on the model we'll be building. Continuing with
the SIR process, we need to provide three paremeters for the infection
probability, the removal probability, and the initial seeding
probability.

.. code-block:: python

    param = dict()
    param[SIR.P_INFECT] = 0.1        # the probability of infection
    param[SIR.P_REMOVE] = 0.5        # the probability of removal
    param[SIR.P_INFECTED] = 0.01     # the random fraction of nodes initially infected


Providing a network
-------------------

We can run the simulation over any appropriate network. A network
whose degree distribution followed a :ref:`powerlaw with cutoff
<model-human-population>` would probably be most realistic, but for
now we'll just use an ER random graph model.

.. code-block:: python

    param[ERNetwork.N] = 10000             # order (number of nodes) of the network
    param[ERNetwork.KMEAN]= 5              # mean node degree


Running the simulation
----------------------

We can now perform a single run of the simulation, using :term:`stochastic dynamics`.

.. code-block:: python

    # create a model and a dynamics to run it
    m = SIR()                      # the model (process) to simulate
    g = ERNetwork()                # network generator for ER networks
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
    rc = e.set(param).run()


Retrieving results
------------------

The ``run`` method returns a dict of results. The structure of this
dict is defined by ``epyc``, and is described :ref:`here
<epyc:results-experiment>`: for our purposes, we will simply see a
nested dict with the results of the experiment appearing in a dict
under the ``epyc.Experiment.RESULTS`` key.

The experimental resuilts are constructed by the
:meth:`Process.results` method. This is overridden by
:meth:`CompartmentedModel.results` to contain a mapping from
compartments to the number of nodes in that compartment at the end of
the simulation. Sub-classes can override the method further to add
more results.

This is all that's needed to define a run individual simulations of
networked processes. There are additional methods and event types that
can be used in other circumstances, which we explore in
:ref:`advanced-topics`. It is also common to want to run simulations
that explore the ways in which a process changes across a range of
parameters, which we discuss under :ref:`run-at-scale`.
