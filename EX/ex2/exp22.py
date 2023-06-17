#-*- coding: UTF-8-*-
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
from lxml import html
import pymysql
import csv
import warnings
from fake_useragent import UserAgent
import time
warnings.filterwarnings("ignore",category=DeprecationWarning)
url='https://baike.baidu.com/item/'
outloc=0
file='1.txt'
used_id=[]
no=0
with open("file2.csv", "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['序号','姓名','ID','简介','基本信息','人物关系','人物履历'])


def printf(str,flag,lab):
    if(flag) :
        print(str)
    # with open(lab,'a',encoding='UTF-8') as p:
        # p.write(str+'\n')

def filter1(str):
    for it in re.findall(r'\[\d+\]|\[\d+-\d+\]|\n',str):
        str=str.replace(it,'')
    return str

def filter2(str):
    for it in re.findall(r'\[\d+\]|\[\d+-\d+\]|\n|\s\s|展开全部',str):
        str=str.replace(it,'')
    return str

#请求网页
def req(url,numm):
    headers = {
        'User-Agent':UserAgent().random
        }
    if numm!=-1:
        res = requests.get(url+'/'+str(numm),headers=headers)
        # print(url+str(numm))
    else:
        res = requests.get(url,headers=headers)
    # print(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    if numm!=-1:
        data.append(numm)
        return res,soup,numm
    else:
        num=re.findall(r'data-lemmaId="(.*?)"',res.text.encode('utf-8').decode("unicode_escape"),re.S)
        if len(num):
            data.append(num[0])
        t=-1
        if len(num):
            t=num[0]
        return res,soup,t


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
    data.append(s)
#输出基本信息
def get2(soup):
    s=''
    s1='\n'+'#'*30+'基本信息'+'#'*30
    printf(s1,outloc,file)
    infos = soup.find("div", {"class": "basic-info J-basic-info cmn-clearfix"})
    if infos == None:
        s='人物暂无基本信息'
        printf(s,outloc,file)
        return 
    # print(infos)
    key=infos.find_all("dt")
    value=infos.find_all("dd")
    for i in range(len(key)):
        str=value[i].text.strip()
        str=filter1(str)
        ss=key[i].text+':'+str
        s+=ss
        printf(s,outloc,file)
    data.append(s)


def get3(num,name):
    s=''
    s1='\n'+'#'*30+'人物关系'+'#'*30
    printf(s1,outloc,file)
    url='https://baike.baidu.com/starmap/api/gethumanrelationcard?lemmaId='+str(num)+'&lemmaTitle='+name
    if num==-1:
        s="呜呜呜，我不配有人物关系"
        printf(s,outloc,file)
        return
    res=requests.get(url)
    # print(res.text)
    lists=res.json()["list"]
    if len(lists)==0:
        s="呜呜呜，我不配有人物关系"
        printf(s,outloc,file)
    for list in lists:
        ss=list['relationName']+' : '+list['lemmaTitle']
        printf(s,outloc,file)
        s+=ss
    data.append(s)
    return lists

def get4(resp):
    s=''
    printf('\n'+'#'*30+'人物履历'+'#'*30,outloc,file)
    # print(resp.text)
    sel=etree.HTML(resp.text)
    pos= sel.xpath('//a[@class="audio-play part-audio-play J-part-audio-play"]')
    if len(pos)==0:
        s='人物暂无履历'
        printf(s,outloc,file)
        return 
    elif len(pos)==1:
        pos1 = pos[0]
        text = pos1.xpath('.//text()')
        ss=filter2(''.join(text))
        printf(ss,outloc,file)
        data.append(ss)
    else:
        pos1 = pos[0]
        pos2 = pos[1]
        pos1 = pos1.xpath("parent::*[1]")[0]
        pos2 = pos2.xpath("parent::*[1]")[0]
        pos = pos1
        pos = pos.xpath("following-sibling::*[1]")[0]
        while pos != pos2:
            text = pos.xpath('.//text()')
            ss=filter2(''.join(text))
            s+=ss
            printf(s,outloc,file)
            pos = pos.xpath("following-sibling::*[1]")[0]
        data.append(s)

def bdbk(no,name,numm=-1):
    data.clear()
    data.append(no)
    data.append(name)
    urlt=url+name
    res,soup,num=req(urlt,numm)
    if num==-1:
        return None,None,None
    get1(soup)
    get2(soup)
    lists=get3(num,name)
    get4(res)
    # print(name,'Over!')
    flag=1
    if len(data)<7:
        flag=0
        return lists,num,flag
    with open("file2.csv", "a", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)
        f.close()
    return lists,num,flag

def dfs(name,num=-1):
    global no
    if num in used_id:
        return 
    no+=1
    lists,realn,flag=bdbk(no,name,num)
    if flag:
        print('第',str(no),'个:',name,'completed!')
        used_id.append(int(realn))
    else:
        print('第',str(no),'个:',name,'failed!')
        no-=1
        time.sleep(10)
        return
    if len(lists)==0:
        return
    for list in lists:
        # print(list['relationName'],' : ',list['lemmaTitle'])
        name=list['lemmaTitle']
        num=list['lemmaId']
        time.sleep(1)
        dfs(name,num)   




if __name__ == '__main__':
    name=input('请输入姓名:')
    # name='邓超'
    outloc=0
    file='1.txt'
    data=[]
    dfs(name)
    