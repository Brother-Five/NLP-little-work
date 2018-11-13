# -*- coding: utf-8 -*-
import logging
import os.path
import six
import sys
import re
import jieba
#from gensim.models import Word2Vec
#from gensim.models.word2vec import LineSentence

'''
usage:python xml2txt.py [Y:\aitest\test\last_vision] [BankCorpus.txt]
'''

#第二个参数是文件的路径
regex_Q=re.compile(b'(?<=<Q>)([\x80-\xff]*?)(?=</Q>)')#只匹配utf_8的中文
class cutting(object):
    def __init__(self,raw_str):
        self.raw_str = raw_str
    def __iter__(self):
        for word in jieba.cut(self.raw_str):
            yield(word)

class ReadXml(object):
    def __init__(self,root_dir):
        self.root_dir = root_dir

    #类里面的迭代器
    def __iter__(self):
        for name in os.listdir(self.root_dir):
            data= open(os.path.join(self.root_dir,name),'rb').read()
            data=data.replace(b'\xef\xbc\x8c',b'').replace(b'\n',b'')#去掉逗号

            quest=regex_Q.findall(data)
            for i in range(len(quest)):
                quest[i]=(quest[i].decode(encoding='utf-8'))
                quest[i]=''.join(' '.join(cutting(quest[i])))
            #quest=''.join(quest)
            #quest=''.join(' '.join(cutting(quest)))
            #for i in range(len(quest)):
            #    quest[i]=quest[i].split()
            yield(name,quest)




if __name__ == '__main__':#直接打开这个脚本
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) != 3:
        print("usage:python xml2txt.py [Y:\aitest\test\last_vision] [BankCorpus.txt]")
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    space = " "
    i = 0

    output = open(outp, 'w')

    for name,quest in ReadXml(inp):
        for u in range(len(quest)):
           output.write(quest[u])
           i = i + 1
           output.write('\n')
           if (i % 50 == 0):
              logger.info("Saved " + str(i) + " articles"+ 'in'+str(name))  

    output.close()
    logger.info("Finished Saved " + str(i) + " articles")
