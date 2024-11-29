.. _coinfection:

.. currentmodule:: epydemic

Studying several diseases in a single population
================================================

**Problem**: You're interested in how diseases co-exist and co-infect
within a single population, for example because you want to introduce
several variants of a disease.

**Solution**: You need to run several instances of the *same* process with
*different* parameters in the *same* simulation.

.. note::

   Multiple instances have only been supported in ``epydemic`` since
   version 1.14.1.

The approach is conceptually simple. We define disease models, or use
built-in ones like SIR. Instead of a single process we introduce two
(or more) and run them over the same population. Or maybe we set
things up so that one disease starts after the other has had time to
get going.

But there's a problem: the processes take the same parameters an
produce the same results! How can we provide *different* values for
the parameters?


Named instances, parameters, and results
----------------------------------------

``epydemic`` solves this by allowing process instances to be *named*.
The instance names can then used to *decorate* parameter names and
result names. This means that two processes whose definitions both (for
example) use :attr:`SIR.P_INFECT` will, when named and run together,
look for parameters with names decorated with their instance names.

``epydemic`` provides functions for writing the parameters into the
parameter dict in a way that respects the process instance names.
Within a process definition similar functions can be used to extract
parameters. In fact it's a little more flexible than this: a process
with an instance name will look for a parameter decorated with its
name and, if it fails to find one, will fall back on a parameter with
the name undecorated. This lets process instances share some parameters
while having different values for others.

(The same technique can also be used when returning results.)


Running two diseases with common removal rate
---------------------------------------------

For example let's run an experiment consisting of two SIR processes
with the same removal rate but different infection rates:

.. code-block:: python

    params = dict()

    # network
    N = 10000
    kmean = 100
    params[ERNetwork.N] = N
    params[ERNetwork.KMEAN] = kmean

    # first infection
    p1 = SIR("Disease1")
    p1.setParameters(params,
		     {SIR.P_INFECT: 0.1,
		      SIR.P_INFECTED: 5.0 / N
		      })

    # second infection
    p2 = SIR("Disease2")
    p2.setParameters(params,
		     {SIR.P_INFECT: 0.3,
		      SIR.P_INFECTED: 5.0 / N
		      })

    # common removal rate
    params[SIR.P_REMOVE] = 0.005

    # run the processes together
    ps = ProcessSequence([p1, p2])
    e = StochasticDynamics(ps, ERNetwork())
    rc = e.set(params).run(fatal=True)

The usual parameters dict is used to store the network topology
information in the usual way. We create the first SIR process, but
give it the name "Disease1" and then use :meth:`Process.setParameters`
to set its infection and initially infected parameters. We then do
similarly with the second process, named "Disease2". The parameters
actually stored will be decorated with the process names: you can see
this is you print the keys in the dict.

The processes also need a removal rate parameter. We could set this
per-process as above, but for this example we'll set it undecorated so
that it'll be picked up by *both* instances.

We then place both instances into a :class:`ProcessSequence` and run
them using the normal dynamics. The results dict returned will contain
the overall results, which in this case are as defined by
:class:`CompartmentedModel` containing the final sizes of the
compartments.


Variations
----------

What if we wanted something different? We could override the
:meth:`Process.results` method to capture per-process results, using
:meth:`Process.setResults` to store them into the process' results
dict. This would decorate any result names, of course, and we could
use :meth:`Process.getResults` to retrieve them for each process.

For larger datasets we might want to access the results from within a
``DataFrame``. In that case the columns will be named using decorated
names, and we can use :meth:`Process.decoratedNameInInstance` to
construct the decorated name of a given result from a given instance.

There are obviously more complicated setups. For example, in the above
example there are two processes but only three compartments: the
compartments don't distinguish between diseases. If we wanted to study
things more closely we'd need to capture who had which disease, and it
might be the case that having had one disease only *partially
immunises* an individual from getting the second disease -- or indeed
might make them *more* susceptible! In that case we'd probably need
to add compartments (perhaps decorating the compartment names according
to process instance), changing the loci and events accordingly to
account for the different probabilities in play. Adding a third
disease would clearly make things more complicated still. The point is
that we can hopefully build this complicated case from simpler
elements, focusing on only the things that *make* it complicated
compared to the simpler cases.
