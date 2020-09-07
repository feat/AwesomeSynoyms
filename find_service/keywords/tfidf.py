# -*- coding: utf-8 -*-

import os
import sys 
sys.path.append("..")
import jieba
import jieba.analyse
# from dataset import STOPWORDS

# 加载用户自定义字典
# jieba.load_userdict("../dataset/userdict.txt")
# 加载用户自定义停止词
# jieba.analyse.set_stop_words("../dataset/stopwords.txt")

APPL_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TfidfKeywords:
    def __init__(self, delete_stopwords=True, topK=20, withWeight=False):
        if delete_stopwords:
            jieba.analyse.set_stop_words(APPL_DIR_PATH + "/dataset/stopwords.txt")

        self.topk = topK
        self.with_wight = withWeight

    def keywords(self, sentence):
        return jieba.analyse.extract_tags(sentence, topK=self.topk, withWeight=self.with_wight)
