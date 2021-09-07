# author: Liberty Askew
# last modified: 17/08/2021

import sys
import networkx as nx
from epydemic import CompartmentedModel, Locus, CompartmentedEdgeLocus

if sys.version_info >= (3, 8):
    from typing import Dict, Any, List, Final, Tuple, Callable
else:
    # backport compatibility with older typing
    from typing import Dict, Any, List, Tuple, Callable
    from typing_extensions import Final


class SpreadStifleLocus(CompartmentedEdgeLocus):
    """
    Locus for Spreader->Stifle or Spreader->Spreader edges. Tracking because stifle event occurs to
    these edges for the opinion model. Typical CompartmentedEdgeLocus only allowsm1 type of edge tracking.
    """

    def __init__(self, name , l , r ):

        super().__init__(name, l , r)


    def matches(self, g , n , m ):
        """
        Overrides CompartmentedEdgeLocus.matches to check if Spreader->Stifle or Spreader->Spreader edge.
        """
        if (g.nodes[n][CompartmentedModel.COMPARTMENT] == self._right) and (g.nodes[m][CompartmentedModel.COMPARTMENT] == self._left):
            return 1
        else:
            if (g.nodes[n][CompartmentedModel.COMPARTMENT] == self._left) and (g.nodes[m][CompartmentedModel.COMPARTMENT] == 'Opinion.T'): #spreader -> stifler
                return 1
            else:
                if (g.nodes[n][CompartmentedModel.COMPARTMENT] == 'Opinion.T') and (g.nodes[m][CompartmentedModel.COMPARTMENT] == self._left):
                    return -1 #reversed
                else:
                    return 0 #no match


class Opinion(CompartmentedModel):
    """
    Model for opinion spreading model. Based on epydemic.SIR model structure and adapted for Moreno's
    opinion model from report.
    """

    P_AFFECTED : Final[float] = 'Opinion.pAffected'  #: Parameter for probability of initially being affected at start.
    P_AFFECT : Final[float] = 'Opinion.pAffect'      #: Parameter for probability of affect on contact.
    P_STIFLE : Final[float] = 'Opinion.pStifle'      #: Parameter for probability of becoming stifler on contact.


    IGNORANT : Final[str] = 'Opinion.G'              #: Compartment for nodes susceptible to infection.
    SPREADER : Final[str] = 'Opinion.P'              #: Compartment for nodes infected.
    STIFLER : Final[str] = 'Opinion.T'               #: Compartment for nodes recovered/removed.


    GP : Final[str] = 'Opinion.GP'                 #: Edge able to transmit infection.
    PPT : Final[str] = 'Opinion.PPT'               #: Spreader->Stifle or Spreader->Spreader edges able to transmit stifling.

    def __init__(self):
        super().__init__()
        self._finalNetwork : Graph = None


    def build(self, params):
        """
        Build the opinion model
        params: dictionary
            params['Opinion.pAffected']
            params['Opinion.pAffect']
            params['Opinion.pStifle']
        """
        super(Opinion, self).build(params)

        pAffected = params[self.P_AFFECTED]
        pAffect = params[self.P_AFFECT]
        pStifle = params[self.P_STIFLE]

        self.addCompartment(self.IGNORANT, 1 - float(pAffected))
        self.addCompartment(self.SPREADER, pAffected)
        self.addCompartment(self.STIFLER, 0.0)

        self.trackEdgesBetweenCompartments(self.IGNORANT, self.SPREADER, name=self.GP)
        self.trackSpreaderEdges(self.SPREADER, self.SPREADER, name=self.PPT) #special hander for spreader->spreader and spreader->stifler

        self.trackNodesInCompartment(self.IGNORANT)
        self.trackNodesInCompartment(self.SPREADER)
        self.trackNodesInCompartment(self.STIFLER)

        self.addEventPerElement(self.GP, pAffect, self.affect)
        self.addEventPerElement(self.PPT, pStifle, self.stifle)


    def trackSpreaderEdges(self, l, r, name):
        """
        Add a locus to track edges with endpoint nodes in the given compartments.
        l: the compartment of the left node
        r: the compartment of the right node
        name: (optional) the name of the locus (defaults to a combination of the two compartment names)
        return: the locus used to track the nodes
        """
        locus = SpreadStifleLocus(name, l, r)
        return self.addLocus(name, locus)


    def affect(self, t, e):
        """
        Performs affect event. Changes the compartment of
        the ignorant-end node to `AFFECTED`. It also marks the edge
        traversed as occupied.

        t: the simulation time
        e: the edge transmitting the infection, spreader -> ignorant
        """
        (n, _) = e
        self.changeCompartment(n, self.SPREADER)
        self.markOccupied(e, t)


    def stifle(self, t, e):
        """
        Performs a stifle event. This changes the compartment of
        the node to `STIFLER`.

        t: the simulation time (unused)
        n: the node
        """
        (n, _) = e
        self.changeCompartment(n, self.STIFLER)


    def results(self):
        """
        Grabs final results of network and stores the final network as class attribute _finalNetwork
        for analysis.
        returns: results dictionary
        """
        res = super().results()
        self._finalNetwork = self.network().copy()
        return res
