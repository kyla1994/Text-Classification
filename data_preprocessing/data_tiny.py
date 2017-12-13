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
    file_path = '/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops/trainsets.txt'
    with open(file_path, 'r') as f:
        for line in f.readlines():
            write_add('/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops/all.txt',line)

    file_path = '/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops/testsets.txt'
    with open(file_path, 'r') as f:
        for line in f.readlines():
            write_add('/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops/all.txt', line)


