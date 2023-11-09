import graphviz
from myfunc import *
import sys
import pymysql


json_info = open('E:\\File\\1_InnovateProj\\py2neo4j-main\\py2neo4j-main\\entity_relation_extraction.json', 'r')
per_article = literal_eval(json_info.read())

db = pymysql.connect(host='localhost', user='root', password='123456', database='superalloy', charset="utf8")
cur = db.cursor()
sql_line = "SELECT t.name from data_node t"
cur.execute(sql_line)
res = cur.fetchone()
# top_node_name = res[0]
top_node_name = "NaSiCON"

print(top_node_name)

dot = graphviz.Digraph(comment='Tree')
dot.attr(compound='True',
         ranksep='2.5',
         rankdir='LR',
         nodesep='0.25',
         fontsize='36',
         fontname="Consolas",
         splines='polyline')   # spline
dot.edge_attr.update(color='royalblue4')
dot.node_attr.update(shape="note",
                     color="seagreen4",
                     fontname="Consolas",
                     fontsize='24')

colortype = [('Cause-Effect', 'red'), ('Component-Whole', 'orange'), ('Condition-On', 'yellow'),
             ('Feature-Of', 'green'), ('Instance-Of', 'blue'), ('Located-Of', 'purple'), ('Method-Of', 'pink'),
             ('Other', 'grey'), ('Used-For', 'pink'), ('Property-Of', 'gold')]
head = [('Located-Of'), ('Used-For')]
back = [('Component-Whole'), ('Feature-Of'), ('Instance-Of'), ('Property-Of')]
# Component-Whole

# Condition-On

# Feature-Of

# Instance-Of

# Located-Of

# Method-Of
NodeList = []
NodeList2 = []
NodeList.append(top_node_name)
basis_node_list = []


# Other
def SearchNode(Node):
    for per_sentence in per_article:
        for per_relationship in per_sentence['relation_list']:
            sub = per_relationship['subject']
            obj = per_relationship['object']
            rela = per_relationship['relation']
            if (Node == sub) and (rela in head) and (obj not in NodeList):
                for j in range(10):
                    if colortype[j][0] == rela:
                        if (sub + ' -> ' + obj) not in dot.source:
                            dot.edge(sub, obj, label=rela, color=colortype[j][1])

                        if obj not in NodeList2:
                            fine_grained_node_list.append(obj)
                            NodeList2.append(obj)
                            SearchNode(obj)
                            j = 0
            if (Node == obj) and (rela in back) and (sub not in NodeList):
                for j in range(10):
                    if colortype[j][0] == rela:
                        dot.edge(obj, sub, label=rela, color=colortype[j][1])

                        if sub not in NodeList2:
                            fine_grained_node_list.append(sub)
                            NodeList2.append(sub)
                            SearchNode(sub)
                            j = 0

    return 0


# dot.node('NASICON_test')
for per_sentence in per_article:
    for per_relationship in per_sentence['relation_list']:
        if top_node_name == per_relationship['subject']:
            b = per_relationship['predicate2']
            if b not in basis_node_list:
                basis_node_list.append(b)
        elif top_node_name == per_relationship['object']:
            a = per_relationship['predicate1']
            if a not in basis_node_list:
                basis_node_list.append(a)
for node in basis_node_list:
    dot.edge(top_node_name, node, label='predicate', color='black')
with dot.subgraph(name='cluster_a') as a:  # 子图
    a.attr(style="rounded",
           label="Basis",
           labelloc="t",
           labeljust="l",
           pencolor="lightsalmon")
    for node in basis_node_list:
        a.node(node)

fine_grained_node_list = []
# rela=[]
for per_sentence in per_article:
    for per_relationship in per_sentence['relation_list']:
        s = per_relationship['subject']
        o = per_relationship['object']
        re = per_relationship['relation']
        # if re not in rela:
        #     rela.append(re)

        if s == top_node_name:
            fine_grained_node_list.append(o)

            for basis in basis_node_list:
                if per_relationship['predicate2'] == basis:
                    for i in range(10):
                        if colortype[i][0] == re and o not in NodeList:
                            NodeList.append(o)

                            dot.edge(basis, o, label=re, color=colortype[i][1])
                            if o not in NodeList2:
                                SearchNode(o)
                                i = 0

        elif o == top_node_name:
            fine_grained_node_list.append(s)
            for basis in basis_node_list:
                if per_relationship['predicate1'] == basis:
                    for i in range(10):
                        if colortype[i][0] == re and s not in NodeList:
                            NodeList.append(s)

                            dot.edge(basis, s, label=re, color=colortype[i][1])
                            if s not in NodeList2:
                                SearchNode(s)
                                i = 0
        '''
        elif o == top_node_name:
            fine_grained_node_list.append(s)
            for basis in basis_node_list:
                if per_relationship['predicate1'] == basis:
                    dot.edge(basis, s)
        '''
# print(rela)
with dot.subgraph(name='cluster_b') as b:
    b.attr(style="rounded",
           label="Fine_grained",
           labelloc="t",
           labeljust="l",
           pencolor="lightsalmon")
    for node in fine_grained_node_list:
        b.node(node)

print(dot.source)

dot.render('../front/src/assets/tree', view=False, format='png')

# dot.view()

