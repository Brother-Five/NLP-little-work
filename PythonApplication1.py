# -*- coding: UTF-8 -*-
from gensim import corpora,models,similarities
import re
import os
import jieba
from pprint import pprint
import numpy as np
import wx
import GUI
######################################################################################################3
#初始化区
#xml文件的地址
corpus_list='C:\\Users\\丁\\Desktop\\14AI-01-LSI-丁俊夫\\data-figure'
#models_list='Y:\\aitest\\test\\models'

#全部的文档都放在xmls里面
textquest=''
textquest2=''

#把string看成raw的去匹配     最短的
regex_Q=re.compile(b'(?<=<Q>)([\x80-\xff]*?)(?=</Q>)')#只匹配utf_8的中文
#regex_A=re.compile(b'(?<=<A>)(.*?)(?=</A>)',re.S)
dictionary = corpora.Dictionary()#初始化词典

###########################################################################################################
#迭代器定义区

class cutting(object):
    def __init__(self,raw_str):
        self.raw_str = raw_str
    def __iter__(self):
        for word in jieba.cut(self.raw_str):
            yield(word)


#读取xml文档
class BankDoc(object):
    def __init__(self,root_dir):
        self.root_dir = root_dir

    #类里面的迭代器
    def __iter__(self):
        for name in os.listdir(self.root_dir):
            #if os.path.isfile(os.path.join(self.root_dir,name)):
            #用r的方式读出原始字符串
            data = open(os.path.join(self.root_dir,name),'rb').read()

            quest=regex_Q.findall(data)
            #把文档里面的每一个问句进行处理
            for i in range(len(quest)):
                   quest[i]=(quest[i].decode(encoding='utf-8'))
            #由列表转成字符串
            quest=''.join(quest)
            quest=''.join(' '.join(cutting(quest)))      
            yield(name,quest)
           

class BankCorpus(object):
    def __init__(self,root_dir,dictionary):
        self.root_dir = root_dir
        self.dictionary= dictionary
    
    def __iter__(self):
        for name,quest in BankDoc(self.root_dir):
            yield self.dictionary.doc2bow(jieba.cut(quest,cut_all=False))
######################################################################################################################
#字典扩大
for name,quest in BankDoc(corpus_list):
    dictionary.add_documents([quest.split()])
    #pprint(quest)
#######################################################################################################################
#构成词袋（bag of word）    input的是要unicode
#构成语料库（得到了对应每一个XML文件的稀疏向量）
corpus = list(BankCorpus(corpus_list, dictionary))
#print(corpus)
#######################################################################################################################
#tf-idf模型
#用词库构建tfidf库
tfidf = models.TfidfModel(corpus)

#用词频表示文档向量，表示为一个用tf-idf值表示的文档向量
corpus_tfidf = tfidf[corpus]
#逐个打印
'''
i=0
for doc in corpus_tfidf:
  print('doc:',i,':',doc)
  i=i+1
del i#释放内存
'''

similarity = similarities.Similarity('Similarity-tfidf-index', corpus_tfidf, num_features=500)  
#模型的保存
#tfidf.save(os.path.join(models_list,'\\model.tfidf'))
#模型的读取
#tfidf = models.TfidfModel.load(os.path.join(self.root_dir,"\\model.tfidf"))
##########################################################################################################################
#LSI模型
#用文档向量训练一个LSI模型
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
#print('LSI模型建立成功!')

#逐个打印

i=0
for t in lsi.print_topics(5):
    print('[话题 #%s]:'%i,t)
    i+=1
del i#释放内存


#建立索引
index = similarities.MatrixSimilarity(lsi[corpus])
#分界线
########################################################################################################
#GUI窗口
class MainWindow(GUI.MyFrame1): 
    '''def init_main_window(self): 
        self.InPut.SetValue('无')'''
    def __init__(self,parent): 
      GUI.MyFrame1.__init__(self,parent)

    def Main_button_click(self, event):

        similarity = similarities.Similarity('Similarity-tfidf-index', corpus_tfidf, num_features=500) #后来加进去的

        IN_Q1 = str(self.InPut.GetValue()) 
        #print('###################################################################################################################')
        ################################################################################################################################
        #分类算法（问句处理）
        '''print('请问，有什么可以帮到您:')
        #IN_Q1='我要过来办信用卡'#调试使用
        IN_Q1=input()'''
        vec_bow=dictionary.doc2bow(list(jieba.cut(IN_Q1)))
        print(vec_bow)
        #################################################################################################################################
        #LSI模型的分类
        vec_lsi=lsi[vec_bow]
        print('用LSI模型识别成功！')
        pprint(vec_lsi)
        sims=index[vec_lsi]
        #文档和代表的序号：0：个人电子银行。1：个人金融。2：企业电子银行。3：其他。 4：投资理财。
        fix_doc=[0,sims[0]]
        for t in range(4):
            if fix_doc[1]<sims[t+1]:
                fix_doc[1]=sims[t+1]
                fix_doc[0]=t+1
            else:
                pass
        var_fix_doc=['个人电子银行','个人金融','企业电子银行','其他','投资理财']
        print('LSI模型识别结果：数据编号：',fix_doc[0]) 
        pprint(sims[:10])
        #####################################################################################################################################
        #TF-IDF模型的分类                               
        similarity.num_best = 5  
        test_corpus_tfidf_1=tfidf[vec_bow]  
        print('用tfidf模型识别成功')
        sim_tfidf=similarity[test_corpus_tfidf_1]
        pprint(sim_tfidf) 
        print('TFIDF模型识别结果：数据编号：',sim_tfidf[0][0]) 
        ########################################################################################################################################
        #对结果做比较
        if sim_tfidf[0][0]==fix_doc[0]:
            print('两个模型的结果一致!识别结果是：')
            print('数据库编号：',fix_doc[0],'\n 您的问题属于《',var_fix_doc[fix_doc[0]],'》的领域')
        else:
            print('两个模型的结果有差异!识别结果分别是：')
            print('数据库编号：',sim_tfidf[0][0],'和',fix_doc[0])

        #打印分界线
        #print('#########################################################################################################################################')
        print('请稍候。。。')
        #print(vec_bow)
        ########################################################################################################################################
        #删除前面tfidf模型，防止冲突
        del similarity
        ##########################################################################################################################################
        #答案匹配方法
        #用每一个问题加答案去算出向量，并一个一个地去和query算相似度并排名
        #打开对应的文档
        all_list=os.listdir(corpus_list)
        data_F = open(os.path.join(corpus_list,all_list[fix_doc[0]]),'rb').read()
        #匹配（答案+问题），来计算向量
        regex_QA=re.compile(b'(?<=<Q>)(.*?)(?=</A>)',re.S)
        data_QA=regex_QA.findall(data_F)#正则表达式获得一个LIST
        dictionary_2 = corpora.Dictionary()#初始化词典2
        #初始化
        dict_bow_2 = [0]*len(data_QA)
        data_QA1=[0]*len(data_QA)
        #训练第二个词袋模型
        for u in range(len(data_QA)):
            data_QA[u]=( data_QA[u].decode(encoding='utf-8'))
            data_QA1[u]=data_QA[u]
            data_QA[u]=''.join(' '.join(cutting(data_QA[u])))
            dictionary_2.add_documents([data_QA[u].split()])
            dict_bow_2[u]=dictionary_2.doc2bow(list(jieba.cut(data_QA1[u])))
            data_QA1[u]=data_QA1[u].replace('\r','').replace('\n','').replace('\u3000','').replace('</Q>','').replace('<A>','').replace('\xa0','')
            
        #print(dict_bow_2)

        #构建每个问答的tfidf模型
        tfidf_QA = models.TfidfModel(dict_bow_2)
        corpus_tfidf_QA = tfidf_QA[dict_bow_2]
        similarity_QA = similarities.Similarity('Similarity-tfidf-index-QA',corpus_tfidf_QA, num_features=2000)
        #问句向量化
        vec_bow_QA=dictionary_2.doc2bow(list(jieba.cut(IN_Q1)))
        similarity_QA.num_best = 5  
        test_corpus_tfidf_QA=tfidf_QA[vec_bow_QA]  
        #print('用tfidf模型识别答案成功')
        sim_tfidf_QA=similarity_QA[test_corpus_tfidf_QA]
        #pprint(sim_tfidf_QA)
        ###########################################################################################################################################
        #LSI模型答案匹配
        lsi_QA = models.LsiModel(corpus_tfidf_QA, id2word=dictionary_2, num_topics=len(data_QA))
        index_QA = similarities.MatrixSimilarity(lsi_QA[dict_bow_2])
        vec_lsi_QA=lsi_QA[vec_bow_QA]
        sims_LSI=index_QA[vec_lsi_QA]
        #用LSI模型匹配出最可能的结果：
        #pprint(sims_LSI)
        #print(np.argmax(sims_LSI))
        print('##################################################################################################################################')

        print('您是不是在问：\n\t\n\t')
        pprint(data_QA1[np.argmax(sims_LSI)])
        ##########################################################################################################################################
        ##########################################################################################################################################
        #后打印tfidf模型的答案
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('或者你在问下列问题：')
        for i in range(len(sim_tfidf_QA)):
           print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
           pprint(data_QA1[sim_tfidf_QA[i][0]])

        self.OutPut.SetValue(data_QA1[np.argmax(sims_LSI)])

    def ClearAll(self, event):
        self.InPut.Clear()
        self.OutPut.Clear()

app = wx.App(False) 
frame = MainWindow(None) 
frame.Show(True) 
#start the applications 
app.MainLoop() 






 