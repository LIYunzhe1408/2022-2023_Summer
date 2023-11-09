# from myfunc import *
import neo4jupyter
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher
from IPython.core.display import display, Javascript
import pymysql
from ast import literal_eval
import json
import os

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

if __name__ == "__main__":
    # 读入json
    json_info = open('E:\\File\\1_InnovateProj\\py2neo4j-main\\py2neo4j-main\\entity_relation_extraction.json', 'r')
    per_article = literal_eval(json_info.read())

    # 连接数据库
    # graph=Graph('http://localhost:7474/',auth=('neo4j','Zhen010809'))#correct
    graph = Graph('bolt://localhost:7687', auth=('neo4j', '123'))

    # 创建节点和关系
    for per_sentence in per_article:
        for per_relationship in per_sentence['relation_list']:
            node1 = CreateNode(graph, per_relationship['predicate1'], per_relationship['subject'])  # 创建头节点
            node2 = CreateNode(graph, per_relationship['predicate2'], per_relationship['object'])   # 创建尾节点
            CreateRelationship(graph, node1, per_relationship['relation'], node2)                   # 创建关系

    # db = pymysql.connect(host='localhost', user='root', password='123456', database='superalloy', charset="utf8")
    # cur = db.cursor()
    # sql = "SELECT t.name from data_node t"
    # cur.execute(sql)
    # res = cur.fetchone()
    # name = res[0]

    # gql = "MATCH c=(cf)-[r]->(ct) WHERE ct.name="+"\"" + name + "\""+" OR cf.name="+"\"" + name + "\""+" RETURN c"
    opt = {"Composition":"name",
           "Structure":"name",
           "Application":"name",
           "Condition":"name",
           "Feature":"name",
           "Processing":"name",
           "Property":"name",
           "Characterization":"name"}
    gql = "MATCH c=(cf)-[r]->(ct) RETURN c LIMIT 50"
    s = graph.run(gql).to_subgraph()

    neo4jupyter.init_notebook_mode()
    src = neo4jupyter.draw_subgraph(subgraph=s, options=opt).data

    xx = src.split("\n")
    x = xx[4]
    y = xx[5]

    data_nodes = x.replace("var nodes = ", "")
    data_nodes = data_nodes.rstrip(";")

    data_edges = y.replace("var edges = ", "")
    data_edges = data_edges.rstrip(";")

    print(data_nodes)
    print(data_edges)


    """
    n = input("请输入要查询的节点名：")
    graph2 = Graph('bolt://localhost:7687', auth=('neo4j', '20021107'))
    # graph2.run("USE sub")
    graph2.run("match (n) detach delete n")
    for per_sentence in per_article:
        for per_relationship in per_sentence['relation_list']:
            s = per_relationship['subject']
            o = per_relationship['object']
            if s == n or o == n:
                node1 = CreateNode(graph2, per_relationship['predicate1'], per_relationship['subject'])  # 创建头节点
                node2 = CreateNode(graph2, per_relationship['predicate2'], per_relationship['object'])   # 创建尾节点
                CreateRelationship(graph2, node1, per_relationship['relation'], node2)                   # 创建关系

    # 输出两节点间多个关系的节点
    # walk(relationship) 返回一个生成器包含起始node、关系本身、终止node
    relationship_list = []
    number = 0
    for per_sentence in per_article:
        for per_relationship in per_sentence['relation_list']:
            # print(per_relationship)
            temp = per_relationship
            temp['num'] = number  # number:第几句，编号从0开始
            relationship_list.append(temp)
        number = number+1
    # print(relationship_list)

    error_relationship_list = []
    number = 1
    # now = 0
    for i in relationship_list:
        subject1 = i['subject']
        object1 = i['object']
        # print(relationship_list.index(i))
        # for j in relationship_list[now+1:]:
        for j in relationship_list:
            if i != j:
                subject2 = j['subject']
                object2 = j['object']
                if subject1 == object2 and object1 == subject2:
                    print(number)
                    print("句子1：", i['num'], per_article[i['num']]['text'])
                    print("关系：", subject1, "----", i["predicate"], "--->", object1, '\n')
                    print("句子2：", j['num'], per_article[j['num']]['text'])
                    print("关系：", subject2, "----", i["predicate"], "--->", object2)
                    print("=====================================================================")
                    number = number + 1
    """