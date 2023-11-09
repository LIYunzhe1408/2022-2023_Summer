




# Now done in linux on window virtual machine.



import pdfplumber
import xlwt
import glob
import os
# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('Sheet1')  #添加sheet
i = 0 # Excel起始位置


pdf_path = glob.glob("C:/Users/16690/Desktop/Chemi_PDF/*.pdf")
path = pdf_path[0]
#path = "aaaaaa.PDF"  # 导入PDF路径
pdf = pdfplumber.open(path)
print('\n')
print('开始读取数据')
print('\n')
for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    # print(page.extract_text())
    for table in page.extract_tables():
        # print(table)
        for row in table:
            print(row)
            for j in range(len(row)):
                sheet.write(i, j, row[j])
            i += 1
        print('---------- 分割线 ----------')

pdf.close()

is_existed = os.path.exists("C:/Users/16690/Desktop/Chemi_PDF/pics/")
if not is_existed:
    os.mkdir("C:/Users/16690/Desktop/Chemi_PDF/pics/")
# 保存Excel表
workbook.save('C:/Users/16690/Desktop/Chemi_PDF/pics/PDFresult.xls')
print('\n')
print('写入excel成功')
print('保存位置：')
print('C:/Users/16690/Desktop/Chemi_PDF/*.pdf')
print('\n')

