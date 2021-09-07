---
title: 'epydemic: Epidemic network simulation in Python'
tags:
  - Python
  - network science
  - complex networks
  - epidemic spreading
authors:
  - name: Simon Dobson
	orcid: 0000-0001-9633-2103
	affiliation: 1
affiliations:
  - name: School of Computer Science, University of St Andrews UK
	index: 1
date: 6 September 2021
bibliography: paper.bib
---

# Summary

``epydemic`` is a library for performing reproducible simulations of
epidemic (and other processes) over complex networks. The goal is to
reduce the learning curve for network science and provide a stable,
re-usable framework for network science simulations that allows
reproducible and portable experiments, integrated into the wider
Python and [Jupyter](https://jupyter.org/) ecosystems that are
increasingly common for computational science.


# Statement of Need


# Features

It provides
simulation under synchronous and stochastic (Gillespie) dynamics,
using the well-known ``networkx`` package to represent and manipulate
networks. It supports a generic model for compartmented models of
disease with several standard models provided and which can be
extended to other, more complex, diseases. It also supports other
network processes such as addition-deletion networks.

``epydemic`` is built on top of the
[``epyc``](https://epyc.readthedocs.io/en/latest/) experiment
management library, allowing simulations to be conducted at scale on
individual machines, multicore machines, and parallel computing
clusters.


# Main applications


# Compatibility and availability


# References
