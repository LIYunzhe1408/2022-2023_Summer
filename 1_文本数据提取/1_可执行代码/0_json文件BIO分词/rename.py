import glob
import os
def rename_file(file_path):
    fileList = os.listdir(file_path)
    cnt = 0
    for _ in fileList:
        old_name = file_path + os.sep + fileList[cnt]
        new_name = file_path + os.sep + str(cnt+1) + ".json"
        cnt += 1
        os.rename(old_name, new_name)

file_path = glob.glob("C:/Users/16690/Desktop/Chemi_PDF/导入的txt/*")
for _ in file_path:
    rename_file(file_path)