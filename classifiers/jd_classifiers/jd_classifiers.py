# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 08:18:25 2017

@author: liyt
"""
import  datetime


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


class jd_classifer(object):  # 经典分类器，使用tf-idf作为特征，用chi2进行特征选择
    def __init__(self, documents, labels, select_chi2, clf):
        self.documents = documents
        self.labels = labels
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.tfidf_vectorizer = None  # tf-idf统计
        self.select_chi2 = select_chi2
        self.ch2 = None
        self.clf = clf

    def feature_select(self):
        ## 使用chi2进行特征选择,Extracting k-best features by a chi-squared test
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
        tfidf = self.tfidf_vectorizer.fit_transform(self.documents)  # 文本分词后的结果，词之间以空格隔开

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(tfidf, self.labels, test_size=0.25,
                                                                                random_state=33)

        self.ch2 = SelectKBest(chi2, k=self.select_chi2)
        self.X_train = sparse.csr_matrix(self.ch2.fit_transform(self.X_train, self.y_train))
        self.X_test = sparse.csr_matrix(self.ch2.transform(self.X_test))

    def train(self):
        print('_' * 80)
        print("Training: ")
        print(self.clf)

        self.clf.fit(self.X_train, self.y_train)
        pred = self.clf.predict(self.X_test)

        score = metrics.accuracy_score(self.y_test, pred)  # 精确度：precision
        print("accuracy:   %0.3f" % score)

    def predict(self, texts):
        freq = sparse.csr_matrix(self.ch2.transform(self.tfidf_vectorizer.transform(texts)))
        topics = self.clf.predict(freq)
        return topics


## 使用经典分类器，进行文本分类
select_chi2 = 200  # 保留的特征数，可调


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
    classifer = jd_classifer(texts, labels, select_chi2, clf)
    classifer.feature_select()  # 使用chi2进行特征选择

    classifer.train()
    end = datetime.datetime.now()
    print str(end - begin)+' s'
    #print classifer.predict(documents[:1])  # 该函数的输入值：列表类型

