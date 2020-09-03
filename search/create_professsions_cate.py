# coding: utf-8
import fasttext
import numpy as np

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


def create():









create()