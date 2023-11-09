#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:32:39 2020

@author: davidxu
"""
import requests
from lxml import etree
import re
from urllib import parse
import time
import random
import pandas
import numpy
from func_timeout import func_set_timeout
from bs4 import BeautifulSoup
import urllib
from urllib import request
import json
from jsonpath import jsonpath

pii=['S0167273820305087', 'S2405829720301835', 'S1385894720306963', 'S0378775318311972']
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'}
pattern=re.compile(r'\d+')
abstract=[]
title=[]
keyword=[]
doi=[]
author=[]
publish_date=[]
volume=[]
research_institution=[]
start_page=[]
end_page=[]
journal=[]
publisher=[]
text=[]
code=[]
institution_lack_pii=[]
institution_lack_code=[]
@func_set_timeout(5)
def gettext(url,headers):
    text.append(requests.get(url,headers=headers).text)

for i in range(0,4,1):
    tempurl="https://www.sciencedirect.com/science/article/pii/%s"%(pii[i])
    while True:
        try:
            print(pii[i])
            gettext(tempurl,headers)
        except :
            print(pii[i]+" *")
            continue
        get=text[0]
        text.pop()
        soup=BeautifulSoup(get,"html.parser")
        head=soup.find('head')
        time.sleep(random.random())
        selector = etree.HTML(get)
        #title
        Title=head.find('meta',attrs={'name':"citation_title"})
        if Title==None:
             title.append("")
        else:
             title.append(Title.get('content'))
        #volume
        Vol=head.find('meta',attrs={'name':"citation_volume"})
        if Vol==None:
             volume.append("")
        else:
             volume.append(Vol.get('content'))
        #publish_date
        Date=head.find('meta',attrs={'name':"citation_publication_date"})
        if Date==None:
            publish_date.append("")
        else:
            publish_date.append(Date.get('content'))
        #abstract
        Abs=soup.find('div',attrs={'class':"abstract author"})
        if Abs==None:
            abstract.append("")
        else:
            abstract.append(Abs.find('p').get_text())
        #doi
        Doi=soup.find('a',attrs={'class':"doi"})
        if Doi==None:
            doi.append("")
        else:    
            doi.append(Doi.get_text())
        #author
        given_name=selector.xpath('//span[@class="text given-name"]/text()')
        surname=selector.xpath('//span[@class="text surname"]/text()')
        if given_name==[] or surname==[]:
            author.append("")
        else:
            temp=str(given_name[0])+" "+str(surname[0])
            for j in range(1,len(given_name),1):
                temp=temp+","+str(given_name[j])+" "+str(surname[j])
            author.append(temp)
        #keyword
        Keywordstext=selector.xpath('//div[@class="keyword"]/span/text()')
        if Keywordstext==[]:
            keyword.append("")
        else:
            temp=Keywordstext[0]
            for j in range(1,len(Keywordstext),1):
                temp=temp+","+Keywordstext[j]
            keyword.append(temp)
        #journal
        Jou =selector.xpath('//a[@class="publication-title-link"]/text()')
        if Jou!=[]:
            journal.append(selector.xpath('//a[@class="publication-title-link"]/text()')[0])
        else:
            journal.append(head.find('meta',attrs={'name':"citation_journal_title"}).get('content'))
        #start_page
        firstpage=head.find('meta',attrs={'name':"citation_firstpage"})
        if firstpage==None:
             start_page.append("")
        else:
            start_page.append(firstpage.get('content'))
        #end_page
        lastpage=head.find('meta',attrs={'name':"citation_lastpage"})
        if lastpage==None:
            end_page.append("")
        else:
            end_page.append(lastpage.get('content'))
        #publisher
        publisher.append(head.find('meta',attrs={'name':"citation_publisher"}).get('content'))
        #research_institution
        temp=soup.find('script',attrs={'type':"application/json"}).string
        institutions=[]
        js=json.loads(temp)
        if jsonpath(js, '$..{key_name}'.format(key_name='$$'))==False:
            research_institution.append("")
        else:
            for j in jsonpath(js, '$..{key_name}'.format(key_name='$$')):
                jlen=len(j)
                for k in range(0,jlen,1):
                    if '#name' in j[k].keys():
                        if j[k]['#name']=='textfn':
                            if '_' in j[k]:
                                institutions.append(j[k]['_'])
            if institutions==[]:
                research_institution.append("")
                institution_lack_pii.append(pii[i])
                institution_lack_code.append(i)
            else:
                institutions_drop_duplicate=institutions[0]
                listlen=len(institutions)
                for j in range(1,(int)(listlen/2),1):
                    institutions_drop_duplicate=institutions_drop_duplicate+";"+institutions[j]
                research_institution.append(institutions_drop_duplicate)
        #code
        code.append(i)
        break
data=[]
data.append(title)
data.append(author)
data.append(keyword)
data.append(publish_date)
data.append(abstract)
data.append(research_institution)
data.append(volume)
data.append(doi)
data.append(start_page)
data.append(end_page)
data.append(journal)
data.append(publisher)
data.append(pii)
data.append(code)
Data=pandas.DataFrame(data,index=['title','author','keywords','publish_date','abstract','research_institution','volume','doi','start_page/article','end_page','journal','publisher','pii','code'])
Data=Data.T

Data.to_excel('../reptile_data_0-2429.xlsx')
lack_data=[]
lack_data.append(institution_lack_pii)
lack_data.append(institution_lack_code)
pandas.DataFrame(lack_data,index=['pii','code']).T.to_excel('../institution_lack_0-2429.xlsx')