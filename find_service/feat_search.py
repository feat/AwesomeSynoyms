#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :feat_search.py
@说明        :根据场景，查找服务
@时间        :2020/09/07 12:04:53
@作者        :王力
@版本        :1.0
'''


from __future__ import print_function
from __future__ import division

import os
import sys
sys.path.append("..")
from absl import flags
from absl import logging
# import jieba
import jieba
# import jieba.posseg as pseg
import jieba.analyse
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import synonyms
from find_service.keywords.tfidf import TfidfKeywords

import json
import string

APPL_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# 加载用户自定义字典
jieba.load_userdict(APPL_DIR_PATH + "/dataset/userdict.txt")
# 加载用户自定义停止词
jieba.analyse.set_stop_words(APPL_DIR_PATH + "/dataset/stopwords.txt")


def search(input_text):
    with open(APPL_DIR_PATH + '/ApplicationsKwords.json', 'r', encoding='utf-8') as fp:
        appl_list = json.load(fp)

    jieba_kwords = []
    for x, w in jieba.analyse.textrank(input_text, withWeight=True):
        # print('%s %s' % (x, w))
        jieba_kwords.append(x)
    
    # tr4w_kwords = get_kwords_by_textrank(input_text)
    # tr4w_kwords.extend(jieba_kwords)
    # all_kwords = tr4w_kwords

    tfidf_kwords = []
    for x in get_tfidf_keywords(input_text, delete_stopwords=True, topK=5, withWeight=False):
        tfidf_kwords.append(x)
    
    tfidf_kwords.extend(jieba_kwords)
    all_kwords = list(set(tfidf_kwords))
    print("all key words:" + str(all_kwords))

    # 获取关键词的近义词
    nearby_words = []
    for word in all_kwords:
        nearby_words.extend(synonyms.nearby(word)[0][0:5])
    print(nearby_words)
    all_kwords.extend(nearby_words)
    all_kwords = list(set(all_kwords))

    re_appl = []
    for app in appl_list:
        for word in all_kwords:
            # print(app)
            if word in app['kwords']:
                print("%s %s", (word, app['text']))
                re_appl.append(app['text'])
    return re_appl



def get_kwords_by_textrank(text):
    """由text rank 算法来生成key words

    Args:
        text (string): 句子或文章

    Returns:
        list: kwords 
    """
    tr4w = TextRank4Keyword()
    # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    tr4w.analyze(text=text, lower=True, window=1)

    # print( '关键
    words = []
    for item in tr4w.get_keywords(5, word_min_len=1):
        words.append(item.word)
    # print(",".join(words))

    phrases = tr4w.get_keyphrases(keywords_num=5, min_occur_num=1)

    phrases.extend(words)
    # print(list(set(phrases+words)))
    tr4w_kwords = []
    for i in phrases:
        if i not in tr4w_kwords:
            tr4w_kwords.append(i)
    return tr4w_kwords   

def get_tfidf_keywords(text, delete_stopwords=True, topK=20, withWeight=True):
    """
    tfidf算法 提取关键词
    :param text: 文本
    :param delete_stopwords: 是否删除停用词
    :param topK: 输出关键词个数
    :param withWeight: 是否输出权重
    :return: [(word, weight), (word1, weight1)]
    """
    tfidf = TfidfKeywords(delete_stopwords=delete_stopwords, topK=topK, withWeight=withWeight)
    keywords = tfidf.keywords(text)
    print("tfidf keywords result: {}\n".format(keywords))
    return keywords


if __name__ == '__main__':
    input_text = "我昨天被老师批评了，说考试分太低，拖了全班的后腿。"
    print(search(input_text))
