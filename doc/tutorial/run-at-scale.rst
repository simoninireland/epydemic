.. _run-at-scale:

.. currentmodule:: epydemic

Running a simulation at scale
=============================

On important thing about epidemic simulation is that both the networks and the processes that run
across them are typically stochastic: they have components that are inherently random. To study the
structure of these processes we therefore typically need to perform multiple repetitions of simulations
with the same parameter values so as to squeeze-out variance in the results that comes from chance
interactions between processes and network. (As a simple, if unlikely, example, consider the case
where the network consists of two components with only a single edge between them and all the infected
nodes start in one of the components. It's likely that the epidemic will die out without crossing
into the other component. (A less extreme example of the same thing is
studied by Shai and Dobson :cite:`CoupledAdaptive-13`.)


Run the epidemic
----------------

To run the epidemic, we need to provide the dynamics with the
parameters that the disease model needs. The dynamics is actually an
``epyc`` :ref:`experiment <epyc:experiment-class>`, so we provide the
parameters as a dict.

We can build a dict giving values to these three parameters:

.. code-block:: python

   import epyc

   param = dict()
   m.setParameters(param, {SIR.P_INFECT: 0.1,
			   SIR.P_REMOVE: 0.05,
			   SIR.P_INFECTED: 0.01})

To run the simulation, we first call the ``set()`` method on the
dynamics object to set the disease parameters, and then call the
``run()`` method:

.. code-block:: python

   rc = e.set(params).run()

Time passes....


Get the results
---------------

When the simulation run finishes we are returned a dict of dicts holding the experimental results and some
metadata. If we concentrate just on the experimental results:

.. code-block:: python

   rc[epyc.Experiment.RESULTS]

we'll see something like this:

.. code-block:: python

   {''I': 0, 'S': 9821, 'R': 110}

What does this mean? The dict holds the sizes of the three SIR
compartments, susceptible (``S``, also known as
:attr:`SIR.SUSCEPTIBLE`), infected (``I``), and removed (``R``). What
this result shows is that we have no nodes in the infected compartment
(the epidemic has died out, and no-one else can be infected); 9821
nodes still in the susceptible compartment who have never been
infected; and 110 nodes who had the disease and have recovered (or
been removed) from it.


Re-running the epidemic
-----------------------

But wait! -- is this the whole story? Well clearly not, because a
disease is a stochastic process depending on random factors. Another
epidemic with the *same* parameters on the *same* network might
generate a *different* result.

We can check this by re-running the experiment again:

.. code-block:: python

   (e.run())[epyc.Experiment.RESULTS]

Notice that we didn't have to re-set the parameters: the experiment
just re-used the ones already set. Looking at the results we might
see:

.. code-block:: python

  {'I': 0, 'S': 9807, 'R': 124}

Slightly more nodes were infected this time and therefore ended up
removed (124 in the ``R`` compartment). If we ran the process again,
we could see a different result again: the results could all be
similar, or might possibly show some dramatic variation such as not
having anyone at all becoming infected other than those who initially
were.


Larger scale: explore infection rates
-------------------------------------

It would clearly be tedious and error-prone to perform lots of
repetiions by hand, and even more so if we wanted to see, for example,
whether changing the infection probability made a
difference. Fortunately, because ``epydemic`` uses ``epyc`` to manage
its execution, we can use ``epyc``'s :ref:`Lab <epyc:lab-class>` class
to automate the process.

Let's run a larger experiment, performing repeated simulations for
several different infection values. Without getting caught up in how
``epyc`` works (there's a whole :doc:`web site <epyc:index>` for
that), we can just jump straight in:

.. code-block:: python

   import numpy

   # create a notebook for results and a lab in which to run the experiments
   nb = epyc.JSONLabNotebook('sir-experiments.json')
   lab = epyc.Lab(nb)

   # build the parameter space, where P_INFECT ranges from 0.01 to 1.0 in 10 steps
   lab[epydemic.SIR.P_INFECTED] = 0.01
   lab[epydemic.SIR.P_INFECT] = numpy.linspace(0.01, 1.0, num=10, endpoint=True)
   lab[epydemic.SIR.P_REMOVE] = 0.05

   # run 5 repetitions of the experiment at each point in the parameter space
   lab.runExperiment(eypc.RepeatedExperiment(e, 5))

Significantly more time passes -- unsurprisingly, since we're doing 50
experimental runs (5 repetitions at each of 10 points in the parameter
space, varying the infection probability each time). We can then
retrieve all the results and import them directly into ``pandas`` for
analysis:

.. code-block:: python

   import pandas

   df = lab.dataframe()

You'll see the results of the experiments loaded into this DataFrame,
including the sizes of compartments, along with the experimental
parameters that gave rise to those results anmd some other metadata
about the simulation.


Even larger scale: parallelism
------------------------------

What if we want to go larger again? -- say 100 points and 1000
repetitions? That's clearly a *lot* more computation: 100,000
experimental runs. That's a lot to do in a sequential fashion, but
fortunately ``epydemic`` (or more accurately ``epyc``) comes to our
aid.

Suppose we have a 32-core workstation. This means we can run up to 32
processes simultaneously, and we can make use of this parallelism to
run simulations in parallel. Each simulation still takes the same
amount of time to run, but we run lots of them together. This can buy
some speed-up.

We probably don't want to use all 32 cores, as that'll soak up *all*
the available computing power and possibly leave us locked-out of our
own machine! Instead we can, for example, leave 2 cores for everything
else and consume the rest for our simulations.

.. code-block:: python

   pnb = epyc.JSONLabNotebook('more-sir-experiments.json')
   plab = epyc.ParallelLab(nb, cores=-2)

   plab[epydemic.SIR.P_INFECTED] = 0.01
   plab[epydemic.SIR.P_INFECT] = numpy.linspace(0.01, 1.0, num=100, endpoint=True)
   plab[epydemic.SIR.P_REMOVE] = 0.05

   plab.runExperiment(eypc.RepeatedExperiment(e, 1000))

That's it! The code of the simulation stays the same. We said
``cores=-2``, which translates as "all but 2 of the cores" -- 30 in
our case -- so 30 experiments run in parallel.

This might *still* not be fast enough, but ``epyc`` can also make use
of a compute cluster if you have one available. See
:ref:`epyc:second-tutorial` for a lot more information on setting up
and using compute clusters: once you've done this, ``epydemic`` can
(with a few scant exceptions) use it without any changes in the
processes or other code. We've used ``epydemic`` on clusters with
around 180 cores without any problems, which gives significant
speed-up as well as letting you walk away and do other things while
your code's running .
