# -*- coding:utf-8 -*-
import math
import codecs
import jieba
from time import time
import numpy as np
import pandas as pd
import  datetime
import re
import string
import nltk

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split

from sklearn.feature_selection import SelectKBest, chi2
from scipy import sparse
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
from random import shuffle

LabeledSentence = gensim.models.doc2vec.LabeledSentence

dic = {}
lis = ['auto', 'culture', 'entertainment', 'history', 'house', 'military', 'politics', 'sports', 'technology']
i = 0
for li in lis:
    dic[li] = i
    i += 1

texts = []
labels = []
infile = '/home/liyt/code/text_classification_v1.1/data/all/all.txt'
with open(infile, 'r') as fr:
    for line in fr.readlines():
        sent = line.replace('\n', '').replace('\r', '')
        sents = sent.split("__label__")
        texts.append(sents[0])
        labels.append(dic[sents[1]])


class LabeledLineSentence(object):
    def __init__(self, documents):
        self.documents = documents

    def __iter__(self):
        for item_no, line in enumerate(self.documents):
            yield LabeledSentence((line).split(), [item_no])

    def to_array(self):
        self.sentences = []
        for item_no, line in enumerate(self.documents):
            self.sentences.append(LabeledSentence(line.split(), [item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences


class Get_doc2vec(object):
    def __init__(self, documents):
        self.documents = LabeledLineSentence(documents)

        # doc2vec有DM和DBOW两种模型
        self.model_dm = None
        self.model_dbow = None


        # 对数据进行训练得到model,size是向量的维度,epoch_num是迭代步数，size和epoch_num均可调

    def train_model(self, size=100, epoch_num=20):
        # Gensim的Doc2Vec应用于训练要求每一篇文章/句子有一个唯一标识的label.
        #         def labelize(X):
        #             labelize_docs = []
        #             for i,v in enumerate(X):
        #                 labelize_docs.append(LabeledSentence(v.split(), [i]))
        #             return labelize_docs


        #         self.documents = labelize(self.documents)
        self.model_dm = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, workers=3)
        self.model_dbow = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, dm=0,
                                                workers=3)
        # 使用所有的数据建立词典
        self.model_dm.build_vocab(self.documents.to_array())
        self.model_dbow.build_vocab(self.documents.to_array())

        # 训练
        self.model_dm.train(self.documents.to_array(), total_examples=len(self.documents.to_array()), epochs=epoch_num)
        self.model_dbow.train(self.documents.to_array(), total_examples=len(self.documents.to_array()),
                              epochs=epoch_num)

    # 读取向量
    def getVecs(self):
        dm = np.concatenate([np.array(self.model_dm.docvecs[z.tags[0]]).reshape((1, -1)) for z in self.documents])
        dbow = np.concatenate([np.array(self.model_dbow.docvecs[z.tags[0]]).reshape((1, -1)) for z in self.documents])
        return np.hstack((dm, dbow))

    # 得到待预测文档的向量表示
    def get_new_d2v(self, doc):
        return np.hstack((np.array(self.model_dm.infer_vector(doc)), np.array(self.model_dbow.infer_vector(doc))))


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
        self.clf.fit(sparse.csr_matrix(self.X_train), self.y_train)

        # 准确度
        pred = self.clf.predict(sparse.csr_matrix(self.X_test))
        score = metrics.accuracy_score(self.y_test, pred)
        print("accuracy:   %0.3f" % score)

    def predict(self, doc):
        if type(self.clf) == MultinomialNB:
            return

        return self.clf.predict(doc)


## 用语料库documents训练doc2vec
d2v = Get_doc2vec(texts)  # 类初始化,实例名d2v,documents的每个文档是由空格连接起来的
d2v.train_model()

docs_vec = d2v.getVecs()  # documents的向量表示

## 分类器，进行文本分类

# 下面分类器的初始化参数，可调
for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
        (Perceptron(n_iter=50), "Perceptron"),
        (LogisticRegression(), "LogisticRegression"),
        (RandomForestClassifier(n_estimators=30), "Random forest"),
        (LinearSVC(loss='l2', penalty="l1", dual=False, tol=1e-3), "LinearSVC penalty= l1"),
        (LinearSVC(loss='l2', penalty="l2", dual=False, tol=1e-3), "LinearSVC penalty= l2"),
        (MultinomialNB(), "MultinomialNB")):
    print('=' * 80)
    print(name)
    begin = datetime.datetime.now()
    classifer = D2V_classifer(docs_vec, labels, clf)  # docs_vec:语料文档的向量表示

    classifer.train()
    end = datetime.datetime.now()
    print str(end - begin)+' s'
    #print classifer.predict(d2v.get_new_d2v(texts[0]))
    # 举例示范，d2v.get_new_d2v(documents[0])的参数值只能是一个文档，不能是列表。该文档的形式:中国 大使馆...
