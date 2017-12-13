#coding:utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8') #设置UTF-8输出环境

def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()
cnt = 0
with open(r'C:\code\news\entertainment.txt', 'r') as f:
    for line in f.readlines():
        # if cnt >3846:
        #     break
        cnt+=1
        write_add('C:\code\data\entertainment.txt', line)