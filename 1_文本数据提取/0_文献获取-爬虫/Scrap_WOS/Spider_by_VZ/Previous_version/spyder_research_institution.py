#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 17:35:00 2021

@author: davidxu
"""

from lxml import etree
import time
import pandas
from selenium import webdriver
from func_timeout import func_set_timeout
from selenium.webdriver.chrome.options import Options

research_institution=[]
piilist=[]
num=[]
options = Options()
options.set_headless()
driver = webdriver.Chrome(options=options,executable_path="D:\yy\chromedriver.exe")
js= "document.getElementById('show-more-btn').click()"

@func_set_timeout(10)
def gettext():
    while True:
        driver.execute_script(js)
        get=driver.page_source
        selector=etree.HTML(get)
        text=selector.xpath('//button[@id="show-more-btn"]/span/text()')[0]
        if text=="Show less":
            institution=selector.xpath('//div[@class="author-group"]/dl/dd')
            if institution!=[]:
                string=""
                kase=1
                for j in range(0,len(institution),1):
                    temp=institution[j].text
                    if temp==None:
                        temp=institution[j].xpath('string(.)').strip()
                        print(temp)
                        if kase==1:
                            kase=0
                            string=string+temp
                        else:
                            string=string+";"+temp
                    else:
                        print(temp)
                        if kase==1:
                            kase=0
                            string=string+temp
                        else:
                            string=string+";"+temp
                print(pii[i])
                research_institution.append(string)
                piilist.append(pii[i])
                num.append(i)
            else:
                print(pii[i]+" Empty")
                research_institution.append("")
                piilist.append(pii[i])
                num.append(i)
            break
        else:
            continue
      
@func_set_timeout(15)
def get():
    driver.get(tempurl)
    
@func_set_timeout(15)
def is_load():
    STR_READY_STATE = ''
    while STR_READY_STATE != 'complete':
            time.sleep(0.5)
            STR_READY_STATE = driver.execute_script('return document.readyState')
            
pii=['S0167273820305087', 'S2405829720301835', 'S1385894720306963']
for i in range(0,10,1):
    tempurl="https://www.sciencedirect.com/science/article/pii/%s"%(pii[i])
    text=""
    while text!='Show less': 
        try:
            get()
        except:
            print(pii[i]+" Get Failed")
            driver.quit()
            continue
        
        try:
            is_load()
        except:
            print(pii[i]+" Load Failed")
            driver.quit()
            time.sleep(5)
            continue
        try:
            gettext()
            driver.quit() 
            time.sleep(5)
            break
        except:
            print(pii[i]+" Click Failed")
            driver.quit()
            time.sleep(5)
            continue
data=[]
data.append(num)
data.append(piilist)
data.append(research_institution)
DF=pandas.DataFrame(data,index=["code","pii","research"])
DF=DF.T
DF.to_excel('article_information/research_institution_0_2429.xlsx')

