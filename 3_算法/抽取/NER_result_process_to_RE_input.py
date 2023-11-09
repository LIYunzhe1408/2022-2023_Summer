print(280/55)
# import argparse
# import re
# import os
# import pandas as pd
# import enchant
# import glob
# # x_path = "E:\\File\\1_InnovateProj\\Algorithm\\RE\\eval\\flag.tsv"
# # if os.path.exists(x_path):
# #     os.remove(x_path)
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--inputData', type=str, default=None)
# args = parser.parse_args()
# filename = args.inputData
#
# tsv_path = "./RE/data_RE/test/lyz_test.tsv"
# csv_path = "./RE/data_RE/test/lyz_test_not_for_re.tsv"
# if os.path.exists(tsv_path):
#     os.remove(tsv_path)
# if os.path.exists(csv_path):
#     os.remove(csv_path)
#
# d = enchant.Dict("en_US")
# # TODO need to traverse
# path = './NER/NER_result/' + filename + '.txt_test_knowledge_base.csv'
# NER_results = glob.glob(path)
# print(NER_results)
# for NER_result in NER_results:
#     print("Processing ", NER_result)
#     raw_ner_result = pd.read_csv(NER_result, header=None, encoding='utf-8')
#     # raw_ner_result = pd.read_csv('./NER/NER_result/304.txt_test_knowledge_base.csv', header=None, encoding='utf-8')
#
#     filter_list = []
#     for i in range(len(raw_ner_result)):
#         now_word_list = str(raw_ner_result.iloc[i, 0]).split(" ")
#
#         count = 0
#         for j in range(len(now_word_list)):
#             if d.check(now_word_list[j]):
#                 count += 1
#
#         if count == len(now_word_list):
#             # TODO add column entity_id here
#             # 0 is entity with tag, 1 is sentence, 2 is entity_id
#             filter_list.append([raw_ner_result.iloc[i, 0], raw_ner_result.iloc[i, 1], raw_ner_result.iloc[i, 2]])
#     # print(len(filter_list))
#     # print(filter_list)
#     df_list = []
#     for ele in filter_list:
#         if ele[0] in df_list:
#             continue
#         else:
#             df_list.append(ele[0])
#     df = pd.DataFrame(df_list)
#     # df.to_csv("./material_knowledge.csv", header=None, index=None, encoding='utf-8')
#     filter_list_df = pd.DataFrame(filter_list)
#     print(filter_list_df)
#
#
#     ##############################
#     merge_entity = {}
#     for i in range(len(filter_list_df)):
#         now_sent = str(filter_list_df.iloc[i, 1]).split(" ")
#         old_len = len(now_sent)
#         last_word = now_sent.pop()
#         new_len = len(now_sent)
#         assert old_len - 1 == new_len
#
#         if last_word != "." or "." in now_sent or new_len <= 8:
#             continue
#
#         if filter_list_df.iloc[i, 1] not in merge_entity:
#             merge_entity[filter_list_df.iloc[i, 1]] = [filter_list_df.iloc[i, 0] + "[" + str(filter_list_df.iloc[i, 2]) +"]"]
#             # TODO add entity_id
#         else:
#             merge_entity[filter_list_df.iloc[i, 1]].append(filter_list_df.iloc[i, 0] + "[" + str(filter_list_df.iloc[i, 2]) +"]")
#             # TODO add entity_id
#     # print(merge_entity)
#     # Prepare for write out.
#     pre_sent = []
#     pre_id = []
#     for idx, (sent, entity_list) in enumerate(merge_entity.items()):
#         entities = list(set(entity_list))
#         # print(entities)
#
#         if len(entities) < 2:
#             continue
#         else:
#             entities_content_temp = []
#             temp = []
#             entities_id = []
#             for i in range(len(entities) - 1):
#                 for j in range(i + 1, len(entities)):
#                     temp.append((entities[i], entities[j]))
#
#             for t in range(len(temp)):
#                 try:
#                     # print("------------")
#                     id_temp = (temp[t][0][temp[t][0].index("[")+1:temp[t][0].index("]")], temp[t][1][temp[t][1].index("[")+1:temp[t][1].index("]")])
#                     content_temp = (temp[t][0][:temp[t][0].index("[")], temp[t][1][:temp[t][1].index("[")])
#                     # print(id_temp)
#                     # print(content_temp)
#                     temp[t] = content_temp
#
#
#                     h0, h1 = sent.index(temp[t][0]), sent.index(temp[t][-1])
#                     t0, t1 = h0 + len(temp[t][0]) + 1, h1 + len(temp[t][-1]) + 1
#                     # print(sent)
#                     # print(h0, h1, t0, t1)
#
#                     if h0 > h1:
#                         e1_sent = sent[0:h0] + "<e2>" + temp[t][0] + "</e2> " + sent[t0:]
#                         e2_sent = e1_sent[0:h1] + "<e1>" + temp[t][-1] + "</e1> " + e1_sent[t1:]
#                         # print(e2_sent)
#                         pre_sent.append(e2_sent)
#                         pre_id.append((id_temp[1],id_temp[0]))
#                     else:
#                         e2_sent = sent[0:h1] + "<e2>" + temp[t][-1] + "</e2> " + sent[t1:]
#                         e1_sent = e2_sent[0:h0] + "<e1>" + temp[t][0] + "</e1> " + e2_sent[t0:]
#                         # print(e1_sent)
#                         pre_sent.append(e1_sent)
#                         pre_id.append((id_temp[0], id_temp[1]))
#                 except:
#                     continue
#         # print(pre_sent)
#         # print(pre_id)
#         break
#     for ele in pre_sent:
#         id_index = pre_sent.index(ele)
#         if "<e1>" not in ele:
#             pre_sent.remove(ele)
#             pre_id.remove(pre_id[id_index])
#             continue
#         elif "</e1>" not in ele:
#             pre_sent.remove(ele)
#             pre_id.remove(pre_id[id_index])
#             continue
#         elif "<e2>" not in ele:
#             pre_sent.remove(ele)
#             pre_id.remove(pre_id[id_index])
#             continue
#         elif "</e2>" not in ele:
#             pre_sent.remove(ele)
#             pre_id.remove(pre_id[id_index])
#             continue
#
#     # Write to test.tsv
#     for i in range(len(pre_sent)):
#         with open("./RE/data_RE/test/lyz_test.tsv", 'a', encoding='utf-8') as f:
#             f.write("Other")
#             f.write("\t")
#             f.write(pre_sent[i] + "\n")
#         with open("./RE/data_RE/test/lyz_test_not_for_re.tsv", 'a', encoding='utf-8') as f1:
#             f1.write("Other")
#             f1.write("\t")
#             f1.write(pre_sent[i])
#             f1.write("\t")
#             f1.write(str(pre_id[i][0]) + "\t" + str(pre_id[i][1][:]) +"\n")
#     print("------------------------------------------------------")
# f.close()
# f1.close()
# print(os.getcwd())
# # with open(x_path, 'a', encoding='utf-8') as f1:
# #     f1.write("flag")
# # f1.close()
