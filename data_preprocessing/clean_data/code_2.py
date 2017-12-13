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
            file_path = os.path.join(parent, filename)
            tag = parent.split('\\')[-1]

            with open(file_path, 'r') as f:
                cnt+=1
                #print cnt
                content  = f.read()
                content = content.strip().replace(' ','').replace('\n','').replace('\r','').replace('\t','').replace('　　','')
                if tag == 'C000008':
                    write_add('finance.txt', content+'\n')
                elif tag == 'C000010':
                    write_add('it.txt', content + '\n')
                elif tag == 'C000013':
                    write_add('health.txt', content + '\n')
                elif tag == 'C000014':
                    write_add('sports.txt', content + '\n')
                elif tag == 'C000016':
                    write_add('travel.txt', content + '\n')
                elif tag == 'C000020':
                    write_add('education.txt', content + '\n')
                elif tag == 'C000022':
                    write_add('jobs.txt', content + '\n')
                elif tag == 'C000023':
                    write_add('culture.txt', content + '\n')
                elif tag == 'C000024':
                    write_add('military.txt', content + '\n')




