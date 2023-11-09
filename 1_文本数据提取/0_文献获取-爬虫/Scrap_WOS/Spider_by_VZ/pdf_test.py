import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko)'
                         ' Chrome/14.0.835.163 Safari/535.1'}

def getHtml(url):
    url = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(url)
    html = page.read()
    page.close()
    return html
def getUrl(html):
    reg = r'(?:href|HREF)="?((?:http://)?.+?\.pdf)'
    url_re = re.compile(reg)
    url_lst = url_re.findall(html.decode())
    return(url_lst)

def getfile(url, save_path, line, name):
    file_name = save_path + str(line) + '-' + name + ".pdf"
    url = urllib.request.Request(url, headers=headers)

    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()


def main(url, save_path, line, name):
    root_url = url
    if root_url[-1] != '/':
        root_url = root_url + '/'

    try:
        html = getHtml(root_url)
        target = getUrl(html)

        for url in target:
            file_name = url.split('/')[-2] + "/" + url.split('/')[-1]
            url = root_url + file_name
            url_final = url
        getfile(url_final, save_path, line, name)
        return True
    except:
        return False

