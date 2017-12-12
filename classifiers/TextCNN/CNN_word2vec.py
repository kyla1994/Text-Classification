#coding:utf-8

import gensim
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Input, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import numpy as np


if __name__ == '__main__':

    dic = {}
    lis = ['auto', 'culture', 'entertainment', 'history', 'house', 'military', 'politics', 'sports', 'technology']
    i = 0
    for li in lis:
        dic[li] = i
        i += 1

    # half_file = '/home/liyt/code/text_classification/data/all_seg_stop/'
    # texts = []
    # labels = []
    # for i in range(9):
    #     infile = half_file + str(i) + '.txt'
    #     with open(infile, 'r') as fr:
    #         for line in fr.readlines():
    #             sent = line.replace('[', '').replace('\n','').replace('\r','')
    #             sents = sent.split(" | ")
    #             seg_line = " ".join(sents)
    #             texts.append(seg_line)
    #             labels.append(i)
    texts = []
    labels = []
    infile = '/home/liyt/code/text_classification_v1.1/data/all/all.txt'
    with open(infile, 'r') as fr:
        for line in fr.readlines():
            sent = line.replace('\n', '').replace('\r', '')
            sents = sent.split("__label__")
            texts.append(sents[0])
            labels.append(dic[sents[1]])

    #首先一些先设定一些会用到的参数
    MAX_SEQUENCE_LENGTH = 500  # 每条新闻最大长度
    EMBEDDING_DIM = 100  # 词向量空间维度
    TEST_SPLIT = 0.2  # 测试集比例
    MAX_NB_WORDS = 70000 # 整体词库字典中，词的多少，可以略微调大或调小
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    labels = to_categorical(np.asarray(labels))
    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)

    #再将处理后的新闻数据按 8：2 分为训练集，测试集
    p2 = int(len(data) * (1 - TEST_SPLIT))
    x_train = data[:p2]
    y_train = labels[:p2]
    x_test = data[p2:]
    y_test = labels[p2:]
    print 'train docs: ' + str(len(x_train))
    print 'test docs: ' + str(len(x_test))

    # VECTOR_DIR = '/home/liyt/code/text_classification/preproccess/vectors.bin' # 词向量模型文件
    # w2v_model = gensim.models.KeyedVectors.load_word2vec_format(VECTOR_DIR, binary=True)
    #vec+=self.model[word].reshape((1,size))
    w2v_model = gensim.models.Word2Vec.load('/home/liyt/code/text_classification/preproccess/demo0713.model')
    embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        if  word in w2v_model:
            embedding_matrix[i] = np.asarray(w2v_model[word]) #, dtype='float32'
    embedding_layer = Embedding(len(word_index) + 1, EMBEDDING_DIM, weights=[embedding_matrix],
                                input_length=MAX_SEQUENCE_LENGTH, trainable=False)

    # 搭建模型
    model = Sequential()
    model.add(embedding_layer)
    model.add(Dropout(0.2))
    model.add(Conv1D(250, 3, padding='valid', activation='relu', strides=1))
    model.add(MaxPooling1D(3))
    model.add(Flatten())
    model.add(Dense(EMBEDDING_DIM, activation='relu'))
    model.add(Dense(labels.shape[1], activation='softmax'))
    model.summary()  # plot_model(model, to_file='model.png',show_shapes=True)
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    model.fit(x_train, y_train, epochs=2, batch_size=128)
    model.save('word_vector_cnn.h5')
    print model.evaluate(x_test, y_test)



