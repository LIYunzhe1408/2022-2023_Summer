
import graphviz
from myfunc import *
import sys
import pymysql


db = pymysql.connect(host='localhost', user='root', password='123456', database='superalloy', charset="utf8")
cur = db.cursor()
sql_line = "SELECT t.name from data_node t"
cur.execute(sql_line)
res = cur.fetchone()
top_node_name = res[0]
# top_node_name = 'NaSiCON'

db_xai = pymysql.connect(host='localhost', user='root', password='123456', database='xai', charset="utf8")
cur_xai = db_xai.cursor()
sql_line = "SELECT t.entity1_id, t.entity2_id, t.relation " \
           "FROM re_lib t"
cur_xai.execute(sql_line)
relation_library_plain_data = cur_xai.fetchall()
# print(relation_library_plain_data)

sql_line = "SELECT entity_id, entity_content, predicate_content " \
           "FROM en_lib "
cur_xai.execute(sql_line)
entity_tuple = cur_xai.fetchall()
# print(len(entity_tuple))
entity_dict = {num: (str1, str2) for num, str1, str2 in entity_tuple}
# print(entity_dict)
per_article = [[entity_dict[int(num1)][0], entity_dict[int(num2)][0], label, entity_dict[int(num1)][1], entity_dict[int(num2)][1]] for num1, num2, label in relation_library_plain_data]
# print(per_article)

# print(top_node_name)

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

colortype = [('Cause-Effect(e2,e1)', 'red'),
             ('Cause-Effect(e1,e2)', 'red'),
             ('Component-Whole(e1,e2)', 'orange'),
             ('Component-Whole(e2,e1)', 'orange'),
             ('Condition-On(e1,e2)', 'yellow'),
             ('Condition-On(e2,e1)', 'yellow'),
             ('Feature-Of(e1,e2)', 'green'),
             ('Feature-Of(e2,e1)', 'green'),
             ('Instance-Of(e1,e2)', 'blue'),
             ('Instance-Of(e2,e1)', 'blue'),
             ('Located-Of(e1,e2)', 'purple'),
             ('Located-Of(e2,e1)', 'purple'),
             ('Method-Of(e1,e2)', 'pink'),
             ('Method-Of(e2,e1)', 'pink'),
             ('Other', 'grey'), ('Used-For(e1,e2)', 'pink'),
             ('Used-For(e2,e1)', 'pink'),
             ('Property-Of(e1,e2)', 'gold'),
             ('Property-Of(e2,e1)', 'gold')]
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
        # print(per_sentence)
        [sub, obj, rela, pred1, pred2] = per_sentence
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
    # print(per_sentence)
    [sub, obj, rela, pred1, pred2] = per_sentence
    if top_node_name == sub:
        b = pred2
        if b not in basis_node_list:
            basis_node_list.append(b)
    elif top_node_name == obj:
        a = pred1
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
    [s, o, re, pred1, pred2] = per_sentence

    # if re not in rela:
    #     rela.append(re)
    if s == top_node_name:
        fine_grained_node_list.append(o)

        for basis in basis_node_list:
            if pred2 == basis:
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
            if pred1 == basis:
                for i in range(len(colortype)):
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

dot.render('E:\\File\\1_InnovateProj\\front\\src\\assets\\tree', view=False, format='png')
# dot.render('test-output/round-table', view=True, format='png')
# dot.view()