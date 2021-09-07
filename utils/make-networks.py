# Craete networks to populate the archive
#
# Copyright (C) 2017--2021 Simon Dobson
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

import os
from sys import argv, exit
import json
from dotenv import load_dotenv
from epyc import Lab, ParallelLab, Experiment, RepeatedExperiment
from epydemic import ERNetwork, BANetwork, PLCNetwork
from epydemic.archive import ArchiveBuilder


class CreateNetwork(Experiment):

    def __init__(self, topology, tags):
        super().__init__()

        # construct the underlying network generator
        if topology == 'ER':
            self._gen = ERNetwork()
        elif topology == 'BA':
            self._gen = BANetwork()
        elif topology == 'PLC':
            self._gen = PLCNetwork()
        else:
            raise Exception(f'Unrecognised topology {topology}')
        self._generator = None
        self._tags = tags

    def configure(self, params):
        super().configure(params)
        self._generator = ArchiveBuilder(self._gen,
                                         tags=self._tags)

    def do(self, params):
        _ = self._generator.set(params).generate()
        return {'UUID': self._generator.generated()[-1]}


# Load configuration
if len(argv) != 2:
    print('usage: make-networks.py <json-file>')
    exit(1)
configfile = argv[1]
with open(configfile, 'r') as rh:
    config = json.load(rh)
specs = config['networks']

# Load environment from .env if present
load_dotenv(dotenv_path='.env')

# Create the lab
lab = ParallelLab(cores=-2)
nb = lab.notebook()

# Process each network specification
n = 0
for spec in specs:
    # keep different specifications separate
    nb.addResultSet(f'Networks {n}')

    # construct the networks
    topology = spec['topology']
    tags = spec.get('tags', ['random'])
    repetitions = spec.get('repetitions', 1)
    e = CreateNetwork(topology, tags)
    params = spec['matrix']
    for k in params:
        lab[k] = params[k]
    lab.runExperiment(RepeatedExperiment(e, repetitions))
    for k in params:
        del lab[k]
    n += 1

    # Show the UUIDs
    uuids = nb.dataframe()['UUID']
    print('\n'.join(uuids))
