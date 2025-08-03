from flask import Blueprint, request, session
from configurations.key_label_match import rev_name, rev_relationship
from tools.database_neo4j.super_neo4j import DatabaseNeo4j, get_label_name

api = Blueprint('search', __name__)

db = DatabaseNeo4j()


def node_unfold(node):
    node_data = set()
    edge_data = set()
    for item in db.match([node], r_type=None):
        node_data.add((item.end_node.identity, item.end_node.get('name')))
        edge_data.add((node.identity, item.end_node.identity, rev_relationship.get(type(item).__name__), item.identity))
    for item in db.match([None, node], r_type=None):
        node_data.add((item.start_node.identity, item.start_node.get('name')))
        edge_data.add(
            (item.start_node.identity, node.identity, rev_relationship.get(type(item).__name__), item.identity))
    return node_data, edge_data


def format_(s: str):
    return s if len(s) <= 4 else s[:3] + '...'


def format_front(nodes):
    node_data = set()
    edge_data = set()
    for node in nodes:
        node_data.add((node.identity, node.get('name')))
        node_temp, edge_temp = node_unfold(node)
        node_data.update(node_temp)
        edge_data.update(edge_temp)
    return {'nodes': list({'id': item[0], 'label': format_(item[1])} for item in node_data),
            'edges': list(
                {'from': item[0], 'to': item[1], 'label': format_(item[2]), 'id': item[3]} for item in edge_data)}


@api.route('/search', methods=['POST'])
def search():
    label = request.form.get('label')  # especially note the label-name of 'All'
    input_ = request.form.get('input')
    # TODO seek for datas from database
    # print(list(item.get('p') for item in db.run(f"match (p) where p.name contains '{input_}' return p")))
    if label == 'All':
        return format_front(
            list(item.get('p') for item in db.run(f"match (p) where p.name contains '{input_}' return p limit 25")))
    return format_front(
        list(item.get('p') for item in db.run(f"match (p:{label}) where p.name contains '{input_}' return p limit 25")))


@api.route('/down-select', methods=['GET'])
def down_select():
    return rev_name


@api.route('/init', methods=['GET'])
def init():
    print(session.get('uuid'))
    return format_front(item['n'] for item in db.run('MATCH (n) RETURN n LIMIT 25'))


@api.route('/get-node-info/<int:id>', methods=['POST'])
def get_node_info(id):
    print(session.get('uuid'))
    node = db.evaluate_by_id(id=id)
    return {'id': node.identity, **node}


@api.route('/double-click-node/<int:id>', methods=['POST'])
def double_click_node(id):
    return format_front([db.evaluate_by_id(id=id)])


@api.route('/single-click-node/<int:id>', methods=['POST'])
def single_click_node(id):
    print(session.get('uuid'))
    return format_front([db.evaluate_by_id(id=id)])
