:class:`SIvR`: SIR with vaccination
===================================

.. currentmodule:: epydemic

.. autoclass:: SIvR


Parameters
----------

The SIvR process extends the parameters of SIR with two new parameters:

.. autoattribute:: SIvR.EFFICACY

.. autoattribute:: SIvR.T_OFFSET


Loci
----

SIvR defines two additional loci:

.. autoattribute:: SIvR.INFECTED_N

.. autoattribute:: SIvR.INFECTED_V

These loci don't directly affect the dynamics, but they track the
sub-populations of the :attr:`SIR:INFECTED` locus who are
(un)vaccinated. This can be useful for reporting using
:class:`Monitor`, when the sizes of these sub-populations will be
captured.


Helper method
-------------

SIvR defines additional "helper" methods that can be used to
vaccinate a node, recording its vaccination status and time. This then
feeds into how infections happen and the recording of (un)vaccinated
sub-populations of the infected.

.. automethod:: SIvR.vaccinateNode

Note that, when a node is removed (recovers from the disease) their
vaccination status and time is retained, and so can be used in
analysis.

.. automethod:: SIvR.nodeVaccinated

.. automethod:: SIvR.nodeVaccinatedAt


Building the model
------------------

.. automethod:: SIvR.build


Event methods
-------------

.. automethod:: SIvR.infect

.. automethod:: SIvR.remove
