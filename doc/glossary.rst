.. _glossary:

Glossary
========

.. currentmodule:: epydemic
		   
.. glossary::

   compartments
      The possible dynamical states in a :term:`compartmented model of disease`.
   
   compartmented model of disease
      A disease model that represents the progression of a disease as
      a set of discrete compartments with transitions possible
      between them. Transitions typically occur with some base
      probability, which might be fixed or might vary across the
      course of the simulation. See :ref:`Hethcote <Het00>` for a survey,
   
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

   locus
      A "place" at which dynamics can occur, that is to say, where
      nodes can change compartments and any other tasks can happen.
      Each :term:`event` is associated with a particular locus: the 
      locus contains the set of nodes or edges to which the event may
      be applied, while the event defines chat happens.
   
   stochastic process
      A process whose exact progression is determined by random
      variables drawn from particular probability distributions.

   stochastic dynamics
      Also known as Gillespie dynamics, this process dynamics operates
      in :term:`continuous time` with one event occurring at each time
      point.

   synchronous dynamics
      A process dynamics using :term:`discrete time`, where a
      simulation passes through a sequence of discrete timesteps which
      may include several (or no) events happening.

      
