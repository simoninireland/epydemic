:class:`ProcessSequence`: A process built from other processes
===============================================================

.. currentmodule :: epydemic

.. autoclass :: ProcessSequence
   :show-inheritance:


Building the process
--------------------

The process sequence essentially just composes the methods of the individual
component processes at each phase of the process' lifecycle.

.. automethod :: ProcessSequence.reset

.. automethod :: ProcessSequence.build

.. automethod :: ProcessSequence.setUp

.. automethod :: ProcessSequence.tearDown

.. automethod :: ProcessSequence.results


Equilibrium and termination
---------------------------

The default implementations work on timeouts respected across all the
component processes. They can be re-defined to provide different equilibrium
detection overall.

.. automethod :: ProcessSequence.atEquilibrium

.. automethod :: ProcessSequence.setMaximumTime

.. automethod :: ProcessSequence.maximumTime





