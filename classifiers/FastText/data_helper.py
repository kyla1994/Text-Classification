# _*_coding:utf-8 _*_



def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()

if __name__ == '__main__':

    dic = {}
    lis = ['auto', 'culture', 'entertainment', 'history', 'house', 'military', 'politics', 'sports', 'technology']
    i = 0
    for li in lis:
        dic[li] = i
        i += 1

    infile = '/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops/trainsets.txt'
    with open(infile, 'r') as fr:
        for line in fr.readlines():
            sent = line.replace('\n', '').replace('\r', '')
            sents = sent.split("__label__")
            write_add('news_fasttext_train.txt', sents[0]+"__label__"+str(dic[sents[1]])+'\n')

    infile = '/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops/testsets.txt'
    with open(infile, 'r') as fr:
        for line in fr.readlines():
            sent = line.replace('\n', '').replace('\r', '')
            sents = sent.split("__label__")
            write_add('news_fasttext_test.txt', sents[0]+"__label__"+str(dic[sents[1]])+'\n')
