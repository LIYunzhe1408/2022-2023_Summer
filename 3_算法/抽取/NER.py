"""
In:
    [inline]file: data_aug.csv. build corpus
    directory: ./result_literatures  txt files in this directory are needed to extract.
Out:
    file: test_lyz_knowledge_base_with_tag.xlsx
    terminal: prompt info
"""
import argparse
import numpy as np
from pytorch_transformers import BertPreTrainedModel, BertModel, BertTokenizer
import torchcrf as CRF
import pandas as pd
import os
import re
from nltk import sent_tokenize
import warnings

warnings.filterwarnings('ignore')
import torch

torch.cuda.set_device(0)
import torch.nn as nn


def build_corpus1(data_dir):
    """获得句子及标签信息"""
    word_lists = []
    tag_lists = []
    words = []
    tags = []
    data = pd.read_csv(data_dir, header=None, encoding='utf-8')
    word = data.iloc[:, 0]
    tag = data.iloc[:, 2]
    for i in range(len(word)):
        if word[i] != " ":
            words.append(word[i])
            tags.append(tag[i])
        elif word[i] == " ":
            word_lists.append(words)
            tag_lists.append(tags)
            words = []
            tags = []
    return word_lists, tag_lists


def build_corpus2(data_dir):
    word_lists = []
    tag_lists = []
    with open(data_dir, "r", encoding="utf-8") as f:
        words = []
        tags = []
        for line in f:
            if line != "\n":
                word = line.split(" ")[0]
                tag = line.split(" ")[1].strip("\n")
                words.append(word)
                tags.append(tag)
            else:
                word_lists.append(words)
                tag_lists.append(tags)
                words = []
                tags = []

    return word_lists, tag_lists


class BERT_BiLSTM_CRF(BertPreTrainedModel):
    def __init__(self, config, need_birnn=False, rnn_dim=128):
        super(BERT_BiLSTM_CRF, self).__init__(config)

        self.num_tags = config.num_labels
        self.bert = BertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        out_dim = config.hidden_size
        self.need_birnn = need_birnn

        # 如果为False，则不要BiLSTM层
        if need_birnn:
            self.birnn = nn.LSTM(config.hidden_size, rnn_dim, num_layers=1, bidirectional=True, batch_first=True)
            out_dim = rnn_dim * 2

        self.hidden2tag = nn.Linear(out_dim, config.num_labels)
        self.crf = CRF(config.num_labels, batch_first=True)

    def forward(self, input_ids, tags=None, token_type_ids=None, input_mask=None):
        outputs = self.bert(input_ids, token_type_ids=token_type_ids, attention_mask=input_mask)
        sequence_output = outputs[0]
        if self.need_birnn:
            sequence_output, _ = self.birnn(sequence_output)

        sequence_output = self.dropout(sequence_output)
        emissions = self.hidden2tag(sequence_output)

        outputs = (emissions,) + outputs[2:]
        if tags is not None:
            loss = -1 * self.crf(emissions, tags, mask=input_mask.byte())
            outputs = (loss,) + outputs

        return outputs


def add_new_sent_to_knowledge(sent):
    all_sentences = []
    try:
        tokenized_sentence = tokenizer.encode(sent)
        input_ids = torch.LongTensor([tokenized_sentence])
        input_ids = input_ids.to(device)
        with torch.no_grad():
            output = model(input_ids, tags=None)
        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
        # join bpe split tokens
        tokens = tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        new_tokens, new_labels = [], []
        for token, label_idx in zip(tokens, label_indices[0]):
            if token.startswith("##"):
                new_tokens[-1] = new_tokens[-1] + token[2:]
            else:
                new_labels.append(tag_values[label_idx])
                new_tokens.append(token)

        tmp_test = [new_tokens, new_labels]
        now_sentence = " ".join(tmp_test[0])
        descriptor_index = []
        for i in range(len(tmp_test[0])):
            if tmp_test[1][i][0] == "B":
                descriptor_index.append(i)
        descriptor_index.append(len(tmp_test[0]))
        descriptor = []
        descriptor_type = []
        for i in range(len(descriptor_index) - 1):
            type_ = tmp_test[1][descriptor_index[i]].split("-")[-1]
            descriptor_type.append(type_)
            descriptor_word = []
            for j in range(descriptor_index[i], descriptor_index[i + 1]):
                if tmp_test[1][j][0] != "O":
                    descriptor_word.append(tmp_test[0][j])
            descriptor.append(descriptor_word)
        descriptors = [" ".join(d) for d in descriptor]
        for i in range(len(descriptors)):
            if descriptors[i] not in knowledge[descriptor_type[i]]:
                knowledge[descriptor_type[i]][descriptors[i]] = [now_sentence]
            else:
                knowledge[descriptor_type[i]][descriptors[i]].append(now_sentence)
        all_sentences.append(now_sentence)
        return all_sentences
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputData', type=str, default=None)
    parser.add_argument('--lastID', type=str, default=None)
    args = parser.parse_args()
    lastID = args.lastID
    print(lastID)
    if lastID == "null":
        lastID = 0

    # if args.inputData == "1":
    print("===============================================")
    print("================Loading model==================")
    print("===============================================")
    # 参数设置
    model_name = "bert-base-cased"
    checkpoint_path = "add-lstm-crf-checkpoint.cpt"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    df = pd.read_csv("./data_aug.csv", header=None, encoding="utf-8")
    sentences, labels = build_corpus1("./data_aug.csv")

    # Ours 数据集
    tag_values = list(set(df.iloc[:, 2].values))
    tag_values.append("PAD")
    tag_values.remove(" ")
    tag2idx = {t: i for i, t in enumerate(tag_values)}
    tokenizer = BertTokenizer.from_pretrained(model_name, do_lower_case=False)

    torch.cuda.empty_cache()
    model = torch.load(checkpoint_path)

    # 获取所有txt格式文献
    dir_all = "./result_literatures/"
    all_text_name_list = []
    for home, dirs, files in os.walk(dir_all):
        for filename in files:
            if filename == args.inputData:
                fullname = os.path.join(home, filename)
                all_text_name_list.append(fullname)
    # all_text_name_list = all_text_name_list[:20]

    #
    sigle_sent = []
    remove_xkh = r"[(](.*)[)]"
    remove_zkh = r"[\[](.*)[\]]"
    remove_dkh = r"[\{](.*)[\}]"
    remove_ex1 = r"[\d\)]"

    # 处理文本得到单个句子列表
    count = 0
    for file in all_text_name_list:
        try:
            with open(file, "r", encoding="utf-8") as f:
                raw_sent_lines = f.readlines()
                sent_size = len(raw_sent_lines)
                # print(sent_size)
                index = 0
                cur_sent = ""
                while index < sent_size:
                    cur = raw_sent_lines[index].strip()
                    # print(cur)
                    # print(index)

                    # TODO 如果最后一行没有换行，就会报错，无法得到句子列表，判断逻辑有问题
                    if cur != "":
                        # print("hahahahahahah")
                        cur_sent += (cur + " ")
                        index += 1
                    else:
                        index += 1

                    if cur == "" and cur_sent != "" or index == sent_size - 1:
                        # print("jhkjhkgjfcgc")
                        cur_sent_list = sent_tokenize(cur_sent.strip())
                        sigle_sent.extend(cur_sent_list)
                        cur_sent = ""
                        index += 1

                count += 1
                print(file + " ======>已完成!")
        except:
            pass
    print("-------------------------------------------------------")
    print("Total literature numbers is ", count)
    # print(sigle_sent)
    result_sent = []
    for sent in sigle_sent:
        if len(sent.split(" ")) <= 8:
            continue
        new_sent1 = re.sub(remove_xkh, '', sent)
        new_sent2 = re.sub(remove_zkh, '', new_sent1)
        new_sent3 = re.sub(remove_dkh, '', new_sent2)
        new_sent4 = re.sub(remove_ex1, '', new_sent3)
        result_sent.append(new_sent4)
    knowledge = {"Composition": {}, "Structure": {}, "Property": {}, "Processing": {},
                 "Feature": {}, "Application": {}, "Characterization": {}, "Condition": {}}

    all_sentences = []
    for sent in result_sent:
        all_sentences.append(add_new_sent_to_knowledge(sent))

    df_sentences = pd.DataFrame(all_sentences)
    name = "./NER_result/" + args.inputData + "_all_sentences.csv"
    df_sentences.to_csv(name, encoding='utf-8', index=False, header=False)

    save_result_with_tag = []
    save_result = []
    classification_count = 0
    count_dict = {"Composition": '', "Structure": '', "Property": '', "Processing": '',
                  "Feature": '', "Application": '', "Characterization": '', "Condition": ''}
    total_cnt = 1
    for k in knowledge.keys():
        classification_count = 0
        for key, value in knowledge[k].items():
            for i in range(len(value)):
                save_result_with_tag.append([key, value[i], int(lastID) + total_cnt, k])
                classification_count += 1
                save_result.append([key, value[i], int(lastID) + total_cnt])
                total_cnt += 1
        count_dict[k] = classification_count
        print(k, ": ", count_dict[k])
    # for i in knowledge.keys():
    #     save_result_with_tag.append([i, count_dict[i]])
    print("-------------------------------------------------------")
    print("Total sentences' numbers is ", len(save_result_with_tag))
    df_new_base_with_tag = pd.DataFrame(save_result_with_tag)
    df_new_base = pd.DataFrame(save_result)

    name = "./NER_result/" + args.inputData + "_test_knowledge_base.csv"
    df_new_base.to_csv(name, encoding='utf-8', index=False, header=False)
    name = "./NER_result/" + args.inputData + "_test_knowledge_base_with_tag.xlsx"
    df_new_base_with_tag.to_excel(name, encoding='utf-8', index=False, header=False)
