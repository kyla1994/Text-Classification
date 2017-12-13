#coding:utf-8
import sys
import os
import jieba # 导入jieba分词库
import re
reload(sys)
sys.setdefaultencoding('utf-8') #设置UTF-8输出环境


def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()

if __name__ == '__main__':

    with open('/home/liyt/code/text_classification/preproccess/stopwords.txt', 'r') as fr:
        stoplist = set([w.strip() for w in fr.readlines()])

    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')

    all_path = '/home/liyt/code/text_classification_v1.1/data/all.txt'
    all_seg_path = '/home/liyt/code/text_classification_v1.1/data/all_seg.txt'
    with open(all_path) as f:
        for line in f.readlines():
            line = line.replace('[', '')
            line = line.replace('　　','')
            line = line.replace('\n', '')
            items = line.split(']__label__')
            try:
                sent,label = items[0],items[1]

                seg_line = ' '.join([w for w in jieba.cut(sent, cut_all=False) \
                                             if
                                             w not in stoplist and not w.isspace() and not w.isdigit() and not value.match(
                                                 w)])
                content = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", seg_line)

                content = content.replace('（  ）','')
                write_add(all_seg_path, content+'__label__'+ label +'\n')
            except:
                pass
    # all_path = '/home/liyt/code/text_classification_v1.1/data/data_split'
    # all_seg_path = '/home/liyt/code/text_classification_v1.1/data/data_split_seg'
    # for parent, dirnames, filenames in os.walk(all_path):
    #     for filename in filenames:
    #         print filename
    #         file_path = os.path.join(parent, filename)
    #         file_seg_path = os.path.join(all_seg_path, filename)
    #         with open(file_path) as f:
    #             for line in f.readlines():
    #                 sent = line.replace('　　','')
    #                 line = line.replace('\n', '')
    #                 items = line.split('__label__')
    #                 try:
    #                     sent,label = items[0],items[1]
    #                     wordlist = jieba.cut(sent)
    #                     content = " ".join(wordlist)
    #                     write_add(file_seg_path, content+'__label__'+ label +'\n')
    #                 except:
    #                     pass
