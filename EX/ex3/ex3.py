from get_rel import *
import cal_and_draw
import get_rel
from cal_and_draw import *
name=input('请输入姓名:')
sum=int(input('请输入核心人物数:'))
cal_and_draw.flag=1
# name='毛泽东'
# sum=6
get(name,sum)
cal_draw()
predict=[cal_and_draw.sorted_items[i][0] for i in range(sum)]
mreal=get_rel.real
print('实际核心人物:',mreal)
print('预测核心人物:',predict)
tp=tn=fp=fn=0
for i in predict:
    if i in mreal:
        tp+=1
    else :
        fp+=1
fn=sum-tp
print('准确率:',float(tp+tn)/sum)
print('精确率:',float(tp)/(tp+fp))
print('召回率:',float(tp)/(tp+fn))
