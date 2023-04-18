import urllib.parse
import asyncio
import aiohttp
from lxml import etree
import re 
import time
from fake_useragent import UserAgent
url='https://baike.baidu.com/item/'
used_id=[]
i=0

 # 请求头部
headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        'User-Agent':UserAgent().random
}

def filter(str):
    for it in re.findall(r'\[\d+\]|\[\d+-\d+\]',str):
        str=str.replace(it,'')
    return str

async def queryid(content):
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            res = await response.text()
            print(res)
            num=re.findall(r'data-lemmaId="(.*?)"',res,re.S)
            t=-1
            if len(num):
                t=num[0]
            return t

async def queryjs(url):
    # 请求地址

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            res = await response.json()
            return res

async def dfs(name):
    global i
    num=await queryid(name) 
    if num in used_id:
        return 
    i+=1
    s='第'+str(i)+'个:'+name+'\n'
    print(s,end='')
    if i==1:
        with open('name.txt','w',encoding='UTF-8') as p:
            p.write(s)
    else :
        with open('name.txt','a',encoding='UTF-8') as p:
            p.write(s)
    used_id.append(num)  
    if num==-1:
        print('Num not found')
        return 
    url2='https://baike.baidu.com/starmap/api/gethumanrelationcard?lemmaId='+str(num)+'&lemmaTitle='+name
    # print(url2)
    res=await queryjs(url2)
    lists=res["list"]
    if len(lists)==0:
        return
    for list in lists:
        # print(list['relationName'],' : ',list['lemmaTitle'])
        name=list['lemmaTitle']
        time.sleep(1)
        await dfs(name) 

async def main():
    result = await dfs(name)
    print(result)

if __name__ == '__main__':
    name=input('请输入姓名:')
    asyncio.run(main())














