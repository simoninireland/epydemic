.. _r-to-probability:

.. currentmodule:: epydemic

Modelling epidemics with real-world data
========================================

**Problem**: You are an epidemiologist or public health worker. You
have obtained data on :math:`\mathcal{R}` and other parameters and
want to use `epydemic` to model the disease -- but then discover that
it needs things like infection probability rather than the data you
have available.

**Solution**: The relationship between the  :math:`\mathcal{R}` number
and the probabilities involved in simulation can be modelled in
several ways, depending on the degree of accuracy you want.

:math:`\mathcal{R}` is defined as the average number of secondary
infections that arise from every new infection. It's probably the
easiest parameter to understand in the disease dynamics. It actually
forms a critical point -- what a mathematician would called a
**separatrix** -- between two possible regimes of epidemic
evolution. If :math:`\mathcal{R} < 1` then the current "generation" of
infected individuals gives rise to fewer infected individuals in the
next generation, and so (if this is sustained for enough generations)
the epidemic will die out; conversely, if :math:`\mathcal{R} > 1` the
next generation will be larger, and the disease will become epidemic.

:math:`\mathcal{R}` will change over time both as a result of the
population becoming gradually immune (if this happens with the disease
model in question), and as a result of countermeasures that seek to`
reduce infection. (Both of these effects are explored experimentally
by Dobson :cite:`em`.) At the very start of an epidemic we have the
disease spreading without immunity (in what epidemiologists refer to
as a **naive population**), and we speak of :math:`\mathcal{R}` at this
point as :math:`\mathcal{R}_0` -- :math:`\mathcal{R}` at time
:math:`t = 0`.

A :term:`compartmented model of disease` is described by dynamical
parameters concerning the way the disease spreads at each contact. For
:term:`SIR` these parameters are the probability that a contact leads
to infection (:math:`\beta`) and the probability that an infected
individual recovers (:math:`\alpha`). In disease models that use
differential equations as their basis, we can define

.. math::

   \mathcal{R} = \frac{\beta}{\alpha}

So :math:`\mathcal{R}` is simply the ratio of the rate of infection to
the rate of recovery. This means the actual choices of numbers for
:math:`\beta` and :math:`\alpha` aren't important in themselves, only
their relationship to each other, so we could set :math:`\alpha = 1`,
use this to set :math:`\beta = \mathcal{R}`, and get a simulation of
the measured disease.

However, this takes no account of the network over which infections
are spreading, and we would expect, in a realistic model, that (for
example) infected individuals with a large number of contacts spread
the disease more effectively than those with only a small number. This
means we should expect the :term:`degree distribution` (and possibly
other topological parameters) to appear in our calculations.

Let's change notation slightly and define :math:`T` to be the
**transmissibility** of the disease, defined by
:math:`\frac{\beta}{\alpha}`. This is purely a disease-level value,
taking no account of the network. We should be able then to express
:math:`\mathcal{R}` in terms of :math:`T` and the network's topology.

Choose a node at random and infect it. If we take the view that we
will choose an "average" node, we expect it to have the average number
of neighbours (which we denote :math:`\langle k \rangle`), and this
node will infect a fraction :math:`\beta` of those neighbours in the
time until it recovers. The expected average recovery time is
:math:`\frac{1}{\alpha}`, and so we have that

.. math::

   \mathcal{R}_0 = T \langle k \rangle

This is known as the **mean field solution** of the epidemic
equations: it assumes that every node behaves like the average
node. Again it gives us a route to define :math:`\beta` and
:math:`\alpha` given that we know both :math:`\mathcal{R}` (from
measurements of the disease) and :math:`\langle k \rangle` (from
measurements of the network).

The mean field is clearly a strong assumption to make in networks
where the degree distribution is not normal. We can account for these
effects by taking account of higher moments of the degree
distribution, for example:

.. math::

   \mathcal{R}_0 = T \frac{\langle k^2 \rangle - \langle k \rangle}{\langle k \rangle}

where :math:`\langle k^2 \rangle` is the variance of the degree
distribution. Again, we measure the topological parameters of the
network and use them to compute the probabilities.

There are a few observations we can make here. The first is that the maximum
number of people that an infected node can infect is bounded by its
degree, :math:`\langle k \rangle` on average. Secondly, the higher
moments of the distribution limit this still further. In order for
there to be an epidemic we need :math:`\mathcal{R} > 1`. To get this
from the last equation implies a threshold

.. math::

   T = \frac{\langle k \rangle}{\langle k^2 \rangle - \langle k \rangle}

which is the **epidemic threshold** for the network, often denotes
:math:`\phi_c`: below this no epidemic will take hold. This is known
as the **Molloy-Reed criterion** :cite:`MolloyReed` for
epidemics to spread on networks.

The third observation pertains to the second. If we have

.. math::

   \phi_c= \frac{\langle k \rangle}{\langle k^2 \rangle - \langle k \rangle}

then if :math:`\langle k^2 \rangle` is very large then :math:`\phi_c`
will be very small: there will be an epidemic even for very small
transmissibilities. Indeed, in the limit of :math:`\langle k^2 \rangle
\rightarrow \infty` it will be that :mAth:`\phi_c \rightarrow 0`. It
so happens that networks with powerlaw degree distributions do indeed
have such infinite variance, and powerlaw networks with a cutoff
(which are used as models of human populations) often have very high
variances, which implies that such networks will be very susceptible
to epidemic outbreaks. (The network science community captures this
with the saying that "powerlaw networks always percolate".)

This has been a long answer to what seems like a straightforward
question about the relationship between measurements collected in the
field for "real" epidemics and their simulation on networks. In
general we can say that we need to account for *both* disease *and*
network characteristics when building a simulation intended to model a
real disease. But the disease we've measured is *itself* spreading
over a network of individuals in the real world -- which is a network
we can't directly observe, measure, or control very precisely. In other
words we have a lot of work to do to determine what disease parameters
are actually in play.
