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
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    items = line.split('	')
                    tag = items[0]
                    content = items[3]
                    #print tag,content
                    if tag == '汽车':
                        write_add('auto.txt', content + '\n')
                    elif tag == '财经':
                        write_add('finance.txt', content + '\n')
                    elif tag == 'IT':
                        write_add('it.txt', content + '\n')
                    elif tag == '健康':
                        write_add('health.txt', content + '\n')
                    elif tag == '体育':
                        write_add('sports.txt', content + '\n')
                    elif tag == '旅游':
                        write_add('travel.txt', content + '\n')
                    elif tag == '教育':
                        write_add('education.txt', content + '\n')
                    elif tag == '招聘':
                        write_add('jobs.txt', content + '\n')
                    elif tag == '文化':
                        write_add('culture.txt', content + '\n')
                    elif tag == '军事':
                        write_add('military.txt', content + '\n')

