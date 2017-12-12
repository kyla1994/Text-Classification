# _*_coding:utf-8 _*_
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import fasttext
import  datetime

begin = datetime.datetime.now()

#训练模型
classifier = fasttext.supervised("news_fasttext_train.txt","news_fasttext.model",label_prefix="__label__")
end = datetime.datetime.now()
print str(end - begin) + ' s'