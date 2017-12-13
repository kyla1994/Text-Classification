#coding: utf-8

from database import Database
import traceback

def write_add(filename, content):
    fo = open(filename, 'a')
    fo.write(content)
    fo.close()

def select_news(sql,label):
    db = Database()
    db.connect('crawl_data')
    try:
        search_result = db.query(sql,label)
        return search_result
    except Exception, e:
        print e
        traceback.print_exc()
    db.close()

if __name__ == '__main__':
    #labels = ['auto','house','military','culture','technology','entertainment','history','politics','sports']
    labels = [ 'military']
    for label in labels:
        sql = "SELECT content FROM news where label=%s "
        res = select_news(sql, label)
        for news in res:
            print news
            if label == 'technology':
                write_add('it.txt',news['content']+'\n')
            else:
                write_add(label+'.txt', news['content'] + '\n')
    # sql = "SELECT title FROM news"
    # db = Database()
    # db.connect('crawl_data')
    # res = db.query(sql)
    #
    # for news in res:
    #     write_add('it.txt', news['title'] + '\n')



