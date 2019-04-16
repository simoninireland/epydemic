---
title: 'epydemic': Epidemic networks simulation in Python
tags:
  - network science
  - epidemic spreading
authors:
  - name: Simon Dobson
    orcid: 0000-0001-9633-2103
    affiliation: 1
affiliations:
  - name: School of Computer Science, University of St Andrews UK
    index: 1
date: 16 April 2019
---

# Summary

``epydemic`` is a library for performing reproducible simulations of
epidemic and other processes over complex networks. It provides
simulation under synchronous and stochastic (Gillespie) dynamics,
using the well-known ``networkx`` package to represent and manipulate
networks. It supports a generic model for compartmented models of
disease with several standard models provided and which can be
extended to other, more complex, diseases. It also supports other
network processes such as addition-deletion networks.

``epydemic`` is built on top of the ``epyc`` experiment management library,
allowing simulations to be conducted at scale on individual machines,
multicore machines, and parallel computing clusters.


