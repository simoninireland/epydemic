from epydemic.archive import Reuse

tags = ['random']
constraints = [('N', '<', 1000),
               ('degree-distribution', '==', 'ER'),
               ('kmean', '>=', 4),
               ('kmean', '<=', 5)]

gen = Reuse(tags=tags, metadata=constraints)

g = gen.generate()
