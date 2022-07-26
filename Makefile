# Makefile for epydemic
#
# Copyright (C) 2017--2022 Simon Dobson
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
VERSION = 1.11.1


# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
SOURCES_CODE = \
	epydemic/__init__.py \
	epydemic/types.py \
	epydemic/bitstream.py \
	epydemic/bbt.py \
	epydemic/drawset.py \
	epydemic/networkexperiment.py \
	epydemic/networkdynamics.py \
	epydemic/synchronousdynamics.py \
	epydemic/stochasticdynamics.py \
	epydemic/generator.py \
	epydemic/standard_generators.py \
	epydemic/plc_generator.py \
	epydemic/loci.py \
	epydemic/process.py \
	epydemic/processsequence.py \
	epydemic/compartmentedmodel.py \
	epydemic/sir_model.py \
	epydemic/sir_model_fixed_recovery.py \
	epydemic/sir_model_variable_infection.py \
	epydemic/sis_model.py \
	epydemic/sis_model_fixed_recovery.py \
	epydemic/sirs_model.py \
	epydemic/seir_model.py \
	epydemic/adddelete.py \
	epydemic/percolate.py \
	epydemic/monitor.py \
	epydemic/statistics.py \
	epydemic/shuffle.py \
	epydemic/newmanziff.py \
	epydemic/opinion_model.py \
	epydemic/vaccinate_model.py \
	epydemic/sivr_model.py \
	epydemic/gf/__init__.py \
	epydemic/gf/gf.py \
	epydemic/gf/function_gf.py \
	epydemic/gf/discrete_gf.py \
	epydemic/gf/continuous_gf.py \
	epydemic/gf/interface.py \
	epydemic/gf/standard_gfs.py \
	epydemic/archive/__init__.py \
	epydemic/archive/builder.py
SOURCES_TESTS = \
	test/__init__.py \
	test/test_bitstream.py \
	test/test_networkdynamics.py \
	test/test_stochasticrates.py \
	test/test_compartmentedmodel.py \
	test/compartmenteddynamics.py \
	test/test_loci.py \
	test/test_sir.py \
	test/test_sir_fixedrecovery.py \
	test/test_sir_variable_infection.py \
	test/test_sis.py \
	test/test_sis_fixedrecovery.py \
	test/test_sirs.py \
	test/test_seir.py \
	test/test_process.py \
	test/test_processsequence.py \
	test/test_adddelete.py \
	test/test_adddeletesir.py \
	test/test_percolate.py \
	test/test_shuffle.py \
	test/test_newmanziff.py \
	test/test_opinion.py \
	test/test_vaccination.py \
	test/test_gf.py \
	test/test_gof.py \
	test/test_events.py \
	test/test_sto_sync.py
TESTSUITE = test

SOURCES_DOC_CONF = doc/conf.py
SOURCES_DOC_BUILD_DIR = doc/_build
SOURCES_DOC_BUILD_HTML_DIR = $(SOURCES_DOC_BUILD_DIR)/html
SOURCES_DOC_ZIP = $(PACKAGENAME)-doc-$(VERSION).zip
SOURCES_DOCUMENTATION = \
	doc/index.rst \
	doc/install.rst \
	doc/reference.rst \
	doc/contributing.rst \
	doc/classes.rst \
	doc/zbibliography.rst \
	doc/glossary.rst \
	doc/helper-types.rst \
	doc/networkdynamics.rst \
	doc/synchronousdynamics.rst \
	doc/stochasticdynamics.rst \
	doc/drawset.rst \
	doc/rng.rst \
	doc/loci.rst \
	doc/compartmentedmodel.rst \
	doc/generator.rst \
	doc/standard_generators.rst \
	doc/sir.rst \
	doc/sis.rst \
	doc/sir_fixed_recovery.rst \
	doc/sis_fixed_recovery.rst \
	doc/sirs.rst \
	doc/seir.rst \
	doc/opinion.rst \
	doc/sivr.rst \
	doc/vaccinate.rst \
	doc/adddelete.rst \
	doc/percolate.rst \
	doc/monitor.rst \
	doc/statistics.rst \
	doc/shuffle.rst \
	doc/processsequence.rst \
	doc/newmanziff.rst  \
	doc/gf.rst \
	doc/standard-gfs.rst \
	doc/tutorial.rst \
	doc/tutorial/simulation.rst \
	doc/tutorial/use-standard-model.rst \
	doc/tutorial/build-sir.rst \
	doc/tutorial/run-at-scale.rst  \
	doc/tutorial/process-composition.rst \
	doc/tutorial/advanced-topics.rst \
	doc/tutorial/generators.rst \
	doc/implementation.rst \
	doc/implementation/challenges.rst \
	doc/implementation/no-multiple-inheritance.rst \
	doc/implementation/events.rst \
	doc/implementation/dynamics.rst \
	doc/implementation/gf-maths.rst \
	doc/cookbook.rst \
	doc/cookbook/population-powerlaw-cutoff.rst \
	doc/cookbook/monitoring-progress.rst \
	doc/cookbook/infect-specific-nodes.rst \
	doc/cookbook/dynamic-population.rst \
	doc/cookbook/keep-network.rst \
	doc/cookbook/percolation-threshold.rst \
	doc/cookbook/from-r-to-probabilities.rst \
	doc/cookbook/speed.rst \
	doc/cookbook/compare-series.rst
SOURCES_DIAGRAMS = \
	doc/cookbook/powerlaw-cutoff.png \
	doc/cookbook/sir-progress-dt.png \
	doc/cookbook/sir-progress-er.png \
	doc/cookbook/sir-progress-plc.png \
	doc/cookbook/bond-percolation-er.png \
	doc/cookbook/site-percolation-er.png \
	doc/cookbook/bond-percolation-plc.png \
	doc/cookbook/site-percolation-plc.png \
	doc/cookbook/sir-time-series.png \
	doc/cookbook/sir-time-series-raw.png \
	doc/implementation/sir-stochastic.png \
	doc/implementation/sir-synchronous.png
SOURCES_BIBLIOGRAPHY = doc/bibliography.bib
SOURCES_PAPER = \
	paper.md \
	paper.bib

# Extras for building diagrams etc
SOURCES_UTILS = \
	utils/make-powerlaw-cutoff.py \
	utils/make-monitor-progress.py \
	utils/make-percolation.py \
	utils/make-networks.py \
	utils/make-compare-time-series.py \
	utils/make-compare-syn-sto.py \
	utils/profile-simulation.py

# Extras for the build and packaging system
SOURCES_EXTRA = \
	README.rst \
	LICENSE \
	HISTORY \
	CONTRIBUTORS \
	CONTRIBUTING.rst
SOURCES_GENERATED = \
	MANIFEST \
	setup.py

# Distribution files
DIST_SDIST = dist/$(PACKAGENAME)-$(VERSION).tar.gz
DIST_WHEEL = dist/$(PACKAGENAME)-$(VERSION)-py3-none-any.whl

# ----- Tools -----

# Base commands
PYTHON = python3
TOX = tox
COVERAGE = coverage
PIP = pip
TWINE = twine
GPG = gpg
GIT = git
ETAGS = etags
VIRTUALENV = $(PYTHON) -m venv
ACTIVATE = . $(VENV)/bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r

# Files that are locally changed vs the remote repo
# (See https://unix.stackexchange.com/questions/155046/determine-if-git-working-directory-is-clean-from-a-script)
GIT_DIRTY = $(shell $(GIT) status --untracked-files=no --porcelain)

# The git branch we're currently working on
GIT_BRANCH = $(shell $(GIT) rev-parse --abbrev-ref HEAD 2>/dev/null)

# Root directory
ROOT = $(shell pwd)

# Requirements for running the library and for the development venv needed to build it
VENV = venv3
REQUIREMENTS = requirements.txt
DEV_REQUIREMENTS = dev-requirements.txt

# Requirements for setup.py
# Note we elide dependencies to do with backporting the type-checking
PY_REQUIREMENTS = $(shell $(SED) -e '/^typing_extensions/d' -e 's/^\(.*\)/"\1",/g' $(REQUIREMENTS) | $(TR) '\n' ' ')

# Constructed commands
RUN_TESTS = $(TOX)
RUN_COVERAGE = $(COVERAGE) erase && $(COVERAGE) run -a setup.py test && $(COVERAGE) report -m --include '$(PACKAGENAME)*'
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = PYTHONPATH=$(ROOT) make html
RUN_TWINE = $(TWINE) upload dist/*
RUN_JOSS_PREVIEW = docker run --rm --volume $(ROOT):/data --user $(id -u):$(id -g) --env JOURNAL=joss openjournals/paperdraft


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Build the tags file
tags:
	$(ETAGS) -o TAGS $(SOURCES_CODE) $(SOURCES_TESTS)

# Run tests for all versions of Python we're interested in
test: env Makefile setup.py
	$(ACTIVATE) && $(RUN_TESTS)

# Run coverage checks over the test suite
coverage: env
	$(ACTIVATE) && $(RUN_COVERAGE)

# Build the API documentation using Sphinx
.PHONY: doc
doc: env $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	$(ACTIVATE) && $(CHDIR) doc && $(RUN_SPHINX_HTML)

# Build a development venv from the requirements in the repo
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CAT) $(REQUIREMENTS) $(DEV_REQUIREMENTS) >$(VENV)/requirements.txt
	$(ACTIVATE) && $(PIP) install -U pip wheel && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt
	$(ACTIVATE) && mypy --install-types --non-interactive

# Build a source distribution
sdist: $(DIST_SDIST)

# Build a wheel distribution
wheel: $(DIST_WHEEL)

# Upload a source distribution to PyPi
upload: master-only commit sdist wheel
	$(GPG) --detach-sign -a dist/$(PACKAGENAME)-$(VERSION).tar.gz
	$(ACTIVATE) && $(RUN_TWINE)

# Check we're on the master branch befoire uploading
master-only:
	if [ "$(GIT_BRANCH)" != "master" ]; then echo "Can only upload from master branch"; exit 1; fi

# Update the remote repos on release
commit: check-local-repo-clean
	$(GIT) push origin master
	$(GIT) tag -a v$(VERSION) -m "Version $(VERSION)"
	$(GIT) push origin v$(VERSION)

.SILENT: check-local-repo-clean
check-local-repo-clean:
	if [ "$(GIT_DIRTY)" ]; then echo "Uncommitted files: $(GIT_DIRTY)"; exit 1; fi

# Build the diagrams for the documentation
diagrams:
	$(ACTIVATE) && PYTHONPATH=$(ROOT) $(PYTHON) utils/make-monitor-progress.py
	$(ACTIVATE) && PYTHONPATH=$(ROOT) $(PYTHON) utils/make-powerlaw-cutoff.py
	$(ACTIVATE) && PYTHONPATH=$(ROOT) $(PYTHON) utils/make-percolation.py
	$(ACTIVATE) && PYTHONPATH=$(ROOT) $(PYTHON) utils/make-compare-time-series.py
	$(ACTIVATE) && PYTHONPATH=$(ROOT) $(PYTHON) utils/make-compare-syn-sto.py

# Preview the JOSS paper
joss-paper:
	$(RUN_JOSS_PREVIEW)

# Clean up the distribution build
clean:
	$(RM) $(SOURCES_GENERATED) $(SOURCES_DIST_DIR) $(PACKAGENAME).egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP) dist build

# Clean up everything, including the computational environment (which is expensive to rebuild)
reallyclean: clean
	$(RM) $(VENV)


# ----- Generated files -----

# Manifest for the package
MANIFEST: Makefile
	echo  $(SOURCES_EXTRA) $(SOURCES_GENERATED) $(SOURCES_CODE) | $(TR) ' ' '\n' >$@

# The setup.py script
setup.py: $(SOURCES_SETUP_IN) $(REQUIREMENTS) Makefile
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's|VERSION|$(VERSION)|g' -e 's|REQUIREMENTS|$(PY_REQUIREMENTS)|g' >$@

# The source distribution tarball
$(DIST_SDIST): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	$(ACTIVATE) && $(RUN_SETUP) sdist

# The binary (wheel) distribution
$(DIST_WHEEL): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	$(ACTIVATE) && $(RUN_SETUP) bdist_wheel


# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite for all Python versions we support
   make coverage     run coverage checks of the test suite
   make tags         build the TAGS file
   make doc          build the API documentation using Sphinx
   make diagrams     create the diagrams for the API documentation
   make joss-paper   preview the JOSS paper on epydemic (uses docker)
   make env          create a development virtual environment
   make sdist        create a source distribution
   make wheel        create binary (wheel) distribution
   make upload       upload distribution to PyPi
   make clean        clean-up the build
   make reallyclean  clean up the virtualenv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
