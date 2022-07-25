.. _subclassing:

.. currentmodule:: epydemic

Defining more new processes
===========================

So now we can build a disease process from scratch. This is the
simplest way of defining a new process, as a direct sub-class of
:class:`CompartmentedModel`, but there are two other ways we might use
instead:

- By adding compartments to an existing model
- By adding state to an existing model
- By computing extra results
- By composing processes together

Each of these starting points has subtleties, and we'll explore all
but the last here. (The last is the subject of the :ref:`next chapter
<process-composition>`.)

(In exceptional circumstances one might need to avoid the process
hierarchy entirely and create new kinds of experiment. This can be
done by sub-classing :class:`NetworkExperiment`.)


New compartmented models
------------------------

A new disease model is easy to build, as we :ref:`saw <build-sir>`,
especially if you have a description of it in terms of
compartments. It's usually just a matter of overriding
:meth:`Process.build` to define the new compartments and add
appropriate rules for each :term:`event`, and then define a
:term:`event function` implementing the actions of each.


Adding more compartments
------------------------

Let's consider a variant of SIR called SIRS, where someone can become
susceptible again after some time. (This models diseases where the
immunity given by infection is time-bounded.)  Again, we'll define a
slightly simplied version of ``epydemic``'s built-in :class:`SIRS`
process.

For SIRS we need to add three things to SIR:

- another parameter, the probability of becoming susceptible again;
- a locus tracking the R nodes so they can be the target of
  re-susceptibility events; and
- the code for this event.

We can bring these three elements together in a sub-class:

.. code-block:: python

  class SIRS(SIR):
    # Extra model parameter
    P_RESUSCEPT = 'pResuscept'    #: Parameter for probability of losing immunity

    # Event name
    RESUSCEPT = 'RS'              #: Compartment/event name for returning to susceptible.

    def __init__(self):
	super().__init__()

    def build(self, params):
	super().build(params)

	# add components needed for SIRS
	pResuscept = params[self.P_RESUSCEPT]
	self.trackNodesInCompartment(self.REMOVED)

	self.addEventPerElement(self.REMOVED, pResuscept, self.resuscept, self.RESUSCEPT)

    def resuscept(self, t, n):
	self.changeCompartment(n, self.SUSCEPTIBLE)

From what we've seen already this is hopefully quite clear. The new
sub-class builds on :class:`SIR`, adding to its :meth:`SIR.build`
method to track nodes in the removed compartment and add an event with
the probability given by the experimental parameter. The code for this
event simply changes the node's compartment back to susceptible.

.. note ::

    You can see the code for the SIRS process
    `here <https://raw.githubusercontent.com/simoninireland/epydemic/master/epydemic/sirs_model.py>`_.


Adding more state
-----------------

A process over a network will typically want to save state on each
node and/or edge> For a :class:`CompartmentedModel` this includes
things like the compartment a node is in
(:attr:`CompartmentedModel.COMPARTMENT`), which is accessed using the
:meth:`CompartmenntModel.getCompartment` method.

Defining new state means providing two things: a name for the state,
as an attribute key for the nodes or edges; and getter and setter
methods that access the attribute.

Defining a name for the state is slightly more complicated that just
picking a meaningful name, because of the ways ``epydemic`` lets you
combine processes: we have to ensure that two processes running on the
same network at the same time don't interfere in unwanted ways. The
easiest approach is to make state names unique to a particular process
instance, which is what :meth:`Process.stateVariable` does. For
example, the initialisation of :class:`CompartmentedModel` defines
some state for compartments as follows:

.. code-block:: python

    # Placeholders for model state variables
    COMPARTMENT: str = None               #: State variable holding a node's compartment.
    OCCUPIED: str = None                  #: State variable that's True for occupied edges.
    T_OCCUPIED: str = None                #: State variable holding the occupation time of an edge.
    T_HITTING: str = None                 #: State variable holding the infection time of a node.

    def __init__(self):
	super().__init__()
	self._compartments = dict()       # compartment -> initial probability
	self._effects = dict()            # compartment -> event handlers

	# state variable tags
	self.COMPARTMENT = self.stateVariable('compartment')
	self.OCCUPIED = self.stateVariable('occupied')
	self.T_OCCUPIED = self.stateVariable('tOccupied')
	self.T_HITTING = self.stateVariable('tHitting')

(We define placeholders for the variable names as a place to hang
their documentation.) Code can use ``COMPARTMENT`` as if it was a
constant -- which it is, but a constant *unique to this instance*. The
actual constants can anyway then be hidden by accessor methods, for
example:

.. code-block:: python

    def setCompartment(self, n, c):
	'''Set the compartment of a node. This assumes that the node doesn't
	already have a compartment set, and so should be used only for
	initialising new nodes: in all other cases, use
	:meth:`changeCompartment`.

	:param n: the node
	:param c: the new compartment for the node'''
	g = self.network()

	# set the correct node attribute
	g.nodes[n][self.COMPARTMENT] = c

	# propagate the change to any other compartments
	self._callEnterHandlers(n, c)

    def getCompartment(self, n):
	'''Return the compartment of a node.

	:param n: the node
	:returns: its compartment'''
	return self.network().nodes[n][self.COMPARTMENT]

The advantage of this approach is that two different compartmented
model processes -- for example a disease and an opinion model -- can
be run together over the same network without one model's state
interfering with the other's. Essentially the model states of
different processes live in separate namespaces, but without any
additional overhead.
