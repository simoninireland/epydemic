:class:`Monitor`: A process to monitor other processes
======================================================

.. currentmodule:: epydemic

.. autoclass:: Monitor

A monitor process is intended to be composed with another process on which it collects
data as the process progresses. This allows monitoring to be added automatically to
any ``epydemic`` process

The monitor works by periodically running an observation event, defined by 
:meth:`observe` (which may be overridden or extended). The cookbook
contains an article on :ref:`monitoring-progress`.


Parameters
----------

.. autoattribute:: Monitor.DELTA


Results
-------

.. autoattribute:: Monitor.TIMESERIES

.. autoattribute:: Monitor.OBSERVATIONS


Events
------

.. automethod:: Monitor.observe


Building the process
--------------------

.. automethod:: Monitor.reset

.. automethod:: Monitor.build

.. automethod:: Monitor.results




