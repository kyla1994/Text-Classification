# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 08:18:25 2017

@author: liyt
"""
import  datetime
import gensim
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
from scipy import sparse
from sklearn.preprocessing import Imputer
import numpy as np

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


class jd_classifer(object):  # 经典分类器，使用word2vec作为特征
    def __init__(self, documents, labels, select_chi2,  clf):
        self.documents = documents
        self.labels = labels
        self.clf = clf
        self.select_chi2 = select_chi2
        self.model = gensim.models.Word2Vec.load('/home/liyt/code/text_classification_v1.1/data/demo0713.model')
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.documents,self.labels,test_size=0.25, random_state=33)
        self.X_train_vecs = np.concatenate([self.buildWordVector(z, 100) for z in self.X_train])
        self.X_test_vecs = np.concatenate([self.buildWordVector(z, 100) for z in self.X_test])

    def buildWordVector(self,news,size):
        vec = np.zeros(size).reshape((1,size))
        count = 0
        newsList = news.split(' ')
        for word in newsList:#
            #print word
            try:
                vec+=self.model[word].reshape((1,size))
                count +=1
            except KeyError:
                continue
        if count != 0:
            vec /= count

        #print len(newsList),count

        return vec



    # def feature_select(self):
    #     ## 使用chi2进行特征选择,Extracting k-best features by a chi-squared test
    #     self.tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
    #     tfidf = self.tfidf_vectorizer.fit_transform(self.documents)
    #
    #     self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(tfidf.toarray(), self.labels,
    #                                                                             test_size=0.25, random_state=33)
    #
    #     self.ch2 = SelectKBest(chi2, k=self.select_chi2)
    #     self.X_train = self.ch2.fit_transform(self.X_train, self.y_train)
    #     self.X_test = self.ch2.transform(self.X_test)

    def train(self):
        print('_' * 80)
        print("Training: ")
        print(self.clf)
        self.X_train_vecs = Imputer().fit_transform(self.X_train_vecs)







        self.clf.fit(sparse.csr_matrix(self.X_train_vecs), self.y_train)#self.X_train

        pred = self.clf.predict(sparse.csr_matrix(self.X_test_vecs))#self.X_test

        score = metrics.accuracy_score(self.y_test, pred)  # 精确度：precision
        print("accuracy:   %0.3f" % score)



    # def predict(self, texts):
    #     freq = self.ch2.transform(self.tfidf_vectorizer.transform(texts))
    #     topics = self.clf.predict(freq)
    #     return topics


## 使用经典分类器，进行文本分类
select_chi2 = 10000  # 保留的特征数，可调

# 下面分类器的初始化参数，可调
for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
        (Perceptron(n_iter=50), "Perceptron"),
        (LogisticRegression(), "LogisticRegression"),
        (RandomForestClassifier(n_estimators=30), "Random forest"),
        (LinearSVC(loss='l2', penalty="l1", dual=False, tol=1e-3), "LinearSVC penalty= l1"),
        (LinearSVC(loss='l2', penalty="l2", dual=False, tol=1e-3), "LinearSVC penalty= l2")):
    print('=' * 80)
    print(name)
    begin = datetime.datetime.now()
    classifer = jd_classifer(texts, labels, select_chi2, clf)
    #classifer.feature_select()  # 使用chi2进行特征选择

    classifer.train()
    end = datetime.datetime.now()
    print str(end - begin)+' s'
    #print classifer.predict(texts[:1])  # 该函数的输入值：列表类型













