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
    rootdir ='/home/liyt/code/text_classification_v1.1/data/data_tiny/tmp' #r'/home/liyt/code/text_classification_v1.1/data/data_cat'
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            label = filename.replace('.txt','')
            cnt = 0
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    cnt+=1
                    if cnt % 5 == 0:
                        write_add('news_fasttext_test.txt',line)
                    else:
                        write_add('news_fasttext_train.txt',line)

                    # if len(line)>10:
                    #     line +='__label__'+ label +'\n'
                    #     cnt+=1
                    #     if cnt % 9 == 0:
                    #         write_add('/home/liyt/code/text_classification_v1.1/data/data_tiny/testsets.txt',line)
                    #     #
                    #     # else:
                    #     #     write_add('/home/liyt/code/text_classification_v1.1/data/data_split/trainsets.txt',line)
