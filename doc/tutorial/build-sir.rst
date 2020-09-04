.. _build-sir:

.. currentmodule:: epydemic

Building a compartmented model
==============================

The easiest way to understand how ``epydemic`` works is to build an epidemic model
from scratch, which is what we'll do here. We'll build the SIR process, the most commonly-used
experimental starting point for epidemic spreading processes: if you're inteersted in ``epydemic`` you're
almost certainly acquainted with SIR.

For anyone who isn't: the Susceptible-Infected-Removed (SIR) model represents an epidemic as
a process where nodes in a network represent individuals and edges represent interactions between
them. Each individual is labelled with one of three states:

- **S**: the individual is susceptible to the disease;
- **I**: the individual is infected with the disease, and can infect any susceptible neighbour; and
- **R**: the individual has recovered (or died) and takes no further part in the simulation.

This structure is called a :term:`compartmented model of disease`: the states of individuals are referred
to conventionally as *compartments*. Questions about the epidemic are often phrased in terms of the
asymptotic behaviour of the process: in the limit, when the process reaches equilibrium, what proportion
of nodes are in which compartment? For an epidemic to *be* an epidemic, this usually means getting a large
number of nodes in the **R** compartment, meaning they've been infected and have been removed.

A simulation of SIR consists of:

- taking a network;
- seeding it with infected individuals;
- setting the probability with which infected nodes infect neighbouring susceptibles;
- setting the probability with which infected noides recover spontaneously; and
- running the simulation until equilibrium, for example when there are no infected nodes left
  or a long time has passed.

A moment's thought will show that there are lots of possible variations to this basic process,
for example where the infection probability changes with time, or the network is re-wired as the
epidemic progresses. For this reason it's worth understanding SIR *ab initio*. What follows is a walk-through
of the code in ``epydemic``'s standard :class:`SIR` model.


Getting started
---------------

Let's start defining a class to represent the model. This will be a sub-class of :class:`CompartmentedModel`,
which is itself a sub-class of :class:`Process`, the class of network processes.

.. code-block:: python

    from epydemic import CompartmentedModel

    class SIR(epydemic.CompartmentedModel):

We then need to populate this class with the  elements needed to define a compartmented model.

.. note ::

    The rest of the code on this page is part of this `SIR` class, and so needs to
    be indented within the scope of the ``class`` definition in proper Python style.

The compartments
----------------

The SIR model has three compartments, so the first part of the model is to define these. We could simply name
them using their initial letters, but it's better practice to define constants in the class to represent them.

.. code-block:: python

    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    REMOVED = 'R'


The transition probabilities
----------------------------

Next we need to be able to specify the transition probabilities that form the dynamics. There are two such
parameters: the probability of the infection passing across a link between a susceptible and an infected node,
the the probability of an infected node being removed.

We also need to specify the probability of a node being initially infected. Essentially this is the probability
that a node starts out in the ``SIR.INFECTED`` compartment rather than in the ``SIR.SUSCEPTIBLE``  compartment, and
will be used to seed the network randomly at the start of the simulation.

.. code-block:: python

    # the model parameters
    P_INFECTED = 'pInfected'
    P_INFECT = 'pInfect'
    P_REMOVE = 'pRemove'

Note that these aren't the parameters themselves, they're the *name* of parameters that will be supplied when the
model is run.


Loci
----

Now we come to a slightly more complicated topic. Where does the process occur? The description above suggests that
changes happen in two places:

- on the edges beteeen susceptible and infected noides (where the infection may pass from the latter to
  the former); and
- on the infected nodes themselves (which may become removed).

In the latter case, the process occurs to nodes in a specific compartment; in the former, it occurs on edges
between nodes in specific compartments. We need to keep track of where these changes can happen, which is the
function of loci: we'll return to these in a minute. For the time being, note that we conventionally refer to the
edges where the infection process can occur as *SI edges* -- edges between a node in the S compartment and a node
in the I compartment -- and so we'll define two loci: one can just be called ``SIR.INFECTED``, but the other
needs to be given a name.

.. code-block:: python

    # the edges at which dynamics can occur
    SI = 'SI'


Building the model
------------------

We can now build the model ready for simulation.  There are four elements to this:

1. Collect the parameters we need, which are passed to us in a dict.
2. Create the compartments.
3. Create the loci that track the nodes and edges we need to perform actions on.
4. Define the events we want to happen to nodes or edges at these loci.

The code to do this is:

.. code-block:: python

    def build( self, params ):
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)
        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)

        self.trackNodesInCompartment(self.INFECTED)
        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)

        self.addEventPerElement(self.SI, pInfect, self.infect)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove)

We first grab the parameters by name from the parameters dict. We then declare the three compartments by calling
:meth:`CompartmentedModel.addCompartment`, which takes a compartment name and the initial probability that a node
will randomly be placed in that compartment. The parameter ``pInfected`` (named ``SIR.P_INFECTED``) gives the
probability of a node initially being infected (in the ``SIR.INFECTED`` compartment, and since no nodes start off
in the ``SIR.REMOVED`` compartment (probability ``0.0``), the probability of nodes being ``SIR.SUSCEPTIBLE`` is ``1 - pInfected``.

We then declare that we want to track the I nodes and the SI edges, and create two loci to do this. The first
gets named ``SIR.INFECTED`` by default; the second is given an explicit name. ``SIR.SI`` (a name will be created
if none is given). The methods :meth:`CompartmentedModel.trackNodesInCompartment` and
:meth:`CompartmentedModel.trackEdgesBetweenCompartment` each create an return a :class:`Locus`, essentially a
set of nodes of edges (with some supporting methods that we'll ignore for now).

Finally, we add events to the loci. These are per-element events, which occur with the gibven probability to
each event in the locus. We provide to :meth:`Process.addPerElementEvent` the locus at which the event occurs,
the probability with which it occurs, which we retreieved from the experimental parameters), and the
:term:`event function` that is called when the event happens. The event functions are methods that we'll now
define.


Events
------

Finally, we define the events that happen as part of the process.

.. code-block:: python

    def infect( self, t, e ):
        (n, m) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)

    def remove( self, t, n ):
        self.changeCompartment(n, self.REMOVED)

Both event functions are passed the current simulation time and
the element on which the event should occur, drawn from the locus to which the event is attached.

For the ``infect`` event, the element is an edge (because the event occurs on SI edges). We extract the endpoints
of the edge by pattern-matching. Since the locus is defined as holding edges between a node in the ``SIR.SUSCEPTIBLE``
compartment and a node in the ``SIR.INFECTED`` compartment, we will be passed edges with this orientation: we can
assume that ``n`` above is a susceptible node. We use :meth:`CompartmentedModel.changeCompartment` to change the
compartment of ``n`` to ``SIR.INFECTED``: the compartment of ``m`` doesn't change (it stays infected). We also
mark the edge as one that the infection travsersed using :meth:`CompartmentedModel.markOccupied` (the "occupied"
terminology is slightly uninformative but is standard in the literature, coming from percolation theory).

For the ``remove`` event, which happens at infected nodes, the element will be a node, and we simply change
its compartment to ``SIR.REMOVED``.

.. note ::

    This code is the same as ``epydemic``'s built-in SIR process. You can see the code
    `here <https://raw.githubusercontent.com/simoninireland/epydemic/master/epydemic/sir_model.py>`_.

This finishes the definition of the disease process. We can now move on to :ref:`use-standard-model`.