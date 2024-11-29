# Test the behaviour of SIR over a dynamic population
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

from epydemic import *
import epyc
import unittest
import networkx


class DynamicSIR(SIR, AddDelete):
    '''Test process for the multiple inheritance approach.'''

    N = 'networkSize'

    def __init__(self, name: str = None):
        super().__init__(name)


    def addNewNode(self, **kwds):
        '''Mark new nodes as susceptible.

        :param kwds: (optional) node attributes
        :returns: the generated name of the new node'''

        # add the node, capturing its name
        n = super().addNewNode(**kwds)

        # set the compartment of this node to susceptible
        self.setCompartment(n, SIR.SUSCEPTIBLE)

        # return the name of the new node
        return n


    def removeNode(self, n):
        '''Mark any node as removed before deleting.

        :param n: the node'''

        # change the node's compartment to removed
        self.changeCompartment(n, SIR.REMOVED)

        # delete the node
        super().removeNode(n)


    def results( self ):
        '''Save the size of the resulting network.

        :returns: a dict of experimental results'''
        rc = super().results()
        rc[self.N] = self.network().order()
        return rc


class CompartmentedAddDelete(AddDelete):
    '''Test process for the process sequence approach.'''

    N = 'networkSize'
    DISEASE = 'diseaseModel'

    def __init__(self, name: str = None):
        super().__init__(name)


    def addNewNode(self, **kwds):
        '''Mark new nodes as susceptible.

        :param kwds: (optional) node attributes
        :returns: the generated name of the new node'''

        # add the node, capturing its name
        n = super().addNewNode(**kwds)

        # set the compartment of this node to susceptible
        self.container()[self.DISEASE].setCompartment(n, SIR.SUSCEPTIBLE)

        # return the name of the new node
        return n


    def removeNode(self, n):
        '''Mark any node as removed before deleting.

        :param n: the node'''

        # change the node's compartment to removed
        self.container()[self.DISEASE].changeCompartment(n, SIR.REMOVED)

        # delete the node
        super().removeNode(n)


    def results( self ):
        '''Save the size of the resulting network.

        :returns: a dict of experimental results'''
        rc = super().results()
        rc[self.N] = self.network().order()
        return rc


class AddDeleteSIRTest(unittest.TestCase):

    def setUp(self):
        '''Set up the experimental parameters and process.'''
        self._N = 5000
        self._kmean = 10
        self._phi = (self._kmean + 0.0) / self._N
        self._network = networkx.erdos_renyi_graph(self._N, self._phi)
        self._maxTime = 5000

        self._params = dict()
        self._params[AddDelete.DEGREE] = 10
        self._params[SIR.P_INFECT] = 0.1
        self._params[SIR.P_INFECTED] = 0.01
        self._params[SIR.P_REMOVE] = 0.05

        self._process = DynamicSIR()
        self._process.setMaximumTime(self._maxTime)
        self._e = StochasticDynamics(self._process, self._network)

    def testIndependent(self):
        '''Test that the epidemic doesn't affect the population size when run with equal rates.'''
        self._params[AddDelete.P_ADD] = 1
        self._params[AddDelete.P_DELETE] = 1
        rc = self._e.set(self._params).run(fatal=True)
        self.assertAlmostEqual(rc[epyc.Experiment.RESULTS][DynamicSIR.N], self._network.order(), delta = int((self._network.order() + 0.0) * 0.1))

    def testZeroRates(self):
        '''Test that zero rates leave a fixed population and a normal epidemic.'''
        self._params[AddDelete.P_ADD] = 0
        self._params[AddDelete.P_DELETE] = 0
        rc = self._e.set(self._params).run(fatal=True)
        self.assertEqual(rc[epyc.Experiment.RESULTS][DynamicSIR.N], self._network.order())
        self.assertEqual(rc[epyc.Experiment.RESULTS][DynamicSIR.N], self._N)
        self.assertCountEqual(rc[epyc.Experiment.RESULTS], [DynamicSIR.N, SIR.SUSCEPTIBLE, SIR.INFECTED, SIR.REMOVED])
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIR.SUSCEPTIBLE] > 0)
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIR.INFECTED] == 0)
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIR.REMOVED] > 0)
        self.assertEqual(rc[epyc.Experiment.RESULTS][SIR.SUSCEPTIBLE] + rc[epyc.Experiment.RESULTS][SIR.REMOVED], self._network.order())

    def testAllInCompartments(self):
        '''Test that all nodes land in a compartment.'''
        self._params[AddDelete.P_ADD] = 1
        self._params[AddDelete.P_DELETE] = 1
        rc = self._e.set(self._params).run(fatal=True)
        self.assertEqual(rc[epyc.Experiment.RESULTS][DynamicSIR.N], rc[epyc.Experiment.RESULTS][SIR.SUSCEPTIBLE] + rc[epyc.Experiment.RESULTS][SIR.INFECTED] + rc[epyc.Experiment.RESULTS][SIR.REMOVED])


    def testSequence(self):
        '''Test the process sequence approach.'''
        self._params[AddDelete.P_ADD] = 1
        self._params[AddDelete.P_DELETE] = 1
        ps = dict()
        ps[CompartmentedAddDelete.DISEASE] = SIR()
        ps['adddelete'] = CompartmentedAddDelete()
        self._process = ProcessSequence(ps)
        self._process.setMaximumTime(self._maxTime)
        self._e = StochasticDynamics(self._process, self._network)
        rc = self._e.set(self._params).run(fatal=True)
        self.assertAlmostEqual(rc[epyc.Experiment.RESULTS][CompartmentedAddDelete.N], self._network.order(), delta = int((self._network.order() + 0.0) * 0.1))


if __name__ == '__main__':
    unittest.main()
