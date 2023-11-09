

import requests
import pandas as pd


# paperCsv_path = "article_information/17101ML_material.paperInfo.csv"
# article_info = pd.read_csv(paperCsv_path, index_col=0)
# save_path = "article_pdf/"


def download(requests_pdf_url, save_path, line, name):
    # index = article_info.index.values
    # for i in index:
    #     if(article_info.loc[i, "pdf_link"] != None):
    #         requests_pdf_url = article_info.loc[i, "pdf_link"]
            try:
                r = requests.get(requests_pdf_url)
                filename = save_path + str(line) + '-' + name +".pdf"
                # article_info.loc[i, "Download_SuccessOrDefeat"] = "Success"
                with open(filename, 'wb+') as f:
                    f.write(r.content)

                return True
            except:
                return False
                # article_info.loc[i,  "Download_SuccessOrDefeat"] = "Defeat"

