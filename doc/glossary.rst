.. _glossary:

Glossary
========

.. currentmodule:: epydemic
		   
.. glossary::

   addition-deletion process
      A process that adds and removes nodes from a network. The usual
      model (due to :ref:`Moore et alia <MGN06>`) adds nodes at a
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
      course of the simulation. See :ref:`Hethcote <Het00>` for a survey,
   
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

   Gillespie simulation
      A simulation technique developed initially for *ab initio*
      chemistry simulations ref:`Gil76`ref:`Gil77`
      
   locus
      A "place" at which dynamics can occur, that is to say, where
      nodes can change compartments and any other tasks can happen.
      Each :term:`event` is associated with a particular locus: the 
      locus contains the set of nodes or edges to which the event may
      be applied, while the event defines chat happens.

   posted event
      An :term:`event` posted for a definite future time. The
      :term:`process dynamics` will execute the posted events at the
      appropriate time
      
   process dynamics
      The simulation approach used, which selects how and when each
      :term:`event` fires. Process dynamics execute events in time
      order from two possible sources: a random distribution that
      chooses an event based on their relative probability or rate; and
      any :term:`posted event` that has been scheduled.

   SIS
      A :term:`compartmented model of disease` where nodes go from being
      Susceptible to the disease, to Infected and able to infect others,
      and then recover back to Susceptible.

   SIR
      A :term:`compartmented model of disease` where nodes go from being
      Susceptible to the disease, to Infected and able to infect others,
      and are then Removed and take no further part in the dynamics.

   stochastic process
      A process whose exact progression is determined by random
      variables drawn from particular probability distributions.

   stochastic dynamics
      Also known as Gillespie dynamics, this :term:`process dynamics` operates
      in :term:`continuous time` with one event occurring at each time
      point.

   synchronous dynamics
      A :term:`process dynamics` using :term:`discrete time`, where a
      simulation passes through a sequence of discrete timesteps which
      may include several (or no) events happening.

      
