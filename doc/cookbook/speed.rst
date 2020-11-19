.. _speed:

.. currentmodule:: epydemic

Improving execution times
=========================

**Problem**: You're trying to work with ``epydemic`` and it's *sooo sloooooow*. 

**Solution**: Welcome to scientific computing. Speed is always a problem.

``epydemic`` is a Python library. The advantage of using Python are ease of programming,
ease of integration, and the availability of lots of libraries (including ``epydemic``) that
can massively reduce the amount of programming effort required to address a problem. Using
is "standing on the shoulders of giants" in the code space, just as we do in science.

The *disadvantage* of Python is that it's an interpreted language, meaning that it's slow
relative to languages like C, C++, or Fortran, that might otherwise be used for scientific
computing. Some measurements suggest that Python is about 100x *slower* than C. Essentially
you trade-off speed of development and integration against speed of experimental execution.

This having been said, there are definitely ways of speeding-up your use of ``epydemic``:

*Don't be too ambitious*. ``epydemic`` will happily deal with processes over networks of the order
of :math:`10^5` nodes. However, bear in mind that a lot of network algorithms are of
polynomial-time complexity, meaning that the move to :math:`10^6` nodes may be painful,
especially if you also want to do lots of repetitions.

*Use PyPy*. The `PyPy project <https://pypy.org>`_ describes itself as "a fast, compliant
alternative implementation of Python". It uses a number of alternative approaches to compiling
Python code that claim to make a 4.4x improvement in speed. Our experience with running
``epydemic`` on PyPy suggests around a 5x speedup over "normal" Python, which is well worth
having.

The easiest way of using PyPy is to build a virtual environment and then run your ``epydemic``
code in that.

*Use a compute cluster*. The use of ``epyc`` means that ``epydemic`` can run the
same experiment in parallel on a compute cluster. This doesn't speed up each individual
experiment, but it allows multiple experiments to run simultaneously -- and since we're often
doing lots of repetitions of experiments, this is a useful way of getting speedup overall.
Of course using PyPy as well gets dual benefits: faster individual experimemts *and*
lots of experiments running at one time.



