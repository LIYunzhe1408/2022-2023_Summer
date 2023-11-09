import re
import os
from multiprocessing import Process
from multiprocessing import Manager
import requests
import time
import xlrd
from bs4 import BeautifulSoup
from lxml import etree
import pickle
from tqdm import tqdm
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)



class SpiderMain(object):
    def __init__(self, sid, kanming):
        self.hearders = {
            'Origin': 'https://apps.webofknowledge.com',
            'Referer': 'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=R1ZsJrXOFAcTqsL6uqh&preferencesSaved=',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.form_data = {
            'fieldCount': 1,
            'action': 'search',
            'product': 'WOS',
            'search_mode': 'GeneralSearch',
            'SID': sid,
            'max_field_count': 25,
            'formUpdated': 'true',
            'value(input1)': kanming,
            'value(select1)': 'TI',
            'value(hidInput1)': '',
            'limitStatus': 'collapsed',
            'ss_lemmatization': 'On',
            'ss_spellchecking': 'Suggest',
            'SinceLastVisit_UTC': '',
            'SinceLastVisit_DATE': '',
            'period': 'Range Selection',
            'range': 'ALL',
            'startYear': '1982',
            'endYear': '2017',
            'update_back2search_link_param': 'yes',
            'ssStatus': 'display:none',
            'ss_showsuggestions': 'ON',
            'ss_query_language': 'auto',
            'ss_numDefaultGeneralSearchFields': 1,
            'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A'
        }
        self.form_data2 = {
            'product': 'WOS',
            'prev_search_mode': 'CombineSearches',
            'search_mode': 'CombineSearches',
            'SID': sid,
            'action': 'remove',
            'goToPageLoc': 'SearchHistoryTableBanner',
            'currUrl': 'https://apps.webofknowledge.com/WOS_CombineSearches_input.do?SID=' + sid + '&product=WOS&search_mode=CombineSearches',
            'x': 48,
            'y': 9,
            'dSet': 1
        }

    def craw(self, root_url, i):
        try:
            s = requests.Session()
            r = s.post(root_url, data=self.form_data, headers=self.hearders)
            r.encoding = r.apparent_encoding
            tree = etree.HTML(r.text)
            cited = tree.xpath("//div[@class='search-results-data-cite']/a/text()")
            download = tree.xpath(".//div[@class='alum_text']/span/text()")
            flag = 0
            print(cited, download, r.url)
            flag = 0
            return cited, download, flag
        except Exception as e:
            # 出现错误，再次try，以提高结果成功率
            if i == 0:
                print(e)
                print(i)
                flag = 1
                return cited, download, flag

    def delete_history(self):
        murl = 'https://apps.webofknowledge.com/WOS_CombineSearches.do'
        s = requests.Session()
        s.post(murl, data=self.form_data2, headers=self.hearders)


class MyThread(Process):
    def __init__(self, sid, kanming, i, dic):
        Process.__init__(self)
        self.row = i
        self.sid = sid
        self.kanming = kanming
        self.dic = dic

    def run(self):
        self.cited, self.download, self.fl = SpiderMain(self.sid, self.kanming).craw(root_url, self.row)
        self.dic[str(self.row)] = Result(self.download, self.cited, self.fl, self.kanming, self.row)


class Result():
    def __init__(self, download, cited, fl, kanming, row):
        super().__init__()
        self.row = row
        self.kanming = kanming
        self.fl = fl
        self.cited = cited
        self.download = download



def runn(sid, kanming, i, d):
    ar, ref, fl = SpiderMain(sid, kanming).craw(root_url, row)
    d[str(i)] = Result(ar, ref, fl, kanming, i)
    print(d)

def getHTMLText(url):
    try:
        kv = {"user-agent":"Mozilla/5.0"}
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text, r
    except:
        return "产生异常"

def download(url):

    path = url.split("/")[-1]
    try:
        if not os.path.exists(path):
            r = requests.get(url)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已存在")
    except:
        print("爬去失败")

def match_target(re_text, text):
    match_list = re.findall(re_text, text)
    print(match_list)

def getAuthor_Name(Many_INFO_html):

    try:
        html = Many_INFO_html[0]
        Author_soup = BeautifulSoup(html, 'html.parser')

        author_name = []
        for i in Author_soup.p.contents:
            try:
                if i.name == 'a':
                    author_name.append(i.next)
                    author_name.append(i.nextSibling)
            except:
                continue
            # print(
            #     "========================================================================================================================")
        Whole_name = [author_name[i] for i in range(len(author_name)) if i % 2 == 0]
        Simply_name = [author_name[i][2:-1] for i in range(len(author_name)) if i % 2 == 1]
    except:
        Whole_name = [""]
        Simply_name = [""]


    return Simply_name,Whole_name


def juan_ye_DOI_Year_Type(Many_INFO_html):  #获取卷，页码，DOI,年份，类型

    #提取一下内容
    Columns = ['Volume','Pages','DOI','Published:','Document Type','Publisher','Research Domain','Issue']
    basic_INFO = dict()


    boarder = len(Many_INFO_html)
    for i in range(1,min(10, boarder)):
        try:
            html = Many_INFO_html[i]
            Author_soup = BeautifulSoup(html, 'html.parser')

            temp_info = []
            for i in Author_soup.p.contents:
                temp_info.append(i.string)

            new_info = [i for i in temp_info if i!='\n' and i!=None ]
            basic_INFO[new_info[0][:-1]] = new_info[1:]
        except:
            continue



    keys = basic_INFO.keys()
    daishanchu = []
    for key in keys:
        if key not in Columns:
            daishanchu.append(key)
    if 'Published:' in keys:
        basic_INFO["Published Date"] = basic_INFO['Published:']
        daishanchu.append('Published:')

    for i in daishanchu:
        del basic_INFO[i]


    return basic_INFO


def abstract(abstract_list):
    abstract_dic = dict()
    try:
        html = abstract_list[0]
        abstract_soup = BeautifulSoup(html, 'html.parser')
        abstract_text = ""
        list1 = []
        for i in abstract_soup.p.contents:

            if i != '\n' and i != None and i != "":
                if type(i.string) != type(None):
                    abstract_text += i.string

        abstract_dic['Abstract'] = abstract_text
    except:
        abstract_dic['Abstract'] = ""
    return abstract_dic

def keyWords_extract(abstract_list):
    keywords_dic = dict()
    try:
        html = abstract_list[0]
        abstract_soup = BeautifulSoup(html, 'html.parser')
        keywords_list = []
        for i in abstract_soup.p.contents:
            if i.string != '\n' and i.string != None and i.string != "" and i.string != "; ":
                keywords_list.append(i.string)
        keywords_dic['Keywords'] = keywords_list[1:]
    except:
        keywords_dic['Keywords'] = [""]




    return keywords_dic

    # abstract_dic = dict()
    # abstract_dic['Abstract'] = abstract_text
    # return abstract_dic


def keyWordsplus_extract(abstract_list):
    keywords_dic = dict()

    soup1 = BeautifulSoup('<b class="boldest">Extremely bold</b>')
    tag = soup1.b

    try:
        html = abstract_list[0]
        abstract_soup = BeautifulSoup(html, 'html.parser')
        keywords_list = []
        for i in abstract_soup.contents[0].contents:
            if type(i) == type(tag):
                if "href" in i.attrs:
                    string_temp = i["href"]
                    re_title = r'value=.*?&'
                    text = re.findall(re_title, string_temp)
                    keywords_list += text[0][6:-1].split("+")



        keywords_dic['Keywords_plus'] = keywords_list
    except:
        keywords_dic['Keywords_plus'] = [""]
    return keywords_dic

def joural_extract(joural_list):


    bas = dict()
    try:
        html = joural_list[0]
        abstract_soup = BeautifulSoup(html, 'html.parser')
        joural_list = abstract_soup.value.string
        bas['joural'] = joural_list

    except:
        bas['joural'] = ""
    return bas

def impact_factor_extract(joural_list):
    bas = dict()

    try:
        html = joural_list[0]
        abstract_soup = BeautifulSoup(html, 'html.parser')
        tag_soup = abstract_soup.tr
        joural_list = tag_soup.contents[3].string
        bas['impact_factor'] = joural_list

    except:
        bas['impact_factor'] = ""
    return bas


def pdf_extract(pdf_htmlList):
    try:
        html = pdf_htmlList[0]
        abstract_soup = BeautifulSoup(html, 'html.parser')
        value = abstract_soup.input.nextSibling["value"]
    except:
        value = ""

    return value



def Merge(dict1, dict2):
    dict2.update(dict1)
    return dict2


def reprint_extract(reprint_htmlList):
    html = reprint_htmlList[0]
    abstract_soup = BeautifulSoup(html, 'html.parser')

    Corresponding_Info = []
    context = abstract_soup.contents[2].contents
    # for i in abstract_soup.contents[3].contents:
    #     if i.string != '\n' and i.string != None and i.string != "" and i.string != "; ":
    #         Corresponding_Info.append(i.string)


    # print(Corresponding_Info)
    reprint_info = dict()
    try:
        reprint_info['reprint author'] = context[3].contents[-2].attrs['author']
    except:
        reprint_info['reprint author'] = ""

    Corresponding_address = []

    try:
        reprint_info["reprint address"] = context[3].contents[1].contents[0]
    except:
        reprint_info['reprint author'] = ""


    return reprint_info



def extract_info(article_url):
    author_name = {}
    all_info = {}
    this_html, session = getHTMLText(article_url)

    re_title = r'<input type="hidden" name="00N70000002BdnX"[\s\S]*?/>'

    title_html = re.findall(re_title, this_html)
    soup = BeautifulSoup(title_html[0], 'html.parser')

    # title 标题提取完成。
    title = soup.input['value']


    #提取所有结构化数据，找到所在网页范围
    re_many_Info = r'<p class="FR_field">[\s\S]*?</p>'
    Many_INFO_html = re.findall(re_many_Info, this_html)
    author_name['whole__author_name'], author_name['simply_author_name'] = getAuthor_Name(Many_INFO_html)

    #卷，页码，DOI。。。
    basic_info = juan_ye_DOI_Year_Type(Many_INFO_html)
    basic_info['title'] = title

    #摘要
    re_Abstract = r'<div class="title3">Abstract</div>[\s\S]*?</p>'
    abstract_list = re.findall(re_Abstract, this_html)
    abstract_info = abstract(abstract_list)


    #关键字
    re_Keywords = r'<div class="title3">Keywords</div>[\s\S]*?</p>'
    keywords_list = re.findall(re_Keywords, this_html)
    keywords_info = keyWords_extract(keywords_list)


    #通讯作者及地址
    re_reprint = r'<div class="title3">Author Information</div>[\s\S]*?</p>'
    reprint_htmlList = re.findall(re_reprint, this_html)
    reprint_Info = reprint_extract(reprint_htmlList)

    #pdfl链接
    re_pdf = r'<td class="FRleftColumn" >[\s\S]*?</div>'
    pdf_htmlList = re.findall(re_pdf, this_html)
    basic_info['pdf_link'] = pdf_extract(pdf_htmlList)


    all_info = Merge(all_info, basic_info)
    all_info = Merge(all_info, abstract_info)
    all_info = Merge(all_info,keywords_info)
    all_info = Merge(all_info, reprint_Info)
    all_info = Merge(all_info, author_name)
    session.close()


    return all_info

def extract_info2(article_url):
    author_name = {}
    all_info = {}
    this_html, session = getHTMLText(article_url)

    re_title = r'<input type="hidden" name="00N70000002BdnX"[\s\S]*?/>'

    title_html = re.findall(re_title, this_html)
    if len(title_html) > 0:
        soup = BeautifulSoup(title_html[0], 'html.parser')

        # title 标题提取完成。
        title = soup.input['value']
        basic_info = dict()


        #keywords_plus 匹配
        re_Keywords_plus=r'<p class="FR_field">\n<span class="FR_label">KeyWords Plus[\s\S]*?</p>'
        keywords_plus_list = re.findall(re_Keywords_plus, this_html)
        keywords_plus_info = keyWordsplus_extract(keywords_plus_list)

        #期刊 及影响因子
        re_journal_plus = r'<source_title_txt_label lang_id="en-us">[\s\S]*?</source_title_txt_label>'
        joural_list = re.findall(re_journal_plus, this_html)
        joural_info = joural_extract(joural_list)


        re_impact_factor = r'<span class="FR_label">  Impact Factor </span>[\s\S]*?</tr>'
        impact_factor_list = re.findall(re_impact_factor, this_html)

        impact_factor_info = impact_factor_extract(impact_factor_list)


        all_info = Merge(all_info, basic_info)
        all_info = Merge(all_info, keywords_plus_info)

        all_info = Merge(all_info, joural_info)
        all_info = Merge(all_info, impact_factor_info)

        session.close()
        return all_info
    else:
        session.close()
        return all_info

def Start_Scarp(root, nums_page, filename, start_num):

    #指定的页数 目前1-xx页,350 may be the best
    #1-2801
    page_nums = list(range(start_num,nums_page+1))
    requests.adapters.DEFAULT_RETRIES = 5
    root = root
    count = 1
    INFO = {}
    for i in tqdm(page_nums):
        article_url = root + str(i)
        # dict1 = extract_info2(article_url)
        # dict2 = extract_info(article_url)
        try:
            dict1 = extract_info2(article_url)
            dict2 = extract_info(article_url)
        except:
            print("第" + str(i) + "文献没爬到")
            dict1 = dict()
            dict2 = dict()
        INFO[count] = Merge(dict1,dict2)
        count += 1
    today = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    save_obj(INFO, "Mid_Process_File/"+today)
    return INFO


