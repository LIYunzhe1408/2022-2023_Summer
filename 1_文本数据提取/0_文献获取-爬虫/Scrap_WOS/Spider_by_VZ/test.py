import os

import requests
import pandas as pd
import pdf_test
import DownLoadPdf

num = 17101





paperCsv_path = "article_information/" + str(num) + "ML_material.paperInfo.csv"
article_info = pd.read_csv(paperCsv_path, index_col=0)

amounts = 0
pdf_amounts = 0
mannul_amounts = 0

lines = article_info.index.values

for line in lines:
        print("%s - %s ---- Number %s is processing......" % (num, num + 100, line))
        save_path = "article_pdf/" + str(num) + '-' + str(num+100) + '/'
        is_existed = os.path.exists(save_path)
        if not is_existed:
            os.mkdir(save_path)
        requests_pdf_url = str(article_info.loc[line, "pdf_link"])
        back_name = requests_pdf_url[-4:]
        if back_name == "nan":
            print("%s - %s ---- Number %s Blank" % (num, num + 100, line))
            continue

        #run DownloadPdf, if == False
        not_need_check = DownLoadPdf.download(requests_pdf_url, save_path, line, article_info.loc[line, "title"])
        if not_need_check:
            print("%s - %s ---- Number %s SUCCESS" % (num, num + 100, line))
            continue
        if not not_need_check:
            if back_name != ".pdf" and back_name != "/pdf":
                is_Success = pdf_test.main(requests_pdf_url, save_path, line, article_info.loc[line, "title"])
                if is_Success:
                    pdf_amounts += 1
                    print("%s - %s ---- Number %s SUCCESS" % (num, num + 100, line))
                if not is_Success:
                    mannul_root_path = save_path + str(num) + '-' + str(num+100) +".txt"
                    file = open(mannul_root_path, 'a')
                    msg = paperCsv_path[20:25] + "\t" + str(line) + "\t" + article_info.loc[line, "title"] + "\t" + requests_pdf_url
                    file.writelines(msg)
                    file.writelines('\n')
                    print("%s - %s ---- Number %s Written in txt" % (num, num + 100, line))
                    file.close()
                    mannul_amounts += 1
                amounts += 1
                continue
            try:
                r = requests.get(requests_pdf_url)
                filename = save_path + str(line) + '-' + article_info.loc[line, "title"] + ".pdf"
                article_info.loc[line, "Download_SuccessOrDefeat"] = "Success"
                with open(filename, 'wb+') as f:
                    f.write(r.content)
                    print("%s - %s ---- Number %s SUCCESS" % (num, num + 100, line))
                amounts += 1
                pdf_amounts += 1
            except:
                article_info.loc[line, "Download_SuccessOrDefeat"] = "Defeat"
                continue

print("Amounts is %s\tPDF_amounts is %s\tMannul_amounts is %s\t" %(amounts,pdf_amounts,mannul_amounts))
print("-------------------------------------------------------------------------------------------")
