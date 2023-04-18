#-*- coding: UTF-8-*-
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
from lxml import html
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
url='https://baike.baidu.com/item/'


#请求网页
def req(url):
    # 发送HTTP GET请求并获取响应
    res = requests.get(url)
    print(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    num=re.findall(r'data-lemmaId="(.*?)"',res.text.encode('utf-8').decode("unicode_escape"),re.S)
    # print(num)
    t=-1
    if len(num):
        t=num[0]
    return soup,t


# 输出简介
def get1(soup):
    info = soup.find("div", {"class": "lemma-summary J-summary"})
    if info == None:
        print('人物暂无简介')
        return 
    # print(info_table)
    match = re.findall(r"[^\x00-\xff]|\d{4}年\d{1,2}月|\d{1,2}日", info.text)
    for i in match:
        print(i, end="")

#输出基本信息
def get2(soup):
    infos = soup.find("div", {"class": "basic-info J-basic-info cmn-clearfix"})
    if infos == None:
        print('人物暂无基本信息')
        return 
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


def get3(num,name):
    url='https://baike.baidu.com/starmap/api/gethumanrelationcard?lemmaId='+str(num)+'&lemmaTitle='+name
    # url='https://baike.baidu.com/starmap/api/gethumanrelationcard?
    # lemmaId=8511458&lemmaTitle=%E8%94%A1%E5%BE%90%E5%9D%A4'
    if num==-1:
        print("呜呜呜，我不配有人物关系")
        return
    res=requests.get(url)
    # print(res.text)
    lists=res.json()["list"]
    if len(lists)==0:
        print("呜呜呜，我不配有人物关系")
    for list in lists:
        print(list['relationName'],' : ',list['lemmaTitle'])

def get4(url):
    resp=requests.get(url)
    sel=etree.HTML(resp.text)
    # if sel.text==None:
    #     print('人物暂无履历')
    #     return -1
    pos= sel.xpath('//a[@class="audio-play part-audio-play J-part-audio-play"]')
    if len(pos)==0:
        print('人物暂无履历')
        return 
    else:
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
    name=input('请输入姓名:')
    # name='蔡徐坤'
    url=url+name
    soup,num=req(url)
    # print(num)
    print('\n################################简介################################')
    get1(soup)
    print('\n################################基本信息################################')
    get2(soup)
    print('\n################################人物关系################################')
    get3(num,name)
    print('\n################################人物履历################################')
    get4(url)