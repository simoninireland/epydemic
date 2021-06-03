.. _keep-network:

.. currentmodule:: epydemic

Keeping access to the network
=============================

**Problem**: You decide that you want to explore the network at the
end of an experiment. You therefore do something like this:

.. code-block:: python

   m = epydemic.SIR()
   e = epydemic.StochasticDynamics(m, epydemic.ERNetwork))
   rc = r.set(params).run()

   g = m.network()

And you discover that g is :code:`None`. This happens even if you
create a network outside the experiment and set it explicitly.

**Solution**: This is actually a deliberate feature, albeit one that
can be annoying.

``epydemic`` is designed to make experiments self-contained. The
reason for this is that they can then be run at scale, possibly on
remote computers, without needing to ship lots of data around. We
therefore package the experiment, and the local analysis of its
results and end state, into a class (possibly built with multiple
inheritance, for decomposition and re-use). Because of this, we take
care to spin-up and tear-down experiments cleanly, and this extends to
the management of the working network.

An ``epydemic`` experiment maintains a working network over a single
run. This is created either from a prototype network, or from a
:term:`network generator`, one of which is supplied experiment's
constructor or set with a call to
:meth:`NetworkExperiment.setNetworkGenerator`. The working network is
created in :meth:`NetworkExperiment.setUp` and destroyed in
:meth:`NetworkExperiment.tearDown`. It means that a single experiment
can be run (and re-run) on a new instance of the underlying
class of networks.

This approach makes sense at large scales: it makes less sense for
small-scale development, and especially when first developing an
experiment when you might want to do more exploratory analysis
locally. In that case, the tear-down behaviour is quite awkward.

For local experiments, then, it might be worth capturing the working
network in the process object, for example by extending
:meth:`Process.results`:

.. code-block:: python

   def results(self):
      # grab the underlying results
      res = super().results()

      # grab the final network state
      self._finalNetwork = self.network().copy()

      # return the results
      return res

The end-state network is now in :code:`m._finalNetwork` for
analysis. This works because results are created *after* the body of
the experiment but *before* tear-down. You could even put this
behaviour into a class on its own, and then include it using multiple
inheritance with whatever process you're defining, or as part of a
:class:`ProcessSequence`.

This approach only works locally and at small scale, though. If run
remotely, the instance variable holding the final network won't be
available; if you re-run the experiment, the final network is
overwritten. You can solve both these problems, of course -- but at
the cost of holding a *lot* of (potentially) large networks
around. For this reason it's far better to package-up and automate
analysis wherever possible.
