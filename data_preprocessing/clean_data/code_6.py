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
    rootdir = r'C:\code\news'
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)#sys.argv[1]
            tag = filename.replace('.txt','')
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    content = line.replace('\n','')
                    if tag == 'auto':#
                        write_add('auto.txt', content + '\n')
                    elif tag == 'finance':#
                        write_add('finance.txt', content + '\n')
                    elif tag == 'it':
                        write_add('it.txt', content + '\n')
                    elif tag == 'sports':#
                        write_add('sports.txt', content + '\n')
                    elif tag == 'education':#
                        write_add('education.txt', content + '\n')
                    elif tag == 'military':#
                        write_add('military.txt', content + '\n')
                    elif tag == 'politics':
                        write_add('politics.txt',content+'\n')
                    elif tag == 'entertainment':
                        write_add('entertainment.txt', content + '\n')
                    elif tag == 'house':
                        write_add('house.txt', content + '\n')
