#coding:utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8') #设置UTF-8输出环境

if __name__ == '__main__':
    with open(r'C:\code\1.txt', 'r') as f:
        for line in f.readlines():
            print line.replace('\n','')
            os.remove(line.replace('\n',''))