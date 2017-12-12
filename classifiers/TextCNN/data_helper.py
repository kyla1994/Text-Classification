#coding:utf-8
from __future__ import print_function

import os
import sys
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model

import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()

if __name__ == '__main__':

    BASE_DIR = ''
    GLOVE_DIR = BASE_DIR + '/glove.6B/'
    TEXT_DATA_DIR = BASE_DIR + '/20_newsgroup/'
    MAX_SEQUENCE_LENGTH = 1000
    MAX_NB_WORDS = 20000
    EMBEDDING_DIM = 100
    VALIDATION_SPLIT = 0.2


    with open('/home/liyt/code/text_classification/preproccess/stopwords.txt', 'r') as fr:
        stoplist = set([w.strip() for w in fr.readlines()])

    import re

    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    half_file = '/home/liyt/code/text_classification/data/all/'
    texts = []
    labels = []

    for i in range(9):
        infile = half_file + str(i) + '.txt'
        cnt = 0
        with open(infile, 'r') as fr:
            for line in fr.readlines():
                sent = line.replace('[', '')

                seg_line = ' '.join([w for w in jieba.cut(sent, cut_all=False) \
                                     if
                                     w not in stoplist and not w.isspace() and not w.isdigit() and not value.match(w)])
                texts.append(seg_line)
                labels.append(i)

    tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)

    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    labels = to_categorical(np.asarray(labels))
    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)

    # split the data into a training set and a validation set
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)
    data = data[indices]
    labels = labels[indices]
    nb_validation_samples = int(VALIDATION_SPLIT * data.shape[0])

    x_train = data[:-nb_validation_samples]
    y_train = labels[:-nb_validation_samples]
    x_val = data[-nb_validation_samples:]
    y_val = labels[-nb_validation_samples:]

    print(len(x_train))
