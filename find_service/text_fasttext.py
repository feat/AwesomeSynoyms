# coding: utf-8
import fasttext
import numpy as np
from gensim.models import fasttext as FastText3
from gensim.models.wrappers import FastText as FastText2
from gensim.models import KeyedVectors
import os
import heapq

def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim

def text():
	# model = FastText('wiki.zh.bin')
	model = fasttext.load_model('wiki.zh.bin')
	
	print('load over..')


	# s1 = '水果是指多汁且有甜味的植物果实，不但含有丰富的营养且能够帮助消化。水果是对部分可以食用的植物果实和种子的统称。水果有降血压、减缓衰老、减肥瘦身、皮肤保养、明目、抗癌、降低胆固醇等保健作用。一般的水果都是生食，不经过加工，洗干净就直接吃了，这样维生素很少损失，弥补了蔬菜的不足。'
	# s2 = '在全球层面上，亚投行建立的主要背景是新兴大国的异军突起。'
	# s3 = '亚洲基础设施投资银行Asian Infrastructure Investment Bank ，简称亚投行，AIIB是一个政府间性质的亚洲区域多边开发机构。重点支持基础设施建设，成立宗旨是为了促进亚洲区域的建设互联互通化和经济一体化的进程，并且加强中国及其他亚洲国家和地区的合作，是首个由中国倡议设立的多边金融机构，总部设在北京，法定资本1000亿美元。截至2017年10月，亚投行有70个正式成员国。2013年10月2日，习近平主席提出筹建倡议，2014年10月24日，包括中国、印度、新加坡等在内21个首批意向创始成员国的财长和授权代表在北京签约，共同决定成立投行。2015年12月25日，亚洲基础设施投资银行正式成立。2016年1月16日至18日，亚投行开业仪式暨理事会和董事会成立大会在北京举行。亚投行的治理结构分理事会、董事会、管理层三层。理事会是最高决策机构，每个成员在亚投行有正副理事各一名。董事会有12名董事，其中域内9名，域外3名。管理层由行长和5位副行长组成。'
	
	s1 = '中国'
	s2 = '软件工程师'
	s3 = '程序'

	# print(model.get_nearest_neighbors(s2))
	# print (s1 in model.words)
	s1_vector = model.get_word_vector(s1)
	s2_vector = model.get_word_vector(s2)
	s3_vector = model.get_word_vector(s3)

	# print (s1_vector, s2_vector, s3_vector)

	print(cos_sim(s1_vector, s2_vector))
	print(cos_sim(s1_vector, s3_vector))
	print(cos_sim(s2_vector, s3_vector))	
	# print(cos_sim(s3, s2))
	
	# s1 = s1[:100]
	# s2 = s2[:100]
	# print(s2)
	# s3 = s3[:100]
	# print(model.similarity(s1,s2))
	# print(model.similarity(s3,s2))

def findSimilar():
	fasttext_model = fasttext.load_model('wiki.zh.bin')	
	print('load over bin file..')	

	fasttext_vec = load_vectors('wiki.zh.vec')	
	print('load over vec file..')	
	# 获取直升机的向量
	word_vec = fasttext_vec[fasttext_model.get_word_id("程序员")]
	# word_vec = model.get_word_vector("程序员")
	# 计算直升机向量与库中每个词的相似度
	sim_vec = np.dot(word_vec, fasttext_vec.T)
	# 按相似度排序词语
	sorted_sim_vec = sorted(zip(fasttext_model.get_words(), sim_vec), key=lambda x:x[1], reverse=True)
	# 获取与直升机最相似的top10词语列表
	print(sorted_sim_vec[1:10+1])	
	
import io

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data


#好像并不兼容，吐血！
def findSimilar2():
	# zh_model = FastText2.load_fasttext_format("wiki.zh.bin")
	zh_model = FastText3.load_facebook_model("wiki.zh.bin")
	# print ('程序员' in zh_model.wv.vocab)
	# words = []
	# for word in zh_model.words:
	# 	words.append(word)

	# print("预训练模型包含单词总数： {}".format(len(words)))

	# print (words[:10])

	find_similar_to = "程序员"
	for similar_word in zh_model.wv.similar_by_word(find_similar_to, topn=5):
		print("Word: {0}, Similarity: {1:.2f}".format(
			similar_word[0], similar_word[1]
		))


	# fasttext_model.wv.most_similar_cosmul(positive='苹果手机', negative='手机', topn=10)
	# fasttext_model.most_similar(positive=[vector], topn=topn, restrict_vocab=restrict_vocab)
	# print (fasttext_model.most_similar("程序员"))


# text()
# findSimilar()
# findSimilar2()









def createVector():
	import os
	model = fasttext.load_model('wiki.zh.bin')
	print('load over..')


	f = open("Applications.txt", 'r', encoding="utf8")               # 返回一个文件对象 
	f2 = open("ApplicationsVector.txt", 'w', encoding="utf8")               # 返回一个文件对象 


	line = f.readline()               # 调用文件的 readline()方法 
	while line: 
		line = str(f.readline()).replace("\n", "")
		vector = model.get_word_vector(line)
		# f2.write(line)
		vstr = ' '.join(str(i) for i in vector)
		f2.write(line + " @|@|@ " + vstr + "\n")

	f.close()
	f2.close()

def findVectors():


	model = fasttext.load_model('wiki.zh.bin')
	print('load over..')

	f2 = open("ApplicationsVector.txt", 'r', encoding="utf8")               # 返回一个文件对象 
	tvec = model.get_word_vector("我的学习成绩太差了")
	sims = []
	words = []
	line = f2.readline()               # 调用文件的 readline()方法 
	while line: 
		line = str(f2.readline()).strip('\n')
		l = line.split(" @|@|@ ")
		if len(l) < 2:
			continue
		s = l[1]
		list1 = s.split(' ')
		vector = np.array(list1, dtype=float)		
		# vector = np.fromstring(l[1], dtype=float)
		sim = cos_sim(vector, tvec)
		sims.append(sim)

    # line_num = sims.index(max(sims))
	max_num_index_list  = list(map(sims.index, heapq.nlargest(3, sims)))
	print(max_num_index_list)
	# print(words[line_num])
	f2.close()



# createVector()
findVectors()

# s = "[-1.38024967e-02 -1.42266899e-01 -1.26839429e-02 -1.46400630e-01]"

# s = s.strip('[').strip(']')
# list1 = s.split(' ')
# arr1 = np.array(list1, dtype=float)
# print(arr1)
