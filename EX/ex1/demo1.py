import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
from html.parser import HTMLParser

def outele(tree):
    tree3 = html.tostring(tree[0], encoding='utf-8').decode('utf-8')
    print(tree3)
url='https://baike.baidu.com/item/%E9%99%88%E5%98%89%E5%BA%9A/485516'
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


if __name__ == '__main__':
    resp=requests.get(url,headers=headers)
    # soup=BeautifulSoup(response.text,'lxml')
    sel=etree.HTML(resp.text)
    infos=sel.xpath("/html/body/div[3]/div[2]/div/div[1]/div[4]")
    for info in infos:
       # / html / body / div[3] / div[2] / div / div[1] / div[4] / div[1]
       #  outele(info.xpath("div[1]"))
       # / html / body / div[3] / div[2] / div / div[1] / div[4] / div[1] / a[1]
        print(info.xpath("div[1]/text()[1]"))