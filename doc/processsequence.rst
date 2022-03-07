:class:`ProcessSequence`: A process built from other processes
===============================================================

.. currentmodule:: epydemic

.. autoclass:: ProcessSequence
   :show-inheritance:


Building the process
--------------------

The process sequence essentially just composes the methods of the individual
component processes at each phase of the process' lifecycle.

.. automethod:: ProcessSequence.reset

.. automethod:: ProcessSequence.build

.. automethod:: ProcessSequence.setUp

.. automethod:: ProcessSequence.tearDown

.. automethod:: ProcessSequence.results


Equilibrium and termination
---------------------------

The default implementations work on timeouts respected across all the
component processes. They can be re-defined to provide different equilibrium
detection overall.

.. automethod:: ProcessSequence.atEquilibrium

.. automethod:: ProcessSequence.setMaximumTime

.. automethod:: ProcessSequence.maximumTime


Anonymous and non-anonymous sequences
-------------------------------------

Process sequences are built from smaller *component* processes passed
in the constructor. In most cases these processes are anonymous and
constructed from a list, and there's no way to refer to each component
process individually. This is the best way as it maximises the
independence of process code.

.. note::

   Versions of ``epydemic`` prior to version 1.9.1 had only anonymous
   process sequences.

There are however some complicated cases where one component needs
access to another. A good example of this is combining
addition-deletion and disease processes, where the addition operation
needs to affect the compartment of new nodes. In that case, one
process needs to be able to access the methods on another.

A non-anonymous process sequence is created using a dict from
component process names (strings) to component processes. There are no
default names, for maximum flexibility. One component process can then
refer to another by using its name, by first using
:meth:`Process.container` to acquire its container and then looking-up
the required component process.

.. automethod:: ProcessSequence.processes

.. automethod:: ProcessSequence.processNames

.. automethod:: ProcessSequence.get

.. automethod:: ProcessSequence.__getitem__

.. note::

   See the cookbook recipe :ref:`dynamic-population` for an extended
   example of using process sequences in different ways.
