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
    #entertainment
    rootdir = r'C:\code\news'
    cnt =0
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)#sys.argv[1]
            with open(file_path, 'r') as f:
                cnt+=1
                #print cnt
                content  = f.read()
                content = content.strip().replace(' ','').replace('\n','').replace('\r','').replace('\t','').replace('　　','')
                write_add('entertainment.txt', content+'\n')
