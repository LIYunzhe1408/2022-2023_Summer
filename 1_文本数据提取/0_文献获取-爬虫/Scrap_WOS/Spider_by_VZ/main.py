import Spider_by_VZ.Main_Methods as pagesToDic
import warnings
import sys

sys.setrecursionlimit(30000)  # 10000为设置的栈大小
warnings.filterwarnings("ignore")

import pickle
import pandas as pd


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def Merge(dict1, dict2):
    dict2.update(dict1)
    return dict2


def toString(list1, key):
    this_string = ""
    if key == 'simply_author_name' or key == 'whole__author_name':
        for i in range(len(list1)):
            this_string += list1[i].replace(',', '') + ","
    else:
        for i in range(len(list1)):
            this_string += list1[i] + ","

    return this_string[:-1]


if __name__ == "__main__":
    # 这是文献所在的url，里面包含验证信息。
    # 先将web of science 检索结果进行翻页一下，以获得最后的page=字符串，
    # 并将此时的连接截取除了最后的数字外，赋值给url——root

    # url_root = "http://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=1&SID=C5d8qVlpdS9z2l55yMW&doc="
    # doc_num = 2802+98 #制定爬到第几个
    # #指定文献信息表格存的路径以及名字
    # # filename = "article_information/machine_learning.paperInfo.csv"
    # filename = "article_information/2801ML_material.paperInfo.csv"

    # #获取文献信息  用字典存储，字典文件备份在Mid_Process_File文件里
    # paper_Dic_Info = pagesToDic.Start_Scarp(root=url_root, nums_page=doc_num, filename=filename)
    #
    # info_dict = paper_Dic_Info
    #
    # columns = ['title','Volume','Issue','Pages','whole__author_name','simply_author_name',	'reprint author','DOI','reprint address','Abstract','Keywords','Document Type','Publisher','Research Domain','Published Date','impact_factor','Keywords_plus','joural','pdf_link',"Download_SuccessOrDefeat"]
    #
    #
    # article_nums = len(info_dict)
    #
    # df = pd.DataFrame(index=range(1, article_nums), columns=columns)
    #
    # for index in info_dict.keys():
    #     for column in info_dict[index].keys():
    #         if (type(info_dict[index][column]) == type([])):
    #             df.loc[index, column] = toString(info_dict[index][column], column)
    #         else:
    #             if column == 'reprint author':
    #                 df.loc[index, column] = info_dict[index][column].replace(',', '')
    #             else:
    #                 df.loc[index, column] = info_dict[index][column]
    #
    # df.to_csv(filename)

    # 这是文献所在的url，里面包含验证信息。
    # 先将web of science 检索结果进行翻页一下，以获得最后的page=字符串，
    # 并将此时的连接截取除了最后的数字外，赋值给url——root
    url_root = "http://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=1&SID=8EYUDHq8nCId19cNlZW&doc="

    doc_num = 17700
    start_num = 17601
    cnt = 5
    i = 0
    while i <= cnt:
        if i == 0:
            start_num = start_num + 100 * 0
            doc_num = doc_num + 100 * 0
        else:
            start_num = start_num + 100
            doc_num = doc_num + 100

        # 指定文献信息表格存的路径以及名字
        filename = "article_information/" + str(start_num) + "ML_material.paperInfo.csv"

        # 获取文献信息  用字典存储，字典文件备份在Mid_Process_File文件里
        paper_Dic_Info = pagesToDic.Start_Scarp(root=url_root, nums_page=doc_num, filename=filename,
                                                start_num=start_num)
        info_dict = paper_Dic_Info

        # 获取信息的列名
        columns = ['title', 'Volume', 'Issue', 'Pages', 'whole__author_name', 'simply_author_name', 'reprint author',
                   'DOI', 'reprint address', 'Abstract', 'Keywords', 'Document Type', 'Publisher', 'Research Domain',
                   'Published Date', 'impact_factor', 'Keywords_plus', 'joural', 'pdf_link', "Download_SuccessOrDefeat"]

        article_nums = len(info_dict)

        df = pd.DataFrame(index=range(1, article_nums), columns=columns)
        for index in info_dict.keys():
            for column in info_dict[index].keys():
                if type(info_dict[index][column]) == type([]):
                    df.loc[index, column] = toString(info_dict[index][column], column)
                else:
                    if column == 'reprint author':
                        df.loc[index, column] = info_dict[index][column].replace(',', '')
                    else:
                        df.loc[index, column] = info_dict[index][column]

        df.to_csv(filename)
        i += 1
        print("------------------------------------------")
