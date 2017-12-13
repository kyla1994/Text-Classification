#coding:utf-8
import os
import re
import xlwt
import  sys
reload(sys)
sys.setdefaultencoding('utf-8')
def write_add(filepath, content):
    fo = open(filepath, 'a')
    fo.write(content)
    fo.write('\n')
    fo.close()

if __name__ == '__main__':
    rootdir = r'C:\code\SogouCA'
    datas = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            real_path = os.path.join(parent, filename)
            print  real_path
            with open(real_path) as file1:
                data = file1.read()
                urls = re.findall(r'<url>.*?</url>', data)
                titles = re.findall(r'<contenttitle>.*?</contenttitle>', data)
                # <contenttitle>本公司电子公告服务严格遵守</contenttitle>
                contents = re.findall(r'<content>.*?</content>', data)
                # <content>＜＜上一页　下一页＞＞</content>
                n = len(urls)
                for i in range(n):

                    if len(urls[i]) > 0:
                        try:
                            urls[i] = urls[i].replace(r'<url>', '')
                            urls[i] = urls[i].replace(r'</url>', '')
                            titles[i] = titles[i].replace(r'<contenttitle>', '')
                            titles[i] = titles[i].replace(r'</contenttitle>', '')
                            titles[i] = titles[i].strip()
                            titles[i] = titles[i].replace(' ','')
                            contents[i] = contents[i].replace(r'<content>', '')
                            contents[i] = contents[i].replace(r'</content>', '')
                            contents[i] = contents[i].strip()
                            contents[i] = contents[i].replace(' ','')
                        except:
                            pass
                        # print urls[i]
                        labs = urls[i].split('/')
                        if len(labs) > 3:
                            label = labs[2].split('.')[0]
                            # auto business it health sports travel learning career cul mil house yule women
                            if len(titles[i]) > 0 and len(contents[i]) > 0:
                                if (label == 'auto'):
                                    write_add('auto.txt', contents[i])
                                elif (label == 'business'):
                                    write_add('finance.txt',  contents[i])
                                elif (label == 'it'):
                                    write_add('it.txt', contents[i])
                                elif (label == 'health'):
                                    write_add('health.txt', contents[i])
                                elif (label == 'sports'):
                                    write_add('sports.txt', contents[i])
                                elif (label == 'travel'):
                                    write_add('travel.txt',contents[i])
                                elif (label == 'learning'):
                                    write_add('education.txt', contents[i])
                                elif (label == 'career'):
                                    write_add('jobs.txt', contents[i])
                                elif (label == 'cul'):
                                    write_add('culture.txt',contents[i])
                                elif (label == 'mil'):
                                    write_add('military.txt',
                                                  contents[i])
                                elif (label == 'house'):
                                    write_add('house.txt',
                                              contents[i])
                                elif (label == 'yule'):
                                    write_add('entertainment.txt', contents[i])
                                elif (label == 'women'):
                                    write_add('women.txt', contents[i])

