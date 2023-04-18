import pandas as pd
import time
from selenium import webdriver
from urllib import parse

driver = webdriver.Firefox()

# 获取一个人的详情页
def get_one_detail(url):
    driver.get(url)
    # 姓名
    temp = url.split('/')
    name = parse.unquote(temp['item'.index(temp)+1])
    # 个人描述
    desc = driver.find_element_by_class_name('lemma-summary').text.split()
    # 头像
    try:
        head_image = driver.find_element_by_class_name('summary-pic').find_element_by_tag_name('a').get_attribute('href')
    except:
        head_image = ''
    return [{'人物':name,'简介':''.join(desc),'头像':head_image}]

# 获取一个人的详情页和关系图
def get_one_detail_kg(name):
    url = 'https://baike.baidu.com/item/'+name
    driver.get(url)
    # time.sleep(1)
    relationship_list = []
    people_list = []
    # 个人描述
    desc = driver.find_element_by_class_name('lemma-summary').text.split()
    # 头像
    try:
        head_image = driver.find_element_by_class_name('summary-pic').find_element_by_tag_name('a').get_attribute('href')
    except:
        head_image = ''
    # 与之相关的人
    elements = driver.find_elements_by_class_name('lemma-relation-item')
    # 相关人的名字，单独get，否则正在循环的element失效
    kg_name = []
    for li in elements:
        relationship = li.find_element_by_class_name('name').text
        _name = li.find_element_by_class_name('title').text
        relationship_list.append({'人物A': _name, '关系': relationship, '人物B': name})
        detail_url = li.find_element_by_tag_name('a').get_attribute('href')
        kg_name.append(detail_url)
    for detail_url in kg_name:
        one_detail = get_one_detail(detail_url)
        people_list.append(one_detail)
    people_list.append({'人物':name,'简介':''.join(desc),'头像':head_image})
    assert relationship_list!=None and people_list!=None
    return relationship_list,people_list



relationship_list = []
people_list = []
names = ['小明','小华']
for i in names:
    print(i)
    one_relationship_list,one_people_list = get_one_detail_kg(i)
    relationship_list += one_relationship_list
    people_list += one_people_list

df = pd.DataFrame(relationship_list)
df.to_excel('人物关系.xls',index=False)

df = pd.DataFrame(people_list)
df.to_excel('人物.xls',index=False)
