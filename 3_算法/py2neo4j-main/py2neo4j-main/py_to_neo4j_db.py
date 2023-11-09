# from myfunc import *
import neo4jupyter
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import pymysql
import json
import os
from IPython.display import HTML, Javascript, display
import uuid


def MatchNode(graph, label, attrs):
    # 判断图中是否存在该节点
    node_matcher = NodeMatcher(graph)
    # re_value=node_matcher.match(label).where("_.name="+"\'"+attrs+"\'").first()  # 转义字符，这样写的话，实体中的引号需要改成中文格式的
    re_value = node_matcher.match(label, name=attrs).first()  # 这种写法ok了
    return re_value  # 若存在该节点，则返回符合条件的第一个节点；若不存在，则返回None


def CreateNode(graph, label, attrs):
    # 创建节点
    re_value = MatchNode(graph, label, attrs)
    # print(re_value)
    if re_value is None:
        # 若图中不存在相同标签的节点，则创建并返回新建的节点
        node = Node(label, name=attrs)
        graph.create(node)
        return node
    else:
        # 若存在相同标签的节点，则返回该已有的节点
        return re_value


def CreateRelationship(graph, node1, relation, node2):
    # 创建关系（注意：Relationship()可以自动去重）
    r = Relationship(node1, relation, node2)
    return graph.create(r)

'''
Get from https://github.com/merqurio/neo4jupyter/blob/master/neo4jupyter.py
'''
def get_vis_edge_info(r):
    return ({"from": r.start_node.identity, "to": r.end_node.identity, "label": r.__class__.__name__})

'''
Get from https://github.com/merqurio/neo4jupyter/blob/master/neo4jupyter.py
'''
##calculate the dict that will represent a node.
def get_vis_node_info(node, options):
    node_label = list(node.labels)[0]
    prop_key = options.get(node_label)
    vis_label = dict(node).get(prop_key, "")

    return {"id": node.identity, "label": vis_label, "group": node_label, "title": repr(node)}

'''
Get from https://github.com/merqurio/neo4jupyter/blob/master/neo4jupyter.py
'''
def vis_network(nodes, edges, physics=True):
    """
    Creates the HTML page with all the parameters
    :param nodes: The nodes to be represented an their information.
    :param edges: The edges represented an their information.
    :param physics: The options for the physics of vis.js.
    :return: IPython.display.HTML
    """
    base = open(os.path.join(os.path.dirname(__file__), 'assets/index.html')).read()

    unique_id = str(uuid.uuid4())
    html = base.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    return HTML(html)


if __name__ == "__main__":
    # Connect to Neo4J.
    graph = Graph('bolt://localhost:7687', auth=('neo4j', '123'))
    graph.run("match (n) detach delete n")

    # Connect to MySQL.
    db_xai = pymysql.connect(host='localhost', user='root', password='123456', database='xai', charset="utf8")
    cur_xai = db_xai.cursor()

    # Prepare SQL statements.
    sql_line_for_relation = "SELECT t.entity1_id, t.entity2_id, t.relation " \
                            "FROM test_re_lib t"
    cur_xai.execute(sql_line_for_relation)
    relation_library_plain_data = cur_xai.fetchall()

    sql_line_for_entity = "SELECT entity_id, entity_content, predicate_content " \
                          "FROM en_lib "

    cur_xai.execute(sql_line_for_entity)
    entity_tuple = cur_xai.fetchall()

    # Prepare corpus
    entity_dict = {num: (str1, str2) for num, str1, str2 in entity_tuple}
    per_article = [[entity_dict[int(num1)][0], entity_dict[int(num2)][0], label, entity_dict[int(num1)][1],
                    entity_dict[int(num2)][1]] for
                   num1, num2, label in relation_library_plain_data]

    # Create Node and Relationship
    for per_sentence in per_article:
        [sub, obj, rela, pred1, pred2] = per_sentence
        node1 = CreateNode(graph, pred1, sub)  # < Create start node.
        node2 = CreateNode(graph, pred2, obj)  # < Create end node.
        CreateRelationship(graph, node1, rela, node2)  # < Create relationship.

    # Options for parameter in getting nodes and edges.
    opt = {"Composition": "name",
           "Structure": "name",
           "Application": "name",
           "Condition": "name",
           "Feature": "name",
           "Processing": "name",
           "Property": "name",
           "Characterization": "name",
           "Other": "name"}

    # Cypher Statement to get specific nodes.
    gql = "MATCH c=(cf)-[r]->(ct) RETURN c limit 50"
    s = graph.run(gql).to_subgraph()

    # Get nodes with Label, ID, group and edges with from_node, to_node and label.
    nodes = [get_vis_node_info(n, opt) for n in s.nodes]
    edges = [get_vis_edge_info(r) for r in s.relationships]
    src = vis_network(nodes, edges, physics=True).data

    # Split the javascript statements.
    split_sentence = src.split("\n")

    nodes_set = split_sentence[4]
    edges_set = split_sentence[5]

    # Clean up.
    data_nodes = nodes_set.replace("var nodes = ", "")
    data_nodes = data_nodes.rstrip(";")

    data_edges = edges_set.replace("var edges = ", "")
    data_edges = data_edges.rstrip(";")

    print(data_nodes)
    print(data_edges)

    # There's a bug in draw_subgraph. The id of end_node will be changed and different from the id in normal node.
    # neo4jupyter.init_notebook_mode()
    # src = neo4jupyter.draw_subgraph(subgraph=s, options=opt).data
