from epydemic import BANetwork
from epydemic.archive import ArchiveBuilder

params = dict()
params[BANetwork.N] = 2000
params[BANetwork.M] = 2

gen = ArchiveBuilder(BANetwork())
g = gen.set(params).generate()
