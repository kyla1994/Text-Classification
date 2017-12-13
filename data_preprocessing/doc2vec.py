# -*- coding:utf-8 -*-
import math
import codecs
import jieba
from time import time
import numpy as np
import pandas as pd

import re
import string
import nltk

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split

from sklearn.feature_selection import SelectKBest, chi2

from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

import gensim
from gensim.models import doc2vec
from gensim.models.doc2vec import Doc2Vec, LabeledSentence

LabeledSentence = gensim.models.doc2vec.LabeledSentence

# ## 分词
# ## 为简化起见，9种语料每种只选择100个文档
# with open('/home/wangwenhui/Documents/NLP_homework/stopwords.txt', 'r') as fr:
#     stoplist = set([w.strip() for w in fr.readlines()])
#
# import re
#
# value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
#
#
# def write_add(path, line):
#     with open(path, 'a') as fw:
#         fw.write(line)
#

# half_file = '/home/wangwenhui/Documents/NLP_homework/all/'
# file_seg_path = '/home/wangwenhui/Documents/NLP_homework/all_seg_stop/00.txt'
# documents = []
# labels = []
#
# for i in range(9):
#     infile = half_file + str(i) + '.txt'
#     cnt = 0
#     with open(infile, 'r') as fr:
#         for line in fr.readlines():
#             if cnt >= 100:
#                 break
#             sent = line.replace('[', '')
#
#             seg_line = [w for w in jieba.cut(sent, cut_all=False) \
#                         if w not in stoplist and not w.isspace() and not w.isdigit() and not value.match(w)]
#             documents.append(seg_line)
#             labels.append(i)
#             cnt += 1
#             # write_add(file_seg_path, seg_line)

train_path = '/home/liyt/code/text_classification_v1.1/data/data_tiny/all2.txt'#'/home/liyt/code/text_classification_v1.1/data/all_seg.txt'
#test_path = '/home/liyt/code/text_classification_v1.1/data/data_split_seg_stops/testsets.txt'

documents = []
labels = []


cnt = 0

# with open(test_path, 'r') as fr:
#     for line in fr.readlines():
#         line = line.replace('\n', '')
#         items = line.split('__label__')
#         try:
#             sent, label = items[0], items[1]
#             documents.append(sent)
#             labels.append(label)
#             cnt+=1
#             if cnt>4999:
#                 break
#         except:
#             pass

with open(train_path, 'r') as fr:
    for line in fr.readlines():
        line = line.replace('\n', '')
        items = line.split('__label__')
        try:
            sent, label = items[0], items[1]
            documents.append(sent)
            labels.append(label)
            cnt+=1
            # if cnt>1000:
            #     break
        except:
            pass

print cnt

print "all nums:"+str(len(labels))


class Get_doc2vec(object):
    def __init__(self, documents):
        self.documents = documents

        # doc2vec有DM和DBOW两种模型
        self.model_dm = None
        self.model_dbow = None


        ##对数据进行训练得到model,size是向量的维度,epoch_num是迭代步数，size和epoch_num均可调

    def train_model(self, size=100, epoch_num=20):
        # Gensim的Doc2Vec应用于训练要求每一篇文章/句子有一个唯一标识的label.
        def labelize(X):
            labelize_docs = []
            for i, v in enumerate(X):
                labelize_docs.append(LabeledSentence(v, [i]))
            return labelize_docs

        self.documents = labelize(self.documents)
        self.model_dm = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, workers=3)
        self.model_dbow = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, dm=0,
                                                workers=3)
        # 使用所有的数据建立词典
        self.model_dm.build_vocab(self.documents)
        self.model_dbow.build_vocab(self.documents)
        self.model_dm.train(self.documents, total_examples=len(self.documents), epochs=epoch_num)
        self.model_dbow.train(self.documents, total_examples=len(self.documents), epochs=epoch_num)

    # 读取向量
    def getVecs(self):
        dm = np.concatenate([np.array(self.model_dm.docvecs[z.tags[0]]).reshape((1, -1)) for z in self.documents])
        dbow = np.concatenate([np.array(self.model_dbow.docvecs[z.tags[0]]).reshape((1, -1)) for z in self.documents])
        return np.hstack((dm, dbow))

    # 得到待预测文档的向量表示
    def get_new_d2v(self, doc):
        return np.hstack((np.array(d2v.model_dm.infer_vector(doc)), np.array(d2v.model_dbow.infer_vector(doc))))


class D2V_classifer(object):
    def __init__(self, documents, labels, clf):
        self.documents = documents
        self.labels = labels
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.clf = clf

    def train(self):

        # 由于MultinomialNB（）分类器的特征值不能为负值，因此需要加判断：如果clf是MultinomialNB，就不执行
        if type(self.clf) == MultinomialNB:
            return
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.documents, self.labels,
                                                                                test_size=0.25, random_state=33)
        self.clf.fit(self.X_train, self.y_train)

        # 准确度
        pred = self.clf.predict(self.X_test)
        score = metrics.accuracy_score(self.y_test, pred)
        print("accuracy:   %0.3f" % score)

    def predict(self, doc):
        if type(self.clf) == MultinomialNB:
            return

        return self.clf.predict(doc)


## 用语料库documents训练doc2vec
d2v = Get_doc2vec(documents)  # 类初始化,实例名d2v
d2v.train_model()
docs_vec = d2v.getVecs()  # documents的向量表示

## 分类器，进行文本分类
# 下面分类器的初始化参数，可调
for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
        (Perceptron(n_iter=50), "Perceptron"),
        (KNeighborsClassifier(n_neighbors=100, algorithm='brute'), "kNN"),
        (LogisticRegression(), "LogisticRegression"),
        (RandomForestClassifier(n_estimators=30), "Random forest"),
        (LinearSVC(loss='l2', penalty="l1", dual=False, tol=1e-3), "LinearSVC penalty= l1"),
        (LinearSVC(loss='l2', penalty="l2", dual=False, tol=1e-3), "LinearSVC penalty= l2"),
        (MultinomialNB(), "MultinomialNB")):
    print('=' * 80)
    print(name)

    classifer = D2V_classifer(docs_vec, labels, clf)  # docs_vec:语料文档的向量表示

    classifer.train()

    print classifer.predict(d2v.get_new_d2v(documents[0]))
    # 举例示范，d2v.get_new_d2v(documents[0])的参数值只能是一个文档，不能是列表。该文档的形式为['中国', '大使馆',...]




