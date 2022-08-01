# Generator that re-uses networks from the archive
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

import sys
from networkx import Graph
from typing import Any, Dict, List, Tuple
from epydemic import NetworkGenerator
from epydemicarchive.api.v1.client import Archive


class Reuse(NetworkGenerator):
    '''A network generator that attempts to re-use networks from an
    epydemic archive.

    The networks re-used can be constrained by tag or by metadata.
    Any network accessed is excluded from future re-use by this
    object, *not* generally: it's possible for other re-users to
    use the same network.

    The archive is searched for a chunk of networks, 1 by default. The
    pool of networks from which a chunk is drawn can be set to ensure
    that a sufficient ensemble of networks is drawn from.
    Networks are only downloaded as they are requested to be generated.

    If the base URI is not provided it is loaded from the SERVER_URI
    environment variable.  If the API key is not provided it is loaded
    from the API_KEY environment variable. This allows programs that
    populate an archive to be configured from their runtime
    environment.  Exceptions are raised if these values aren't
    available.

    :param uri: (optional) the base URI of the archive
    :param api_key: (optional) the API key to authenticate against the archive
    :param tags: (optional) tags on candidate networks
    :param metadata: (optional) metadata constraints on candidate networks
    :param exclude: (optional) list of networks to exclude (defaults to None)
    :param chunk: (optional) networks requested per chunk (defaults to 1)
    :param pool: (optional) minimum pool from which to draw (defaults to none)

    '''

    def __init__(self,
                 uri: str = None, api_key: str = None,
                 tags: List[str] = [],
                 metadata: List[Tuple[str, str, str]] = None,
                 exclude: List[str] = [],
                 chunk: int = 1,
                 pool: int = None):
        super().__init__()
        self._archive = Archive(uri, api_key)
        self._tags = tags
        self._metadata = metadata
        self._exclude = exclude
        self._chunk = chunk
        self._pool = pool
        self._uuids: List[str] = []

    def exclude(self):
        '''Return a list of UUIDs that can\'t be returned again.

        :retyurns: a list of excluded networks'''
        return self._exclude

    def _generate(self,  params: Dict[str, Any]) -> Graph:
        '''Return a network from the archive that matches the search criteria.
        An exception is raised if no such network can be retrieved.

        :param params: experimental parameters
        :returns: a network'''
        if len(self._uuids) == 0:
            # no networks, fetch a chunk
            self._uuids = self._archive.search(self._tags,
                                               self._metadata,
                                               exclude=self._exclude,
                                               n=self._chunk,
                                               pool=self._pool)
            if len(self._uuids) == 0:
                raise Exception('Can\'t retrieve chunk of networks')

        # pop a network UUID
        uuid = self._uuids.pop()

        # retrieve the network from the archive
        try:
            g = self._archive.raw(uuid)
            return g
        finally:
            # add the network to the exclude list for future calls
            self._exclude.append(uuid)
