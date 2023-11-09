# encoding: utf-8
import sys
import importlib
importlib.reload(sys)

from pdfminer3.pdfparser import PDFParser,PDFDocument
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.layout import LTTextBoxHorizontal,LAParams, LTTextBox, LTTextLine
from pdfminer3.pdfinterp import PDFTextExtractionNotAllowed

import glob

# path = "C:/Users/16690/Desktop/Chemi_PDF/Internal short circuit detection in Li-ion batteries using supervised machine learning.pdf"


# Provide a key. No need now.
# doc.initialize()

def parse(path, filename):
        fp = open(path, 'rb')
        # Create a parser with one file.
        praser = PDFParser(fp)
        # Create a PDFDocument.
        doc = PDFDocument()
        # Connect parser with document.
        praser.set_document(doc)
        doc.set_parser(praser)

        # Create one manager.
        rsrcmgr = PDFResourceManager()
        # PDF Device.
        laparams = LAParams()
        # 创建聚合器,用于读取文档的对象PDFPageAggregator
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # Create one PDFPageInterpreter
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # One page at a time
        page_num = 1
        for page in doc.get_pages():  # Get pages amount
            # Read single page

            print("Curent Page  is: %s \n" % page_num)
            interpreter.process_page(page)
            layout = device.get_result()
            page_num += 1
            for x in layout:
                if isinstance(x, LTTextBox) or isinstance(x, LTTextLine):
                    save_path = 'C:/Users/16690/Desktop/Chemi_PDF/test/' + filename + '.txt'
                    with open(save_path, 'a', encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results + '\n')


if __name__ == '__main__':

    pdf_path = glob.glob("C:/Users/16690/Desktop/Chemi_PDF/*.pdf")
    path = "C:/Users/16690/Desktop/Chemi_PDF/On-the-fly assessment of diffusion barriers of disordered transition metal oxyfluorides using local descriptors.pdf"
    file_name = path[33:-4]
    print("Processing number --- %s" % file_name)
    parse(path, file_name)
    # print(pdf_path)
    # for path in pdf_path:
    #     file_name = path[33:-4]
    #     print("Processing number --- %s"%file_name)
    #     parse(path, file_name)