#-*- coding: UTF-8-*-
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
from lxml import html
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
url='https://baike.baidu.com/item/'
outloc=0
file='1.txt'


def printf(str,flag,lab):
    if(flag) :
        print(str)
    with open(lab,'a',encoding='UTF-8') as p:
        p.write(str+'\n')

def filter1(str):
    for it in re.findall(r'\[\d+\]|\[\d+-\d+\]|\n',str):
        str=str.replace(it,'')
    return str

def filter2(str):
    for it in re.findall(r'\[\d+\]|\[\d+-\d+\]|\n|\s\s|展开全部',str):
        str=str.replace(it,'')
    return str

#请求网页
def req(url):
    # 发送HTTP GET请求并获取响应
    res = requests.get(url)
    # print(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    num=re.findall(r'data-lemmaId="(.*?)"',res.text.encode('utf-8').decode("unicode_escape"),re.S)
    t=-1
    if len(num):
        t=num[0]
    return soup,t


# 输出简介
def get1(soup):
    s='\n'+'#'*32+'简介'+'#'*32
    printf(s,outloc,file)
    info = soup.find("div", {"class": "lemma-summary J-summary"})
    if info == None:
        s='人物暂无简介'
        printf(s,outloc,file)
        return 
    s=filter1(info.text)
    printf(s,outloc,file)

    # match = re.findall(r"[^\x00-\xff]|\d{4}年\d{1,2}月|\d{1,2}日", info.text)
    # for i in match:
    #     print(i, end="")

#输出基本信息
def get2(soup):
    s='\n'+'#'*30+'基本信息'+'#'*30
    printf(s,outloc,file)
    infos = soup.find("div", {"class": "basic-info J-basic-info cmn-clearfix"})
    if infos == None:
        printf('人物暂无基本信息',outloc,file)
        return 
    # print(infos)
    key=infos.find_all("dt")
    value=infos.find_all("dd")
    for i in range(len(key)):
        str=value[i].text.strip()
        str=filter1(str)
        # if str[-1]==']':
        #     while str[-1]!='[':
        #         str=str[:-1]
        #     str = str[:-2]
        printf(key[i].text+':'+str,outloc,file)


def get3(num,name):
    s='\n'+'#'*30+'人物关系'+'#'*30
    printf(s,outloc,file)
    url='https://baike.baidu.com/starmap/api/gethumanrelationcard?lemmaId='+str(num)+'&lemmaTitle='+name
    if num==-1:
        printf("呜呜呜，我不配有人物关系",outloc,file)
        return
    res=requests.get(url)
    # print(res.text)
    lists=res.json()["list"]
    if len(lists)==0:
        printf("呜呜呜，我不配有人物关系",outloc,file)
    for list in lists:
        printf(list['relationName']+' : '+list['lemmaTitle'],outloc,file)

def get4(url):
    printf('\n'+'#'*30+'人物履历'+'#'*30,outloc,file)
    resp=requests.get(url)
    # print(resp.text)
    sel=etree.HTML(resp.text)
    pos= sel.xpath('//a[@class="audio-play part-audio-play J-part-audio-play"]')
    if len(pos)==0:
        printf('人物暂无履历',outloc,file)
        return 
    else:
        pos1 = pos[0]
        pos2 = pos[1]
        pos1 = pos1.xpath("parent::*[1]")[0]
        pos2 = pos2.xpath("parent::*[1]")[0]
        # print(pos2.xpath(".//text()"))
        # print(pos1 == pos2)
        pos = pos1
        pos = pos.xpath("following-sibling::*[1]")[0]
        while pos != pos2:
            text = pos.xpath('.//text()')
            printf(filter2(''.join(text)),outloc,file)
            # if text:
            #     for a in text:
            #         if a.count('[')==0 and a.count('\n')==0:
            #             print(a,end="")
            #     # print(text)
            #         print('\n')
            pos = pos.xpath("following-sibling::*[1]")[0]

def bdbk(name):
    urlt=url+name
    soup,num=req(urlt)
    get1(soup)
    get2(soup)
    get3(num,name)
    get4(urlt)
    print('Over!')

if __name__ == '__main__':
    name=input('请输入姓名:')
    # name='邓超'
    outloc=0
    file='3.txt'
    bdbk(name)
    