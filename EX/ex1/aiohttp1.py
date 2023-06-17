import urllib.parse
import asyncio
import aiohttp
from lxml import etree
import re 

 # 请求头部
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

def filter(str):
    for it in re.findall(r'\[\d+\]|\[\d+-\d+\]',str):
        str=str.replace(it,'')
    return str

async def query(content):
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.text()
            # 构造 _Element 对象
            html = etree.HTML(text)
            # 使用 xpath 匹配数据，得到匹配字符串列表
            sen_list = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')
            # 过滤数据，去掉空白
            sen_list_after_filter = [item.strip('\n') for item in sen_list]
            # 将字符串列表连成字符串并返回
            return ''.join(sen_list_after_filter)

async def main():
    while (True):
        content = input('查询词语：')
        result = await query(content)
        rest=filter(result)
        print("查询结果：%s" % rest)

if __name__ == '__main__':
    asyncio.run(main())