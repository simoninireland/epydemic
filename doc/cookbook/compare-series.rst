.. _timeseries:

.. currentmodule:: epydemic

Comparing series data
=====================

**Problem**: You collect a time series for a compartment in a
:class:`CompartmentedModel` using :class:`Monitor`, or some other
series data. You then want to compare these series between different
experimental runs, or find the mean of several series. How do you
wrangle the data into a form that can be worked with?

**Solution**: This is really a ``pandas`` question, but one that's
extremely common in network science and so relevant to ``epydemic``.

The issue is that time series land in a result set as arrays. This
makes them hard to manipulate. What we would probably prefer is a
DataFrame whose rows are the series and whose columns are the
observation times, degrees, or whatever: extracting a sub-set of rows
from the original result set DataFrame and then re-formatting them
into a more suitable shape.

Fortunately ``pandas`` provides exactly the function we need. It can
create a DataFrame from a list of lists, and we can then rename the
columns to be meaningful.

As an example, suppose we've used :class:`Monitor` to capture the
progression of an :class:`SIR` epidemic:

.. code-block:: python

   lab[BANetwork.N] = int(1e5)
   lab[BANetwork.M] = 6
   lab[SIR.P_INFECTED = 0.01
   lab[SIR.P_INFECT] = 0.1
   lab[SIR.P_REMOVE] = 0.01
   lab[Monitor.DELTA] = 1
   lab['repetitions'] = range(100)

   e = StochasticDynamics(ProcessSequence([SIR(), Monitor()]), BANetwork())
   lab.runExperiment(e)

This will result in a result set with result columns that capture the
size of each locus in the SIR model -- the SI edges and I nodes --
over time. We can retrieve the column name of the time series for the
I locus by:

.. code-block:: python

   c = Monitor.timeSeriesForLocus(SIR.INFECTED)

If we extract the result set for this experiment it will have 100 rows
(one per repetition), and we can project-out just the time series
using:

.. code-block:: python

   df = lab.dataframe()
   tss = df[Monitor.timeSeriesForLocus(SIR.INFECTED)]

Then each row will have a single column: not quite what we wanted, so
now we need to "explode" this list-like column into a row in itself:
