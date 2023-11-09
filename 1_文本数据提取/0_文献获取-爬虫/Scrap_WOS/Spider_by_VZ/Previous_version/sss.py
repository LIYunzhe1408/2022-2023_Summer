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



results = requests.get("https://tv.cctv.com/cctv12/").text
soup = BeautifulSoup(
    '<div class="retrieve"><div class="logo"><a href="http://tv.cctv.com/"><img width="245" height="100" src="//p1.img.cctvpic.com/photoAlbum/page/performance/img/2019/1/9/1547008602986_172.png" alt="央视网" title="央视网（www.cctv.com）由中央电视台主办，为国家重点新闻网站，是集新闻、信息、娱乐、服务为一体的具有视听互动特色的综合性门户网站。"></a></div>',
    'html.parser')
print(soup._most_recent_element.attrs['title'])