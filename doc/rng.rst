.. _rng:

Random number generation
========================

``epydemic`` provides a central reference point for the random number
generator (RNG) being used by the simulator, ``epydemic.rng``. This is
simply an instance of a ``numpy`` random number generator, and by
default is simply the result of ``numpy.random.default_rng()``.

All the core classes in ``epydemic`` use this object as their source
of random numbers, and it's usually appropriate to use it in any
extensions. The reason for this is to allow the RNG to be changed
uniformly across a simulation.

Why might you want to do this? It might be that you want to use a
specific random number generator for some reason: perhaps you have
extreme requirements for your random numbers. In that case any random
bit generator can be encapsulated within an instance of
``numpy.random.Generator`` and used across ``epydemic``. Then assign
this new generator to ``epydemic.rng`` to have it picked up by all the
objects.

Another reason that's sometimes put forward is to *reduce* randomness,
for example using a generator with a known seed that thereafter
produces the *same* stream of "random" numbers. This is sometimes
argued for as a way to replicate computational experiments, and it
works ... kind of. Tempting as it may sound, there are good reasons to
avoid obsessing about the reproducibility of individual samples:

1. Reproducibility relies on the "random" number stream being consumed
   in exactly the same way. This isn't guaranteed: for example
   ``epydemic`` might iterate across a set in each different run, and
   the iteration order of Python sets isn't guaranteed.
2. The idea that exact reproduction is necessary in these kinds of
   experiments is flawed. Because the processes are stochastic, we're
   interested in ensuring that each sample run is drawn from the set
   of possible outcomes (which is an issue for unit testing, amongst
   other things). We're also interested in ensuring that the variance
   in these samples is squeezed-out (which is an issue of averaging).
   Given these two properties, it should be the case that, while
   individual samples differ, the statistical properties of large
   *sets* of samples are the same. This is a lot more important and
   convincing than the reproducibility of individual samples.

We therefore think that the default global RNG will be sufficient in
the vast majority of cases.
