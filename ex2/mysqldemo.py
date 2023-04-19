import requests
import pandas as pd
import re
import pymysql
 
db = pymysql.connect(host='localhost', user='root', password='qweewq', db='world', port=3306, charset='utf8')
cursor = db.cursor()#建立游标
cursor.execute("DROP TABLE IF EXISTS 东方财富")#如果有表叫东方财富，删除表
sql = """
        create table 东方财富(            
        日期 char(20) not null,
        主力净流入净额 char(20),
        小单净流入净额 char(20),
        中单净流入净额 char(20),
        大单净流入净额 char(20),
        超大单净流入净额 char(20) ,
        主力净流入净占比 char(20),
        小单净流入净占比 char(20),
        中单净流入净占比 char(20),
        大单净流入净占比 char(20),
        超大单净流入净占比 char(20),
        收盘价 char(20),
        涨跌幅 char(20))
    """
try:#如果出现异常对异常处理
    # 执行SQL语句
    cursor.execute(sql)
    print("创建数据库成功")
except Exception as e:
    print("创建数据库失败：case%s" % e)




url = 'https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?cb=jQuery112301445006905131534_1634624378230&lmt=0&klt=101&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid=0.000037&_=1634624378231'
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
           }
#发送url链接的请求，并返回响应数据
response = requests.get(url=url, headers=headers)
page_text = response.text
#使用正则表达式获取数据
pat = '"klines":\[(.*?)\]'#(.*?)就是我们要取出的部分
data = re.compile(pat, re.S).findall(page_text)#compile函数编译正则匹配表达式，re.S代表可以换行匹配，使用findall函数选定数据集，也就是爬取的所有源代码



datas = data[0].split('","')#分割字符串
 
for i in range(len(datas)):
    stock = list(datas[i].replace('"', "").split(","))#把“替换为空格，以,为分隔符分割
#用sql语言写入数据表
    sql1 = """
                insert into 东方财富(
                日期,
                主力净流入净额,
                小单净流入净额,
                中单净流入净额,
                大单净流入净额,
                超大单净流入净额,
                主力净流入净占比,
                小单净流入净占比,
                中单净流入净占比,
                大单净流入净占比,
                超大单净流入净占比 ,
                收盘价 ,
                涨跌幅 )value('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
    """ % (
    stock[0], stock[1], stock[2], stock[3], stock[4], stock[5], stock[6], stock[7], stock[8], stock[9], stock[10],
    stock[11], stock[12])#将值插入到占位符%s
    # 执行 insert 增加的语句  如果出现异常对异常处理
    try:
        cursor.execute(sql1)
        db.commit() #进行数据库提交，写入数据库
    except:
        cursor.rollback() #数据回滚，多次操作要么都执行，要么都不执行
        print('写入失败')
 
# 关闭游标连接
cursor.close()
# 关闭数据库连接
db.close()
print('写入成功！')