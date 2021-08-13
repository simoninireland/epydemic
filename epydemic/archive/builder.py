# Network builder and archive submission
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
from tempfile import NamedTemporaryFile
import sys
import json
from networkx import Graph, write_adjlist
from typing import Any, Dict, List
if sys.version_info >= (3, 8):
    from typing import Final
else:
    # backport compatibility with older typing
    from typing_extensions import Final
from epydemic import NetworkGenerator
from epydemicarchive.api.v1.client import Archive


class ArchiveBuilder(NetworkGenerator):
    '''A network generator that uses another generator to construct
    a network that it then submits to an epydemic archive.

    If the base URI is not provided it is loaded from the SERVER_URI
    environment variable.  If the API key is not provided it is loaded
    from the API_KEY environment variable. This allows programs that
    populate an archive to be configured from their runtime
    environment.  Exceptions are raised if these values aren't
    available.

    :param gen: the underlying network generator
    :param uri: (optional) the base URI of the archive
    :param api_key: (optional) the API key to authenticate against the archive
    :param tags: (optional) tags to be applied to the network in the archive

    '''

    def __init__(self, gen: NetworkGenerator, uri: str = None, api_key: str = None, tags: List[str] = []):
        super().__init__()
        self._generator: NetworkGenerator = gen
        self._archive = Archive(uri, api_key)
        self._tags = tags
        self._uuids = []

    def topology(self) -> str:
        '''Return the topology flag for this generator. This is the same
        as the topology for the underlying generator.

        :returns: the topology'''
        return self._generator.topology()

    def _generate(self, params: Dict[str, Any]) -> Graph:
        '''Return a network from the underlying generator,
        submitting a copy to the archive.

        :param params: experimental parameters (ignored)
        :returns: a network instance'''

        # create the network using the underlying generator
        g = self._generator._generate(params)

        # submit the network to the archive, storing its UUID
        uuid = self._archive.submit(g, tags=self._tags)
        self._uuids.append(uuid)

        # return the network as usual
        return g

    def generated(self):
        '''Return a list of the UUIDs of the networks generated.

        :returns: a list of UUIDs'''
        return self._uuids