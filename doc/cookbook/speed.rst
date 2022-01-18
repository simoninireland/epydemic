.. _speed:

.. currentmodule:: epydemic

Improving execution times
=========================

**Problem**: You're trying to work with ``epydemic`` and it's *sooo sloooooow*.

**Solution**: Welcome to scientific computing. Speed is always a problem.

``epydemic`` is a Python library. The advantages of using Python are
ease of programming, ease of integration, and the availability of lots
of libraries (including ``epydemic``) that can massively reduce the
amount of programming effort required to address a problem. Using it
is "standing on the shoulders of giants" in the code space, just as we
do in science.

The *disadvantage* of Python is that it's an interpreted language,
meaning that it's slow relative to languages like C, C++, or Fortran,
that might otherwise be used for scientific computing. Some
measurements suggest that Python is about 100x *slower*
than C. Essentially you trade-off speed of development and integration
against speed of experimental execution.

This having been said, there are definitely ways of speeding-up your
use of ``epydemic``.


Don't be too ambitious
^^^^^^^^^^^^^^^^^^^^^^

``epydemic`` will happily deal with processes over networks of the
order of :math:`N = 10^5` nodes, and can stretch in many cases to
:math:`10^6` nodes. However, bear in mind that a lot of network
algorithms have poor time complexity: they often scale linearly with
the number of edges, which is :math:`O(N^2)` in the number of nodes,
and even the more well-behaved ones seldom drop below :math:`O(N)`.
This mean that the move to :math:`10^7` nodes may be painful,
especially if you also want to do lots of repetitions.

Having said that, the most important internal data structures within
``epydemic`` (which are the loci of nodes and edges at which events
happen) have :math:`O(\log N)` operations, which helps keep things
linear. See :ref:`implementation-challenges` for a longer discussion.


Use PyPy
^^^^^^^^

The `PyPy project <https://pypy.org>`_ describes itself as "a fast,
compliant alternative implementation of Python". It uses a number of
alternative approaches to compiling Python code that claim to make a
4.4x improvement in speed. Our experience with running ``epydemic`` on
PyPy suggests around a 5x speedup over "normal" Python, which is well
worth having.

Note however that PyPy is a work in progress and doesn't support all
Python libraries -- and annoyingly this includes ``matplotlib``, which
means you can't have a single program that both simulates an epidemic
and generates the graphs of the results. You may be able to split the work
by having two programs linked through a common :ref:`lab notebook
<epyc:labnotebook-class>`, but this makes coding (and more especially
code maintenance) more delicate. It also doesn't play well with Jupyter.

The easiest way of using PyPy is to build a virtual environment and
then run your ``epydemic`` code in that.


Use a multicore workstation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most modern workstations (and indeed many laptops) are
multicore. Since ``epydemic`` uses :doc:`epyc <epyc:index>` for
experimental management, you can use :ref:`epyc:parallellab-class`
that will make use of the cores you have available. If you have a
16-core machine you might get a (somewhat less than) 16x performance
improvement this way.

The use of multicore *doesn't* speed up individual simulations:
they're all single-threaded. But it *does* mean that multiple
simulations can run simultaneously.


Use a compute cluster
^^^^^^^^^^^^^^^^^^^^^

The use of :doc:`epyc <epyc:index>` means that ``epydemic`` can run the same
experiment in parallel on a compute cluster, using
:ref:`epyc:clusterlab-class`.  Again, this doesn't speed up each
individual experiment but does allow multiple experiments to run
simultaneously -- and since we're often doing lots of repetitions of
experiments, this is a useful way of getting speedup overall.
