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
VERSION = 0.2.0

# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
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
	epydemic/sis_model.py

SOURCES_TESTS = \
	test/__init__.py \
	test/__main__.py \
	test/compartmentedmodel.py \
	test/sir.py \
	test/sis.py
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
	doc/sis.rst

SOURCES_EXTRA = \
	README.rst \
	LICENSE \
	HISTORY
SOURCES_GENERATED = \
	MANIFEST \
	setup.py

# Python packages needed
# For the system to install and run
PY_COMPUTATIONAL = \
	numpy \
	networkx \
	epyc
# For the documentation
PY_INTERACTIVE = \
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

# Constructed commands
RUN_TESTS = $(IPYTHON) -m $(TESTSUITE)
RUN_NOTEBOOK = $(JUPYTER) notebook
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = make html
RUN_TWINE = $(TWINE) upload dist/$(PACKAGENAME)-$(VERSION).tar.gz dist/$(PACKAGENAME)-$(VERSION).tar.gz.asc

# Virtual environment support
ENV_COMPUTATIONAL = venv
REQ_COMPUTATIONAL = requirements.txt
NON_REQUIREMENTS = $(SED) $(patsubst %, -e '/^%*/d', $(PY_NON_REQUIREMENTS))
REQ_SETUP = $(PY_COMPUTATIONAL:%="%",)


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run the test suite in a suitable (predictable) virtualenv
test: env-computational
	($(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(CHDIR) .. && $(RUN_TESTS))

# Build the API documentation using Sphinx
.PHONY: doc
doc: $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	($(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(CHDIR) ../doc && PYTHONPATH=.. $(RUN_SPHINX_HTML))
	($(CHDIR) $(SOURCES_DOC_BUILD_HTML_DIR) && $(ZIP) $(SOURCES_DOC_ZIP) *)
	$(CP) $(SOURCES_DOC_BUILD_HTML_DIR)/$(SOURCES_DOC_ZIP) .

# Run a server for writing the documentation
.PHONY: docserver
docserver:
	($(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(CHDIR) ../doc && PYTHONPATH=.. $(RUN_NOTEBOOK))

# Build a source distribution
dist: $(SOURCES_GENERATED)
	$(RUN_SETUP) sdist

# Upload a source distribution to PyPi
upload: $(SOURCES_GENERATED) dist
	$(GPG) --detach-sign -a dist/$(PACKAGENAME)-$(VERSION).tar.gz
	($(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(CHDIR) .. && $(RUN_TWINE))

# Clean up the distribution build 
clean:
	$(RM) $(SOURCES_GENERATED) epyc.egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP)

# Clean up everything, including the computational environment (which is expensive to rebuild)
reallyclean: clean
	$(RM) $(ENV_COMPUTATIONAL)


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
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's/VERSION/$(VERSION)/g' -e 's/REQ_SETUP/$(REQ_SETUP)/g' >$@


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
