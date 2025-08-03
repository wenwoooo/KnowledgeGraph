from __future__ import annotations

from py2neo import Graph, Node, NodeMatch, Relationship, NodeMatcher, RelationshipMatcher, RelationshipMatch
from py2neo.cypher import Cursor

from configurations.neo4j_configuration import profile as t_profile, name as t_name, auth
from tools import dict_to_str


def get_label_name(node: Node | NodeMatch | Relationship) -> str | None:
    if node is None:
        return None
    return list(node.labels)[0]


class DatabaseNeo4j:
    def __enter__(self) -> DatabaseNeo4j:
        self.__pre()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()

    def __init__(self, profile=t_profile, name=t_name, **settings):
        if 'auth' not in settings:
            settings['auth'] = auth
        self.__g = Graph(profile, name, **settings)
        self.__transaction = True
        self.__gt = self.__g.begin()

    def __pre(self):
        if not self.__transaction:
            self.__transaction = True
            self.__gt = self.__g.begin()

    def run(self, cypher, parameters=None, **kwparameters) -> Cursor:
        self.__pre()
        return self.__gt.run(cypher, parameters=parameters, **kwparameters)

    def get_graph(self):
        return self.__g

    def matcher(self) -> NodeMatcher:
        self.__pre()
        return NodeMatcher(self.__gt)

    def relationship_matcher(self) -> RelationshipMatcher:
        self.__pre()
        return RelationshipMatcher(self.__gt)

    def query(self, *labels, **properties) -> NodeMatch:
        return self.matcher().match(*labels, **properties)

    def evaluate_by_id(self, id, label=None):
        if label is None:
            return self.__gt.evaluate(f"MATCH (n) WHERE id(n) = {id} RETURN n")
        return self.__gt.evaluate(f"MATCH (n:{label}) WHERE id(n) = {id} RETURN n")

    def evaluate(self, *label, **properties) -> Node | NodeMatch | Relationship | None:
        self.__pre()
        return self.__gt.evaluate(
            f"MATCH (n:{':'.join(label)}) where {dict_to_str(pre_key='n.', separate='=', **properties)} RETURN n")

    def delete(self, node: Node | NodeMatch | Relationship):
        self.__pre()
        if node is None:
            return False
        self.__gt.delete(node)

    def delete_by_id(self, label, id: int | str):
        self.__pre()
        node = self.__gt.evaluate(f'MATCH (n:{label}) where id(n) = {id} RETURN n')
        return self.delete(node)

    def delete_by_unique_identifier(self, lable, id: int | str, lab_name):
        node = self.evaluate(lable, {f'{lab_name}': id})
        return self.delete(node)

    def add(self, label, **properties):
        match = self.matcher().match(label, **properties)
        if not match.exists():
            p = Node(label, **properties)
            self.create(p)
            return p
        return match.first()

    def create(self, node: Node | NodeMatch | Relationship):
        self.__pre()
        self.__gt.create(node)

    def push(self, node: Node | NodeMatch):
        self.__pre()
        self.__gt.push(node)

    def commit(self):
        if self.__transaction:
            self.__transaction = False
            self.__gt.commit()

    def match(self, nodes=None, r_type=None, limit=None):
        return self.__g.match(nodes, r_type, limit)
