import os
import json
import xlrd2

fileTypeArray = [".xlsx", ".xls"]


def readExcel(path, name):
    workbook = xlrd2.open_workbook(path)
    sheet2_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(sheet2_name)  # sheet索引从0开始
    # sheet的名称，行数，列数
    adict = []
    relation_list = []
    for i in range(1, sheet.nrows):
        data = {}

        for j in range(0, sheet.ncols):
            value = sheet.cell_value(i, j)

            if value != '':
                if value[0] == '{':
                    [subj_char_span_l, subj_char_span_r, predicate1,
                     obj_char_span_l, obj_char_span_r, predicate2, relation] = value.split(',')

                    subj_char_span_l = subj_char_span_l.lstrip('{[')
                    subj_char_span_r = subj_char_span_r.lstrip(' ')
                    subj_char_span_r = subj_char_span_r.rstrip(']')
                    subj_char_span_l = int(subj_char_span_l)
                    subj_char_span_r = int(subj_char_span_r)
                    subject = text[subj_char_span_l:subj_char_span_r+1]
                    subject = subject.lstrip(' ')
                    subject = subject.rstrip(' ')
                    # print([subj_char_span_l, subj_char_span_r])

                    obj_char_span_l = obj_char_span_l.lstrip('{[')
                    obj_char_span_r = obj_char_span_r.lstrip(' ')
                    obj_char_span_r = obj_char_span_r.rstrip(']')
                    obj_char_span_l = int(obj_char_span_l)
                    obj_char_span_r = int(obj_char_span_r)
                    object = text[obj_char_span_l:obj_char_span_r+1]
                    object = object.lstrip(' ')
                    object = object.rstrip(' ')
                    # print([obj_char_span_l, obj_char_span_r])

                    predicate1 = predicate1.rstrip('}')
                    predicate2 = predicate2.rstrip('}')
                    # print([predicate1, predicate2])
                    relation = relation.rstrip('0')
                    for k in range(9, 0, -1):
                        relation = relation.rstrip(str(k))
                    print(relation)
                    relation_list.append({'subject': subject,
                                          'subj_char_span': [subj_char_span_l, subj_char_span_r],
                                          'object': object,
                                          'obj_char_span': [obj_char_span_l, obj_char_span_r],
                                          'predicate1': predicate1,
                                          'predicate2': predicate2,
                                          'relation': relation})
                else:
                    text = data[sheet.cell_value(0, j)] = value
        data['relation_list'] = relation_list
        adict.append(data)
        relation_list = []


    data = json.dumps(adict, indent=1, ensure_ascii=False)
    _json_save_path = os.getcwd() + "/" + name + '.json'
    f = open(_json_save_path, 'w')
    f.write(data)
    f.close()
    print("create json:" + path)
    return data, _json_save_path


if __name__ == '__main__':
    _label_filepath_text = "entity_relation_extraction.xlsx"
    _file_path = _label_filepath_text
    _file_type_list = [".xlsx", ".xls"]
    if _file_path is not None:
        if os.path.isfile(_file_path):
            filesp = os.path.splitext(_file_path)
        for k in _file_type_list:
            if filesp[1] == k:
                filename = os.path.basename(_file_path)
                _json_data = readExcel(_file_path, filename.split('.')[0])
