.. _subclassing:

.. currentmodule:: epydemic

Defining new processes
======================

Defining a new process is simply a matter of sub-classing the relevant
base class. There are three likely places to start:

- A new disease model -- probably subclass one of :class:`SIR`,
  :class:`SIS`, or :class:`SEIR`
- A new compartmented model unrelated to these -- sub-class
  :class:`CompartmentedModel`
- An entirely new process -- sub-class :class:`Process`

Each of these three starting points has subtleties, things it's best to
understand before starting.

(In exceptional circumstances one might need to avoid the process
hierarchy entirely and create new kinds of experiment. This can be
done by sub-classing :class:`NetworkExperiment`.)


New compartmented models
------------------------

A new disease model is easy to build, especially if you have a
description of it in terms of compartments. It's usually just a matter
of overriding :meth:`Process.build` to define the new compartments and
add appropriate rules for each :term:`event`, and then define a
:term:`event function` implementing the actions of each.


Additional state
----------------

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
	self._compartments: Dict[str, float] = dict()         # compartment -> initial probability
	self._effects: Dict[str, List[Handlers]] = dict()     # compartment -> event handlers

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

    def setCompartment(self, n: Node, c: str):
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

    def getCompartment(self, n: Node) -> str:
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
