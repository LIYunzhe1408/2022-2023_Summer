import json
from ast import literal_eval
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher


def MatchNode(graph, label, attrs):
    # 判断图中是否存在该节点
    node_matcher = NodeMatcher(graph)
    # re_value=node_matcher.match(label).where("_.name="+"\'"+attrs+"\'").first()  # 转义字符，这样写的话，实体中的引号需要改成中文格式的
    re_value=node_matcher.match(label,name=attrs).first()                          # 这种写法ok了
    return re_value                                                                # 若存在该节点，则返回符合条件的第一个节点；若不存在，则返回None


def CreateNode(graph, label, attrs):
    # 创建节点
    re_value = MatchNode(graph,label,attrs)
    if re_value is None:
        # 若图中不存在相同标签的节点，则创建并返回新建的节点
        node = Node(label,name=attrs)
        graph.create(node)
        return node
    else:
        # 若存在相同标签的节点，则返回该已有的节点
        return re_value


def CreateRelationship(graph, node1, relation, node2):
    # 创建关系（注意：Relationship()可以自动去重）
    r = Relationship(node1,relation,node2)
    return graph.create(r)


def allnode_query(graph):
    # 查询某节点的所有邻接点
    n = input("请输入要查询的节点名：")

    node_matcher = NodeMatcher(graph)
    node = node_matcher.match(name=n).first()

    relationship_matcher = RelationshipMatcher(graph)
    allnode_relationship = relationship_matcher.match(nodes={node}, r_type=None)
    list(allnode_relationship)
    return allnode_relationship


def headnode_query(graph):
    # 查询以该节点为头节点的子图

    n = input("请输入要查询的节点名：")
    node_matcher = NodeMatcher(graph)
    node = node_matcher.match(name=n).first()

    relationship_matcher = RelationshipMatcher(graph)
    headnode_relationship = relationship_matcher.match(nodes=[node], r_type=None)
    list(headnode_relationship)
    return headnode_relationship


def endnode_query(allnode_relationship, headnode_relationship):
    # 查询以该节点为尾节点的子图
    n = input("请输入要查询的节点名：")

    endnode_relationship = set(allnode_relationship).difference(set(headnode_relationship))
    list(endnode_relationship)


def search_path(graph):
    # 查询任意两个节点之间的通路
    node_matcher = NodeMatcher(graph)
    node1 = node_matcher.match(name='crossslipping').first()
    node2 = node_matcher.match(name='{100} planes').first()

    relationship_matcher = RelationshipMatcher(graph)
    road = relationship_matcher.match(nodes=(node1, node2), r_type=None)
    print(list(road))


def tuples_to_one(tups):
    result = tuple()
    for t in tups:
        result += t
    return result
