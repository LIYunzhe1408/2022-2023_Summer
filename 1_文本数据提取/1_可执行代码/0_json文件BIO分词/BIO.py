
import pandas as pd
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from chemdataextractor.nlp.tokenize import ChemWordTokenizer,ChemSentenceTokenizer
import glob
import shutil
# nltk.download()

# 给json重命名以适应下个函数
def rename_file(file_path):
    fileList = os.listdir(file_path)
    cnt = 1
    for _ in fileList:
        old_name = file_path + os.sep + fileList[cnt]
        new_name = file_path + os.sep + str(cnt) + ".json"
        cnt += 1
        os.rename(old_name, new_name)


def prepare_json(file_path):
    word_list = []
    #     json_list = []
    alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # 获取file_path路径下所有json文件并按照序号排列
    for path, _, files in os.walk(file_path):
        json_num = []
        sorted_json = []

        for j in files:
            json_num.append(int(j.split(".")[0]))
        for num in sorted(json_num):
            sorted_json.append(str(num) + ".json")
        json_list = [os.path.join(path, file) for file in sorted_json]

    # 对每个json文件进行单词与标签的对应
    for json in json_list:
        words = []
        span = []
        tag = []
        # 读取数据
        data = pd.read_json(json, orient='records')
        # 每个json分句["第一句"，"第二句"]
        sent = ChemSentenceTokenizer().tokenize(data["content"][0])
        # 每个句子进行分词
        for s in sent:
            words.append(ChemWordTokenizer().tokenize(s))

        for i in range(len(data)):
            onlyalph = []
            # 设置标签类别，用以后续匹配
            prepare_tag_char = ["Characterization"]
            prepare_tag_feature = ["Feature"]
            prepare_tag_condition = ["Condition"]
            prepare_tag_appli = ["Application"]
            prepare_tag_proc = ["Processing"]
            prepare_tag_pro = ["Property_Behavior"]
            prepare_tag_str = ["Structure"]
            prepare_tag_compo = ["Composition"]

            span.append(data["records"][i]["span"].strip())
            # 遍历，并和上述准备的标签匹配
            for s in data["records"][i]["tag"]:
                if s in alph:
                    onlyalph.append(s)
            if ("".join(onlyalph)) in prepare_tag_pro:
                tag.append("property&behavior")
            elif ("".join(onlyalph)) in prepare_tag_str:
                tag.append("structure")
            elif ("".join(onlyalph)) in prepare_tag_char:
                tag.append("characterization")
            elif ("".join(onlyalph)) in prepare_tag_feature:
                tag.append("feature")
            elif ("".join(onlyalph)) in prepare_tag_condition:
                tag.append("condition")
            elif ("".join(onlyalph)) in prepare_tag_appli:
                tag.append("application")
            elif ("".join(onlyalph)) in prepare_tag_proc:
                tag.append("processing")
            elif ("".join(onlyalph)) in prepare_tag_compo:
                tag.append("composition")
            else:
                tag.append("".join(onlyalph))

        # 临时存储标记了的单词与对应的标签
        span_word2tag = {" ": " "}
        for j in range(len(span)):
            if len(span[j].split(" ")) == 1:
                span_word2tag[span[j]] = "B-" + tag[j].capitalize()
            elif len(span[j].split(" ")) > 1:
                for m in range(len(span[j].split(" "))):
                    if m == 0:
                        span_word2tag[span[j].split(" ")[m]] = "B-" + tag[j].capitalize()
                    else:
                        span_word2tag[span[j].split(" ")[m]] = span_word2tag.get(span[j].split(" ")[m],
                                                                                 "I-" + tag[j].capitalize())
        for word in words:
            tag_list = []
            word.append(" ")
            for w in range(len(word)):
                tag_list.append(span_word2tag.get(word[w], "O"))
            word_list.append([word, tag_list])
    return word_list








# file_path = "C:/Users/16690/Desktop/Chemi_PDF/导入的txt/1.Internal short circuit detection in Li-ion batteries using supervised machine learning/DatasetId_291477_1640772546"
# file_path =  r"D:\jupyter notebook\material_nlp\material_ner\data"
# file_path = r"D:\jupyter notebook\material_nlp\material_ner\data\DatasetId_150389_1611229435"
# file_path = r"D:\研究生\材料文本挖掘\NASICON体系命名实体识别\已标注数据\数据\张俊伟\文献标注\DatasetId_154355_1612365067"
# file_path = r"D:\jupyter notebook\material_nlp\material_ner\data\DatasetId_145106_1612427291"



# give_number(file_path)


path_list = glob.glob("C:/Users/16690/Desktop/Chemi_PDF/4_json/*")
# print(file_path[0])
# path_list= []
#
# for path,folder,files in os.walk(file_path):
#     path_list.append(path)

# path_list.pop(0)
print(path_list[0])
for dir_num in range(len(path_list)):
    data = prepare_json(path_list[dir_num])
    for i in range(len(data)):
        name_entities = list(zip(data[i][0], data[i][1]))
        df = pd.DataFrame(name_entities, columns=['Entity Name', 'Entity Type'])
        df.to_csv("C:/Users/16690/Desktop/Chemi_PDF/" + path_list[dir_num][40:] +".csv", mode="a", encoding="utf-8", index=False, header=False)



# prepare_json(file_path)
