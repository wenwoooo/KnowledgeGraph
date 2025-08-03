import numpy as np
import pandas as pd
from py2neo import Node, Relationship, Walkable
from configurations.neo4j_configuration import profile, name, auth

from super_neo4j import DatabaseNeo4j

tg = DatabaseNeo4j()
node = tg.evaluate('Effect', name='清热解毒')

print(list(node.labels))
print(tg.match([None, node], 'Treatment').first().end_node.labels)

print('--------------', list(tg.run("match (p1:MedicineName {name: '" + '山葡萄' +
                                    "'})<-[:Include]-(p3:Prescription)<-[:TreatmentWay]-(p2:Illness) return p2")))

# p1 = Node('person', name='小花')
# print(tg.create(p1))

# tx = tg.begin()
#
# matcher = NodeMatcher(tg)
# p1 = matcher.match('person', name='小花')
#
# print(p1.first())
#
# tg.delete(p1.first())
# tg.commit()
