.. _implementation-multiple-instances:

.. currentmodule:: epydemic

Multiple instances of processes
===============================

..  versionadded:: 1.14.1

   Versions of ``epydemic`` prior to 1.14.1 only support a single
   instance of a process within a simulation. Supporting multiple
   instances led to the changes in parameter and result handling
   described here.

Multiple diseases circulating in a population, whether simultaneously
or one after the other, are an important area of research. The several
"diseases" might be different, or might represent variants of same
underlying illness; they might be independent of each other, or might
exhibit complete cross-immunity (having had one disease prevents you
from getting another), some lesser immunity, or even make infection
with another disease *more* likely. The richness of possible models
makes it important that we can build them by composing simpler models,
letting us focus on the interactions rather than the mechanics.

``epydemic`` supports multiple instances of a process within a single
simulation. This means that (for example) a simulation wanting to have
two circulating SIR-style infections can simply create two instances
of :class:`SIR` and run them together.

It's a bit more complicated that that, though. Both instances of the
process would need to get their parameters from a single parameter
dict, and both would expect the same basic parameter names (such as
:attr:`SIR.P_INFECT` for the probability of infection). We need a way
to specify *separate* parameters for each instance.

In order to support multiple instances we make two small extensions.
The first is to optionally associate names with processes ("first
disease" and "second disease", for example), and use these names to
decorate parameter names to show which instance they belong with. This
would clearly be unwieldy to do manually, so we also add functions to
get and set parameters *en masse* for a given process. So if a process
named "first disease" requests a parameter called "A" by calling
:meth:`Process.getParameters` it will first look for a parameter called
"A@first disease"; if this parameter doesn't exist in the parameter
dict it will fall back on a parameter called "A". (This lets instances
share some parameters.)

The parameters can be set using the corresponding
:meth:`Process.setParameters`, which decorates the parameter names
with the instance names of the process it's called on.

:meth:`Process.getParameters` should be used in the
:meth:`Process.build` and :meth:`Process.setUp` methods of all
processes that might be multiply instanciated -- which is probably all
of them. All the standard processes in ``epydemic`` use this style and
so are safe to multiply instanciate.

:meth:`Process.decoratedNameInInstance` can be used to decorate a
parameter or result name, for exaple when accessing columns in a
``DataFrame`` created from results.

Decoration is performed using the :meth:`Process.decoratedName` and
:meth:`Process.undecoratedName` methods, which add and remove
decorations respectively.
