# Makefile for epydemic
#
# Copyright (C) 2017--2020 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

# The name of our package on PyPi
PACKAGENAME = epydemic

# The version we're building
VERSION = 1.0.1


# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
SOURCES_SDIST = dist/$(PACKAGENAME)-$(VERSION).tar.gz
SOURCES_WHEEL = dist/$(PACKAGENAME)-$(VERSION)-py2-py3-none-any.whl
SOURCES_CODE = \
	epydemic/__init__.py \
	epydemic/networkdynamics.py \
	epydemic/synchronousdynamics.py \
	epydemic/stochasticdynamics.py \
	epydemic/loci.py \
	epydemic/process.py \
	epydemic/compartmentedmodel.py \
	epydemic/sir_model.py \
	epydemic/sir_model_fixed_recovery.py \
	epydemic/sis_model.py \
	epydemic/sis_model_fixed_recovery.py \
	epydemic/sirs_model.py \
	epydemic/adddelete.py

SOURCES_TESTS = \
	test/__init__.py \
	test/test_networkdynamics.py \
	test/test_stochasticrates.py \
	test/test_compartmentedmodel.py \
	test/compartmenteddynamics.py \
	test/test_sir.py \
	test/test_sis.py \
	test/test_fixed_recovery.py \
	test/test_adddelete.py
TESTSUITE = test

SOURCES_DOC_CONF = doc/conf.py
SOURCES_DOC_BUILD_DIR = doc/_build
SOURCES_DOC_BUILD_HTML_DIR = $(SOURCES_DOC_BUILD_DIR)/html
SOURCES_DOC_ZIP = $(PACKAGENAME)-doc-$(VERSION).zip
SOURCES_DOCUMENTATION = \
	doc/index.rst \
	doc/install.rst \
	doc/reference.rst \
	doc/simulation.rst \
	doc/bibliography.rst \
	doc/glossary.rst \
	doc/networkdynamics.rst \
	doc/synchronousdynamics.rst \
	doc/stochasticdynamics.rst \
	doc/loci.rst \
	doc/compartmentedmodel.rst \
	doc/sir.rst \
	doc/sis.rst \
	doc/sir_fixed_recovery.rst \
	doc/sis_fixed_recovery.rst \
	doc/adddelete.rst \
	doc/tutorial.rst \
	doc/tutorial/use-standard-model.rst \
	doc/tutorial/build-sir.rst \
	doc/tutorial/run-at-scale.rst  \
	doc/tutorial/advanced-topics.rst \
	doc/cookbook.rst \
	doc/cookbook/build-network-in-experiment.rst \
	doc/cookbook/population-powerlaw-cutoff.rst \
	doc/cookbook/monitoring-progress.rst \
	doc/cookbook/infect-specific-nodes.rst \
	doc/cookbook/powerlaw-cutoff.png \
	doc/cookbook/sir-progress-dt.png \
	doc/cookbook/sir-progress-er.png \
	doc/cookbook/sir-progress-plc.png
SOURCES_PAPER = \
	paper.md \
	paper.bib

# Extras for building diagrams etc
SOURCES_UTILS = \
    utils/make-powerlaw-cutoff.py \
    utils/make-monitor-progress.py

# Extras for the build and packaging system
SOURCES_EXTRA = \
	README.rst \
	LICENSE \
	HISTORY \
	CONTRIBUTORS
SOURCES_GENERATED = \
	MANIFEST \
	setup.py


# ----- Tools -----

# Base commands
PYTHON = python3
TOX = tox
COVERAGE = coverage
PIP = pip
TWINE = twine
GPG = gpg
VIRTUALENV = $(PYTHON) -m venv
ACTIVATE = . $(VENV)/bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r

# Root directory
ROOT = $(shell pwd)

# Requirements for running the library and for the development venv needed to build it
VENV = venv3
REQUIREMENTS = requirements.txt
DEV_REQUIREMENTS = dev-requirements.txt

# Constructed commands
RUN_TESTS = $(TOX)
RUN_COVERAGE = $(COVERAGE) erase && $(COVERAGE) run -a setup.py test && $(COVERAGE) report -m --include '$(PACKAGENAME)*'
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = PYTHONPATH=$(ROOT) make html
RUN_TWINE = $(TWINE) upload dist/*


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run tests for all versions of Python we're interested in
test: env Makefile setup.py
	$(ACTIVATE) && $(RUN_TESTS)

# Run coverage checks over the test suite
coverage: env
	$(ACTIVATE) && $(RUN_COVERAGE)

# Build the API documentation using Sphinx
.PHONY: doc
doc: $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	$(ACTIVATE) && $(CHDIR) doc && $(RUN_SPHINX_HTML)

# Build a development venv from the requirements in the repo
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CAT) $(REQUIREMENTS) $(DEV_REQUIREMENTS) >$(VENV)/requirements.txt
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt

# Build a source distribution
sdist: $(SOURCES_SDIST)

# Build a wheel distribution
wheel: $(SOURCES_WHEEL)

# Upload a source distribution to PyPi
upload: sdist wheel
	$(GPG) --detach-sign -a dist/$(PACKAGENAME)-$(VERSION).tar.gz
	$(ACTIVATE) && $(RUN_TWINE)

# Clean up the distribution build 
clean:
	$(RM) $(SOURCES_GENERATED) $(SOURCES_DIST_DIR) epyc.egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP) dist build

# Clean up everything, including the computational environment (which is expensive to rebuild)
reallyclean: clean
	$(RM) $(VENV)


# ----- Generated files -----

# Manifest for the package
MANIFEST: Makefile
	echo  $(SOURCES_EXTRA) $(SOURCES_GENERATED) $(SOURCES_CODE) | $(TR) ' ' '\n' >$@

# The setup.py script
setup.py: $(SOURCES_SETUP_IN) Makefile
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's/VERSION/$(VERSION)/g' -e 's/REQUIREMENTS/$(PY_REQUIREMENTS:%="%",)/g' >$@

# The source distribution tarball
$(SOURCES_SDIST): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	$(ACTIVATE) && $(RUN_SETUP) sdist

# The binary (wheel) distribution
$(SOURCES_WHEEL): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	$(ACTIVATE) && $(RUN_SETUP) bdist_wheel


# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite for all Python versions we support
   make coverage     run coverage checks of the test suite
   make doc          build the API documentation using Sphinx
   make env          create a known-good development virtual environment
   make sdist        create a source distribution
   make wheel	     create binary (wheel) distribution
   make upload       upload distribution to PyPi
   make clean        clean-up the build
   make reallyclean  clean up the virtualenv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
