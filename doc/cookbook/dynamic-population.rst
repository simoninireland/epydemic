.. _dynamic-population:

.. currentmodule:: epydemic

An epidemic over a changing population
======================================

**Problem**: You want to simulate an epidemic in a population that has a
"background" level of birth and death, unconnected to the disease.

**Solution**: ``epydemic`` has the building blocks we need for this
scenario: a compartmented model and an addition-deletion process. We
just have to make them work together.

Python multiple inheritance is the mechanism for this, in the same way
as we can include :ref:`monitoring <monitoring-progress>` to any process.
The basic structure will therefore be to create a new process that combines
the compartmented model we want with the addition-deletion process, and then
set all the parameters that the two processes need. Suppose we choose our
favourite :class:`SIR` model. We'd then have a class definition that lools something like:

.. code-block :: python

    class DynamicSIR(epydemic.SIR, epydemic.AddDelete):

	def __init__(self):
	    super(DynamicSIR, self).__init__()

So far so good.

However, let's think about the processes involved here. The compartmented SIR
model starts by putting nodes into the :attr:`SIR.SUSCEPTIBLE` compartment, and
then changing the compartment as the epidemic spreads. This setting of the initial
compartment happens in :meth:`SIR.build` when we set the initial probabilities
of nodes being in the :attr:`SIR.SUSCEPTIBLE` or :attr:`SIR.INFECTED` compartments.
(The actual assignment of nodes to compartments happens in :meth:`CompartmentedModel.initialCompartments`
which is called as part of the setup procedure.)

Now let's turn to the addition-deletion process. :class:`AddDelete` builds
fixed-rate events that add and delete nodes, independently of any other
process running at the same time. But while these events are independent in terms
of their occurrence, they're *not* independent in terms of their interaction with
the compartmented model. When we add a node we need to decide what compartment
it's going to be placed in; when wee delete a node we need to take account of what
effects that has on the infection of other nodes. This suggests that we can't simply
combine the two classes together and expect them to work out of the box: there's
some missing functionality.

(Another way to think about this is that the base processes provide the independent
parts of the scenario, and we have to encode the parts of the scenario in which they
communicate with each other.)

The issue is what happens when nodes are added and removed. These functions are
provided by two methods, :meth:`Process.addNode` and :meth:`Process.removeNode`. by
default these methods just do what you'd expect, affecting the underlying network the
process is running over. :class:`AddDelete` overrides both these methods
(:meth:`AddDelete:addNode` and :meth:`AddDelete.removeNode`), and also
defines another, :meth:`AddDelete.addNewNode`, that creates a new node with a new
name.

To define how :class:`SIR` and :class:`AddDelete` work together, then, we need to
extend the methods where the interaction occurs. Let's suppose we've decided that
all added nodes will be marked as :attr:`SIR.SUSCEPTIBLE`, and that all deleted nodes
will just disappear. We can code this up by adding two methods to our class definition:

.. code-block :: python

    def addNewNode(self, **kwds):
	'''Mark new nodes as susceptible.

	:param kwds: (optional) node attributes'''

	# add the node, cepturing its name
	n = super(DynamicSIR, self).addNewNode(*kwds)

	# set the compartment of this node to susceptible
	self.setCompartment(n, epydemic.SIR.SUSCEPTIBLE)

	# return the name of the new node
	return n

    def removeNode(self, n):
	'''Mark any node as removed before deleting.

	:param n: the node'''

	# change the node's compartment to removed
	self.changeCompartment(n, epydemic.SIR.REMOVED)

	# delete the node
	super(DynamicSIR, self).removeNode(n)

(Note that when adding a node we used :meth:`CompartmentModel.setCompartment` because
the newly-added node didn't have a compartment, whereas when deleting a
node we used and not :meth:`CompartmentedModel.changeCompartment` because it did.)

The :meth:`AddDelete.add` and :meth:`AddDelete.delete` events will now use these
overridden methods, and will inform the compartmented model when new susceptible
nodes appear and when nodes are deleted.


Keeping the numbers straight
----------------------------

You might have noticed that we've been a bit fast and loose with how we delete
nodes in this solution. We communicate to the :class:`SIR` process that the node is
no longer part of the process by setting its compartment to :attr:`SIR.REMOVED`, just
as would happen if it recovered (or died) as part of the epidemic. But if you're interested
in the actual numbers who die naturally *versus* those who die (or whatever) from
the disease, then this muddles these numbers up by aggregating the two causes together.

The easiest way to deal with this is with an extended model that
has an extra compartment ("D" for "died"?) into which to place deleted nodes. We
can do this in one of three ways:

1. Extend :class:`SIR` and add a new compartment in the sub-class;
2. Write another compartmented model that *only* has this compartment, and no
   events, and add it into the mix using multiple inheritance; or
3. Extend :meth:`AddDelete.build` to add the new compartment.

Which of these is the "correct" approach depends on context. In any case there's
an interaction between the addition-deletion process and the compartmented model
process that's requiring extra code. At one level the solution you choose doesn't
matter, because the interactions all go through an API and any extra results that
you obtain land in the results dict alongside the other values.
