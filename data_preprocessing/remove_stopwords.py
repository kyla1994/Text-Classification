# coding:utf-8
import sys
import os
import jieba  # 导入jieba分词库
import re

reload(sys)
sys.setdefaultencoding('utf-8')  # 设置UTF-8输出环境

#去除无用词
def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()


if __name__ == '__main__':
    key_words = set()
    all_path = '/home/liyt/code/text_classification_v1.1/data/data_split_seg'
    all_seg_stop_path = '/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops'
    stopwords = {}.fromkeys([line.rstrip() for line in open('/home/liyt/code/text_classification_v1.1/data/stopwords.txt')])
    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    for parent, dirnames, filenames in os.walk(all_path):
        for filename in filenames:
            print filename
            file_path = os.path.join(parent, filename)
            file_seg_path = os.path.join(all_seg_stop_path, filename)
            with open(file_path) as f:
                for line in f.readlines():
                    line = line.replace('\n', '')
                    #print line
                    items = line.split('__label__')
                    try:
                        sent,label = items[0],items[1]
                        seg_line = " ".join([w for w in jieba.cut(sent) \
                                               if
                                               w not in stopwords and not w.isspace() and not w.isdigit() and not value.match(
                                                   w)])
                        write_add(file_seg_path, seg_line+'__label__'+ label +'\n')
                    except:
                        pass
