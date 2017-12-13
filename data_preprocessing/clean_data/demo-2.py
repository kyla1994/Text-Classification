#coding:utf-8
from itertools import groupby
def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()

if __name__ == '__main__':

    # MAX_LENGTH = 0
    # with open(r'E:\data_split_seg_stops\all.txt') as f:
    #     for line in f.readlines():
    #         line = line.replace(' ','').replace('\n','')
    #         if MAX_LENGTH<len(line):
    #             MAX_LENGTH = len(line)
    # print  MAX_LENGTH
    lst = []
    dic = {}
    for i in range(0,56542):
        dic[i] = 0
    cl = 0
    with open('/home/liyt/code/text_classification_v1.1/data/all/all.txt') as f:
         for line in f.readlines():
             line = line.replace(' ', '').replace('\n', '')
             items = line.split('__label__')
             content = items[0]
             try:
                dic[len(content)]+=1
                lst.append(len(content))
                write_add('lyt.txt', str(len(content)) + '\n')
                cl+=1
             except:
                 pass
    #print len(lst)/cl
    # dict2 = {}
    # print len(lst)
    # for k,g in groupby(lst,key=lambda x:(x-1)//100):
    #     dict2['{}-{}'.format(k*100+1,(k+1)*100)]=len(list(g))
    # print dict2
    # sum = 0
    # for i in range(0,56542):
    #     sum +=dic[i]
    # print sum
    # dic1 ={}
    # for i in range(0,115):
    #     dic1[i] = 0

    # for i in range(0, 56542):
    #     print i%500 ,dic1[i%500],dic[i],i
    #     dic1[i%500]=+dic[i]
    # for i in  range(0,115):

