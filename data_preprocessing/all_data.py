#coding:utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8') #设置UTF-8输出环境

def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()

if __name__ == '__main__':
    rootdir = '/home/liyt/code/text_classification_v1.1/data/all/'
    for i in xrange(0,9):
        file_path = rootdir+str(i)+'.txt'
        label = str(i)
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip().replace('\n','').replace('\r','').replace(' ','')
                if len(line)>50:
                    line +='__label__'+ label +'\n'
                    write_add('/home/liyt/code/text_classification_v1.1/data/all.txt',line)
                        #
                        # else:
                        #     write_add('/home/liyt/code/text_classification_v1.1/data/data_split/trainsets.txt',line)
