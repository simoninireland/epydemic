.. _glossary:

Glossary
========

.. currentmodule:: epydemic

.. glossary::

   addition-deletion process
      A :term:`process` that adds and removes nodes from a network. The usual
      model :cite:`AdditionDeletionNetworks` adds nodes at a
      constant rate and with constant degree, removes nodes randomly
      at a constant rate, and connects new nodes to existing nodes according
      to some probabilistic attachment kernel.

   compartments
      The possible dynamical states in a :term:`compartmented model of disease`.

   compartmented model of disease
      A disease model that represents the progression of a disease as
      a set of discrete compartments with transitions possible
      between them. Transitions typically occur with some base
      probability, which might be fixed or might vary across the
      course of the simulation. See Hethcote :cite:`Hethcote-CompartmentedModels` for a survey,

   contact tree
      The way in which individuals were infected during thhe infection.
      Each node is an infected individual, with edges representing the
      individuals that individual infected.

      While it's common talk of a
      contact *tree*, this will only be the case if there is an identifiable
      "patient zero" from whom all infections arise. In the more general case
      of multiple people initially infected, the contact tree will actually
      be a contact *forest* of multiple independent trees, each one rooted
      at an initially-infected individual.

   continuous time
      A simulation mode in which events occur at unique times
      represented by real numbers. No two events ever happen
      simultaneously, but they can be separated by an arbitrarily
      small interval. Continuous-time simulations can be made
      statistically exact and run faster for situations in which there
      are long periods where no events occur.

   degree distribution
      The way in which the numbers of neighbours each node has
      varies. The most basic measure of network topology. More
      precisely, the degree distribution is the probability
      :math:`p_k` that a node chosen at random from the network will
      have degree :math:`k`, for all values of :math:`k`.

   discrete time
      A simulation mode in which time progresses in single integer
      timesteps. During each timestep a collection of events can
      occur. Discrete-time simulations can be easier to code and
      understand.

   dynamical state
      The state of a node or edge at some point in the
      simulation. These typically reflect the :term:`compartments`
      of the simulation, but may be more complex and
      comprise a vector of information.

   event
      A simulation event that changes the state of the underlying
      network or simulation. Events can occur in :term:`continuous
      time` or :term:`discrete time`.

   event function
      A function called when an :term:`event` fires to perform the
      action required. Event functions take three arguments: the
      current simulation time and the element at which
      the event occurs (which will be selected by the chosen
      :term:`process dynamics`). Elements are typically either nodes
      or edges, depending in the :term:`locus` at which the event
      occurs.

   generating functions
      A mathematical tool for working with entire
      probability distributions, often used in network science
      research because of its flexibility. They're often used when
      describing the :term:`degree distribution` of a network. See
      Newman *et alia* :cite:`ArbitraryDegreeDistributions` for a
      network science introduction and Wilf
      :cite:`generatingfunctionology` for a more detailed treatment.

   giant connected component
      In :term:`percolation` (and other) processes, the giant
      connected component (sometimes called the GCC, or simply "the
      giant component") is a connected component that occupies a
      substantial fraction of the network: basically the GCC forms
      when the size of the :term:`largest connected component` is
      "very large". The formal definition of when a component becomes
      giant is quite complicated; the common working definition is
      that the LCC is "giant" when it includes more that a
      hundredth of the network's nodes
      :cite:`PercolationSmearedPhaseTransition`.

   Gillespie simulation
      A simulation technique developed initially for *ab initio*
      chemistry simulations :cite:`Gillespie76,Gillespie77`.

   largest connected component The largest collection of nodes in the
      network linked by edges. Often called the LCC, and sometimes
      called the :term:`giant connected component`. In some cases we
      may also be interested in the sizes of other components: for
      example the second-largest connected component (SLCC) can give
      useful information.

   locus
      A "place" at which dynamics can occur, that is to say, where
      nodes can change compartments and any other tasks can happen.
      Each :term:`event` is associated with a particular locus: the
      locus contains the set of nodes or edges to which the event may
      be applied, while the event defines what happens. ALl loci
      are derived from the :class:`Locus` class.

   network generator
      A process that samples a class of random networks to create an
      instance. A typical example is the class of networks with Poisson
      degree distribution (the ER networks), defined by the order and
      mean degree of the network.

   percolation
      A process that randomly "occupies" nodes or edges in a
      network with a given probability.

   percolation threshold
      The occupation probability in a percolation process above which
      a :term:`giant connected component` forms. The size of the GCC
      rises rapidly once the threshold is passed, making the
      threshold generally "crisp".

   posted event
      An :term:`event` posted for a definite future time. The
      :term:`process dynamics` will execute the posted events at the
      appropriate time

   process
      A system that associates a state vector with each node (and
      possibly edge) in a network, and describes how they evolve over
      time.

   process dynamics
      The simulation approach used, which selects how and when each
      :term:`event` fires. Process dynamics execute events in time
      order from two possible sources: a random distribution that
      chooses an event based on their relative probability or rate; and
      any :term:`posted event` that has been scheduled.

   SEIR
      A :term:`compartmented model of disease` where nodes are Exposed
      to the disease and become infectious for a period before moving
      to being Infected. This can be used to model pre-symptomatic
      infectivity.

   SIS
      A :term:`compartmented model of disease` where nodes go from being
      Susceptible to the disease, to Infected and able to infect others,
      and then recover back to Susceptible.

   SIR
      A :term:`compartmented model of disease` where nodes go from being
      Susceptible to the disease, to Infected and able to infect others,
      and are then Removed and take no further part in the dynamics.

   stochastic event
      An :term:`event` whose occurrence is determined by a
      probability distribution. In a  :term:`compartmented model of
      disease`, for example, the passage of an infection over an edge
      is a stochastic event, the rate and location of which are
      determined according to the distribution of infections.

   stochastic process
      A :term:`process` whose exact progression is determined by random
      variables drawn from particular probability distributions.

   stochastic dynamics
      Also known as Gillespie dynamics, this :term:`process dynamics` operates
      in :term:`continuous time` with one event occurring at each time
      point.

   synchronisation
      A :term:`process` that places an oscillator on each node in a
      network and allow them to interact. In many cases the intention
      is to have the oscillators converge to a common phase; this can
      be difficult to achieve, and gives rise to a huge set of
      interesting possible dynamics.

   synchronous dynamics
      A :term:`process dynamics` using :term:`discrete time`, where a
      simulation passes through a sequence of discrete timesteps which
      may include several (or no) events happening.
