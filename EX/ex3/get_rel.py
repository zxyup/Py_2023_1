#-*- coding: UTF-8-*-
import requests
import re
import csv
import warnings
from fake_useragent import UserAgent
warnings.filterwarnings("ignore",category=DeprecationWarning)
fieldnames=['No','p1','rel','p2']
url='https://baike.baidu.com/item/'
used_id=[]
no=1
real=[]


def find_rel(name,num):
    global no
    url='https://baike.baidu.com/starmap/api/gethumanrelationcard?lemmaId='+str(num)+'&lemmaTitle='+name
    res=requests.get(url)
    lists=res.json()["list"]
    if len(lists) == 0:
        return None,0
    data=[]
    for list in lists:
        data.append({'No':no,'p1':name,'rel':list['relationName'],'p2':list['lemmaTitle']})
        no+=1
    with open("rel.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for row in data:
            writer.writerow(row)
    return lists,1



def bfs(name,sum,num=-1):
    ns=1
    global no
    if num in used_id:
        return 
    queue=[(name,num)]
    while queue:
        (na,nn)=queue.pop(0)
        if nn in used_id:
            continue
        lists,flag=find_rel(na,nn)
        if flag:
            print('第',str(ns),'个核心人物:',na,'successful!')
            used_id.append(int(nn))
            real.append(na)
            for list in lists:
            # print(list['relationName'],' : ',list['lemmaTitle'])
                name=list['lemmaTitle']
                num=list['lemmaId']
                queue.append((name,num))   
        else:
            print('第',str(ns),'个核心人物:',na,'failed!')
        if ns == sum:
            return
        ns+=1
        



headers = {
        'User-Agent':UserAgent().random
        }


def get(name,sum):
    res = requests.get(url+str(name),headers=headers)
    num=re.findall(r'data-lemmaId="(.*?)"',res.text.encode('utf-8').decode("unicode_escape"),re.S)[0]
    with open("rel.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()#写入表头
    bfs(name,sum,num)
    print('关系数:',no)

if __name__ == '__main__':
    # name=input('请输入姓名:')
    # sum=input('请输入核心人物数:')
    name='蔡徐坤'
    sum=10
    get(name,sum)