.. _standard-gfs:

Standard generating functions
=============================

.. currentmodule:: epydemic.gf

The most common use for generating functions in network science is to
describe degree distributions. There are generating functions that
reflect to standard network generators provided by ``epydemic``.

.. autofunction:: gf_er

.. autofunction:: gf_powerlaw

.. warning::

   In versions of ``epydemic`` prior to 1.8.1 :func:`gf_powerlaw` was called
   ``gf_ba``.

.. autofunction:: gf_plc
