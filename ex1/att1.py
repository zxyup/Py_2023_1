import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
from lxml import html

# 设置百度百科陈嘉庚的URL
# url='https://baike.baidu.com/item/%E9%99%88%E5%98%89%E5%BA%9A/485516'
url='https://baike.baidu.com/item/%E5%BC%A0%E8%8D%A3'




#请求网页
def req(url):
    # 发送HTTP GET请求并获取响应
    response = requests.get(url)
    # 使用BeautifulSoup解析HTML响应
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


# 输出简介
def get1(soup):
    info = soup.find("div", {"class": "lemma-summary J-summary"})
    # print(info_table)
    match = re.findall(r"[^\x00-\xff]|\d{4}年\d{1,2}月|\d{1,2}日", info.text)
    for i in match:
        print(i, end="")

#输出基本信息
def get2(soup):
    infos = soup.find("div", {"class": "basic-info J-basic-info cmn-clearfix"})
    # print(infos)
    key=infos.find_all("dt")
    value=infos.find_all("dd")
    for i in range(len(key)):
        str=value[i].text.strip()
        if str[-1]==']':
            while str[-1]!='[':
                str=str[:-1]
            str = str[:-2]
        print(key[i].text,':',str)


def get3(num):
    # url='https://baike.baidu.com/starmap/api/gethumanrelationcard?lemmaId='+str(num)+'&lemmaTitle='+name
    url='https://baike.baidu.com/starmap/api/gethumanrelationcard?lemmaId=8511458&lemmaTitle=%E8%94%A1%E5%BE%90%E5%9D%A4'
    res=requests.get(url)
    lists=res.json()["list"]
    for list in lists:
        print(list['relationName'],' : ',list['lemmaTitle'])

def get4(url):
    resp=requests.get(url)
    sel=etree.HTML(resp.text)
    pos1 = sel.xpath('//a[@class="audio-play part-audio-play J-part-audio-play"]')[0]
    pos2 = sel.xpath('//a[@class="audio-play part-audio-play J-part-audio-play"]')[1]
    pos1 = pos1.xpath("parent::*[1]")[0]
    pos2 = pos2.xpath("parent::*[1]")[0]
    # print(pos2.xpath(".//text()"))
    # print(pos1 == pos2)
    pos = pos1
    while pos != pos2:
        text = pos.xpath('.//text()')
        if text:
            for a in text:
                if a.count('[')==0 and a.count('\n')==0:
                    print(a,end="")
            # print(text)
            print('\n')
        pos = pos.xpath("following-sibling::*[1]")[0]


if __name__ == '__main__':
    url='https://baike.baidu.com/item/%E9%99%88%E5%98%89%E5%BA%9A/485516'   #袁隆平
    # url='https://baike.baidu.com/item/%E5%BC%A0%E8%8D%A3'    #张荣
    # url='https://baike.baidu.com/item/%E6%9D%8E%E5%85%8B%E5%BC%BA'  #李克强
    url='https://baike.baidu.com/item/%E8%94%A1%E5%BE%90%E5%9D%A4'
    num=485516
    soup=req(url)
    get1(soup)
    print('\n################################')
    get2(soup)
    print('\n################################')
    get3(num)
    get4(url)