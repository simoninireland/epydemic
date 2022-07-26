:class:`SIR_VariableInfection`: SIR with per-edge infectivity
=============================================================

.. currentmodule:: epydemic

.. autoclass:: SIR_VariableInfection


Different parameters and additional node attributes
---------------------------------------------------

There is no use for the :attr:`SIR.P_INFECT` parameter: instead the
infection probability of each edge is set by
:meth:`SIR_VariableInfection.initialInfectivities`. The value assigned
to each edge is stored in an edge property

.. autoattribute:: SIR_VariableInfection.INFECTIVITY


Building the model
------------------

.. automethod:: SIR_VariableInfection.build

.. automethod:: SIR_VariableInfection.setUp

.. automethod:: SIR_VariableInfection.initialInfectivities


The event distribution
----------------------

To allow the :class:`Dynamics` to access the infection events defined
per-edge we construct an event distribution at each time point. This
takes any events associated directly with loci (such as those
for removal) and adds an event per edge with the given probability.

.. automethod:: SIR_VariableInfection.perElementEventDistribution
