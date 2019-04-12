.. epydemic documentation master file, created by
   sphinx-quickstart on Mon Jun 12 20:20:38 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

epydemic: Epidemic simulations on networks in Python
====================================================

Vision: A common platform for epidemic simulation
--------------------------------------------------

``epydemic`` aims to provide a common framework for the scalable and efficient simulation of epidemic processes.


What are epidemics?
-------------------

Many common processes can be treated as epidemic, where some condition spreads between the nodes
of a network. The most familiar example is a transmissible disease such as flu, where un-infected
people become infected through contact with infceted people. Mathematically the population of
people form a network (or graph), where the nodes represent people and the edges represent
possible contacts between them. An epidemic begins when one or more person is initially infected
and begins to spread the disease to his neighbours with some probability. Depending on factors such
as the way the network is connected, the probability of a contact giving rise to an infection,
the rate at which people recover from the illness and so forth, the disease may come to infect
none, some, or all of the people.

It turns out that a lot of interesting processes work mathematically like epidemics. As well as diseases,
these include the spread of computer viruses, the spread of rumours on social media (or in the real world),
the spread of genetic mutations, and even how soils drain.

Simulating epidemic processes is therefore something a lot of people want to do frequently. However, the
actual process of setting up and simulating an epidemic is complicated, and this is especially true when
we want to do lots of repetitions of experiments to explore how different parameters affect the way an
epidemic behaves.


What is ``epydemic``?
-------------------

``epydemic`` is a simulation framework for epidemic processes. It aims to provide the common simulation
approaches used in the scientific literature, together with a small set of "common epidemics" that can
form the basis for experimentation. ``epydemic`` is built on top of `epyc <https://epyc.readthedocs.io/en/latest/index.html>`_,
an experiment management package that handles running different simulations, either on a single machine or in the cloud.


Current features
----------------

* Compatible with both Python 2.7 and Python 3.7 and later, as well as with PyPy

* Supports both discrete-time :term:`synchronous dynamics` and continuous-time
  :term:`stochastic dynamics` (Gillespie simulation)

* All details of network processes encapsulated in a single class

* Uses ``networkx`` for representing disease networks, allowing random networks to be generated easily and
  real networks to be imported from outside sources

* Support for a generic :term:`compartmented model of disease`, allowing
  more complex diseases to be described

* Susceptible-Infected-Removed (:term:`SIR`) and Susceptible-Infected-Susceptible (:term:`SIS`) models
  built-in, with either stochastic or fixed recovery times

* Addition-deletion process to model natural birth and death

* Integrated with ``epyc``'s labs and experiments, including execution in parallel
  on compute clusters for doing simulations at scale


.. toctree::
   :hidden:

   install
   start
   reference
   cookbook
   glossary
   bibliography


