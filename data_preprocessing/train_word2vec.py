#!/usr/bin/env python
# encoding: utf-8

# 引入 word2vec
import gensim
import os
from gensim.models import word2vec
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                line = line.replace('\r\n','').replace('\n','').replace('\r','')
                yield line.split(' ')

sentences = MySentences('/home/liyt/code/text_classification_v1.1/data/all') # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences)
#print model
#print model['美女']
for w in model.most_similar('梅西'):
    print w[0],w[1]
output = 'demo0713.model'
model.save(output)
model.wv.save_word2vec_format('vectors.bin',binary=True)
