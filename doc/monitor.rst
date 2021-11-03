:class:`Monitor`: A process to monitor other processes
======================================================

.. currentmodule:: epydemic

.. autoclass:: Monitor

A monitor process is intended to be composed with another process on
which it collects data as the process progresses. This allows
monitoring to be added automatically to any ``epydemic`` process

The monitor works by periodically running an observation event,
defined by :meth:`observe` (which may be overridden or extended). The
cookbook contains an article on :ref:`monitoring-progress`.


Parameters
----------

.. autoattribute:: Monitor.DELTA


Results
-------

:class:`Monitor` stores its results as time series, one (tagged with
:attr:`Monitor.OBSERVATIONS`) holding the simulation times, and then
one for each locus in the model holding the size of the locus at each
sample time. (All these time series therefore have the same length.)

The names of the time series for the loci are derived from the locus
names.

.. automethod:: Monitor.timeSeriesForLocus

.. autoattribute:: Monitor.OBSERVATIONS


Building the process
--------------------

.. automethod:: Monitor.reset

.. automethod:: Monitor.build

.. automethod:: Monitor.results


Events
------

.. automethod:: Monitor.observe


Running the process
--------------------

.. automethod:: Monitor.atEquilibrium
