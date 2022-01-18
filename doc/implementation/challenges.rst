.. _implementation-challenges:

.. currentmodule:: epydemic

Major implementation challenges
===============================

Network science simulation is a compute-intensive task. The expense comes from
three different sources:

- the overheads from using Python;
- the cost of running a single simulation over a possibly large network; and
- the cost of running multiple repetitios of simulations to reduce the
  variance of results.

Using Python is simply a decision to use a language that's easier to
write than (for example) C or C++, and easier to integrate with other
tools, but that inevitably runs more slowly. Essentially this decision
is to prioritise programmer time at the cost of runtime. This does
make speed an issue, though, as Python is often two orders of
magnitude slower to run than the equivalent C or C++ program (although
it's often two orders of magnitude (or more) quicker to write and
debug).

Making single simulations as fast as possible involves avoiding those
operations which are inherently slower. Many network operations have
computational complexities of :math:`O(N)` or :math:`O(N^2)` when done
naively: careful design can sometimes reduce this to :math:`O(1)` or
:math:`O(\langle k \rangle)`. ``epydemic`` has a number of situations
where these sorts of trade-offs occur. A good example is the use of
the :class:`Locus` to keep running track of sets of nodes or edges,
rather than extracting them from the network at each timestep (or
event).

A more subtle situation occurs with core data structures, whose
performance (and more significantly their computational complexity) is
critical to the performance overall. Several data structures have been
re-designed when profiling has shown them to be bottlenecks.  The
:class:`Locus` uses a specially-coded balanced binary tree so as to
support efficient random drawing of an element from a set of nodes or
edges -- an operation that can happen hundreds of thousands of times
within a single simulation run.

The cost of running multiple simulations reduced by using parallelism,
and this is why ``epydemic`` is built on top of ``epyc``, a library
for managing computational experiments on multicore systems and
workstaion clusters. ``epyc`` handles a lot of the housekeeping needed
in starting, monitoring, and collating the results of a lot of
simalutions.
