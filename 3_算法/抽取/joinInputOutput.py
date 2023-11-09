import pandas as pd
import os
csv_path = "E:\\File\\1_InnovateProj\\Algorithm\\RE\\eval\\flag.tsv"
if os.path.exists(csv_path):
    os.remove(csv_path)
tsv_path = "E:\\File\\1_InnovateProj\\Algorithm\\RE/data_RE/test/lyz_test_not_for_re.tsv"
txt_path = "E:\\File\\1_InnovateProj\\Algorithm\\RE/eval/lyz_proposed_answers.txt"
if os.path.exists("E:\\File\\1_InnovateProj\\Algorithm\\RE\\jointInOut.tsv"):
    os.remove("E:\\File\\1_InnovateProj\\Algorithm\\RE\\jointInOut.tsv")

input_data = pd.read_csv(tsv_path, sep='\t', header=None)
# relation, sentence, entity1_id, entity2_id
output_data = pd.read_table(txt_path, sep='\t', header=None)

# Write to test.tsv
for i in range(len(input_data)):
    with open("E:\\File\\1_InnovateProj\\Algorithm\\RE\\jointInOut.tsv", 'a', encoding='utf-8') as f1:
        f1.write(output_data.values[i][1])
        f1.write("\t")
        f1.write(input_data.values[i][1])
        f1.write("\t")
        f1.write(str(input_data.values[i][2]) + "\t" + str(input_data.values[i][3]) +"\n")
f1.close()
with open(csv_path, 'a', encoding='utf-8') as f1:
    f1.write("flag")
f1.close()
