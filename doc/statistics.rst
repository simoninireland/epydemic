:class:`NetworkStatistics`: A process to collect summary statistics
===================================================================

.. currentmodule:: epydemic

.. autoclass:: NetworkStatistics

A statistics process is intended to be composed with another process, for
which it collects a common set of summary network statistics. This allows
standart statistics to be collected from any ``epydemic`` process.

The statistics gathered are:

- The order of the network (number of nodes)
- The number of edges
- The mean degree of nodes
- The degree histogram
- The number of connected components
- The number of nodes in the largest connected component
- The number of nodes in the second-largest connected component

The process runs in the results-gathering phase, where is analyses the topology
and features of the final network.


Results
-------

.. autoattribute :: NetworkStatistics.N

.. autoattribute :: NetworkStatistics.M

.. autoattribute :: NetworkStatistics.KMEAN

.. autoattribute :: NetworkStatistics.KDIST

.. autoattribute :: NetworkStatistics.COMPONENTS

.. autoattribute :: NetworkStatistics.LCC

.. autoattribute :: NetworkStatistics.SLCC


Building the process
--------------------

.. automethod :: NetworkStatistics.results




