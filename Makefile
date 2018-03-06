# Makefile for epydemic
#
# Copyright (C) 2017 Simon Dobson
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
VERSION = 0.4.1


# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
SOURCES_SDIST = dist/$(PACKAGENAME)-$(VERSION).tar.gz
SOURCES_CODE = \
	epydemic/__init__.py \
	epydemic/networkdynamics.py \
	epydemic/synchronousdynamics.py \
	epydemic/stochasticdynamics.py \
	epydemic/compartmentedmodel.py \
	epydemic/loci.py \
	epydemic/compartmentedsynchronousdynamics.py \
	epydemic/compartmentedstochasticdynamics.py \
	epydemic/sir_model.py \
	epydemic/sir_model_fixed_recovery.py \
	epydemic/sis_model.py \
	epydemic/sis_model_fixed_recovery.py

SOURCES_TESTS = \
	test/__init__.py \
	test/__main__.py \
	test/networkdynamics.py \
	test/compartmentedmodel.py \
	test/compartmenteddynamics.py \
	test/sir.py \
	test/sis.py \
	test/fixed_recovery.py
TESTSUITE = test

SOURCES_TUTORIAL = doc/epydemic.ipynb
SOURCES_DOC_CONF = doc/conf.py
SOURCES_DOC_BUILD_DIR = doc/_build
SOURCES_DOC_BUILD_HTML_DIR = $(SOURCES_DOC_BUILD_DIR)/html
SOURCES_DOC_ZIP = epydemic-doc-$(VERSION).zip
SOURCES_DOCUMENTATION = \
	doc/index.rst \
	doc/bibliography.rst \
	doc/glossary.rst \
	doc/networkdynamics.rst \
	doc/synchronousdynamics.rst \
	doc/stochasticdynamics.rst \
	doc/compartmenteddynamics.rst \
	doc/loci.rst \
	doc/compartmentedmodel.rst \
	doc/sir.rst \
	doc/sis.rst \
	doc/sir_fixed_recovery.rst \
	doc/sis_fixed_recovery.rst

SOURCES_EXTRA = \
	README.rst \
	LICENSE \
	HISTORY
SOURCES_GENERATED = \
	MANIFEST \
	setup.py

# Python packages needed
# For the system to install and run
PY_REQUIREMENTS = \
	numpy \
	networkx \
	epyc
# For the documentation and development venv
PY_DEV_REQUIREMENTS = \
	ipython \
	jupyter \
	matplotlib \
	seaborn \
	sphinx \
	twine

# Packages that shouldn't be saved as requirements (because they're
# OS-specific, in this case OS X, and screw up Linux compute servers)
PY_NON_REQUIREMENTS = \
	appnope \
	functools32 \
	subprocess32
VENV = venv
REQUIREMENTS = requirements.txt
DEV_REQUIREMENTS = dev-requirements.txt


# ----- Tools -----

# Base commands
PYTHON = python
IPYTHON = ipython
JUPYTER = jupyter
IPCLUSTER = ipcluster
PIP = pip
TWINE = twine
GPG = gpg
VIRTUALENV = virtualenv
ACTIVATE = . bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r

# Root directory
ROOT = $(shell pwd)

# Constructed commands
RUN_TESTS = $(IPYTHON) -m $(TESTSUITE)
RUN_NOTEBOOK = $(JUPYTER) notebook
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = make html
RUN_TWINE = $(TWINE) upload dist/$(PACKAGENAME)-$(VERSION).tar.gz dist/$(PACKAGENAME)-$(VERSION).tar.gz.asc
NON_REQUIREMENTS = $(SED) $(patsubst %, -e '/^%*/d', $(PY_NON_REQUIREMENTS))


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run the test suite in a suitable (predictable) virtualenv
.PHONY: test
test: venv
	($(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) .. && $(RUN_TESTS))

# Build the API documentation using Sphinx
.PHONY: doc
doc: $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	($(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) ../doc && PYTHONPATH=.. $(RUN_SPHINX_HTML))
	($(CHDIR) $(SOURCES_DOC_BUILD_HTML_DIR) && $(ZIP) $(SOURCES_DOC_ZIP) *)
	$(CP) $(SOURCES_DOC_BUILD_HTML_DIR)/$(SOURCES_DOC_ZIP) .

# Run a server for writing the documentation
.PHONY: docserver
docserver:
	($(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) ../doc && PYTHONPATH=.. $(RUN_NOTEBOOK))

# Build a development venv from the known-good requirements in the repo
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CP) $(DEV_REQUIREMENTS) $(VENV)/requirements.txt
	$(CHDIR) $(VENV) && $(ACTIVATE) && $(PIP) install -r requirements.txt

# Build a development venv from the latest versions of the required packages,
# creating a new requirements.txt ready for committing to the repo. Make sure
# things actually work in this venv before committing!
.PHONY: newenv
newenv:
	$(RM) $(VENV)
	$(VIRTUALENV) $(VENV)
	echo $(PY_REQUIREMENTS) | $(TR) ' ' '\n' >$(VENV)/$(REQUIREMENTS)
	$(CHDIR) $(VENV) && $(ACTIVATE) && $(PIP) install -r requirements.txt && $(PIP) freeze >requirements.txt
	$(NON_REQUIREMENTS) $(VENV)/requirements.txt >$(REQUIREMENTS)
	echo $(PY_DEV_REQUIREMENTS) | $(TR) ' ' '\n' >$(VENV)/$(REQUIREMENTS)
	$(CHDIR) $(VENV) && $(ACTIVATE) && $(PIP) install -r requirements.txt && $(PIP) freeze >requirements.txt
	$(NON_REQUIREMENTS) $(VENV)/requirements.txt >$(DEV_REQUIREMENTS)

# Build a source distribution
sdist: $(SOURCES_SDIST)

# Upload a source distribution to PyPi
upload: $(SOURCES_SDIST)
	$(GPG) --detach-sign -a dist/$(PACKAGENAME)-$(VERSION).tar.gz
	($(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) $(ROOT) && $(RUN_TWINE))

# Clean up the distribution build 
clean:
	$(RM) $(SOURCES_GENERATED) epyc.egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP)

# Clean up everything, including the computational environment (which is expensive to rebuild)
reallyclean: clean
	$(RM) $(VENV)


# ----- Helper targets -----

# Build a computational environment in which to run the test suite
env-computational: $(ENV_COMPUTATIONAL)

# Build a new, updated, requirements.txt file ready for commiting to the repo
# Only commit if we're sure we pass the test suite!
newenv-computational:
	echo $(PY_COMPUTATIONAL) $(PY_INTERACTIVE) | $(TR) ' ' '\n' >$(REQ_COMPUTATIONAL)
	make env-computational
	$(NON_REQUIREMENTS) $(ENV_COMPUTATIONAL)/requirements.txt >$(REQ_COMPUTATIONAL)

# Only re-build computational environment if the directory is missing
$(ENV_COMPUTATIONAL):
	$(VIRTUALENV) $(ENV_COMPUTATIONAL)
	$(CP) $(REQ_COMPUTATIONAL) $(ENV_COMPUTATIONAL)/requirements.txt
	$(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(PIP) install -r requirements.txt && $(PIP) freeze >requirements.txt


# ----- Generated files -----

# Manifest for the package
MANIFEST: Makefile
	echo  $(SOURCES_EXTRA) $(SOURCES_GENERATED) $(SOURCES_CODE) | $(TR) ' ' '\n' >$@

# The setup.py script
setup.py: $(SOURCES_SETUP_IN) Makefile
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's/VERSION/$(VERSION)/g' -e 's/REQUIREMENTS/$(PY_REQUIREMENTS:%="%",)/g' >$@

# The source distribution tarball
$(SOURCES_SDIST): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	($(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) $(ROOT) && $(RUN_SETUP) sdist)


# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite in a suitable virtualenv
   make doc          build the API documentation using Sphinx
   make docserver    run a Jupyter notebook to edit the tutorial
   make dist         create a source distribution
   make upload       upload distribution to PyPi
   make clean        clean-up the build
   make reallyclean  clean up the virtualenv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
