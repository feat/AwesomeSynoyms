from __future__ import print_function
from __future__ import division

import os
import sys
from absl import flags
from absl import logging
# import jiagu
import jieba
import jieba.posseg as pseg
import jieba.analyse
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import synonyms

import json
import string

jieba.load_userdict("./dataset/userdict.txt")
jieba.analyse.set_stop_words("./dataset/stopwords.txt")

def search():
    with open('ApplicationsKwords.json', 'r', encoding='utf-8') as fp:
        appl_list = json.load(fp)

    input_text = "我昨天被老师批评了，说考试分太低，拖了全班的后腿。"

    jieba_kwords = []
    for x, w in jieba.analyse.textrank(input_text, withWeight=True):
        print('%s %s' % (x, w))
        jieba_kwords.append(x)

    text = input_text
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=1)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    # print( '关键词：' )
    words = []
    for item in tr4w.get_keywords(5, word_min_len=1):
        words.append(item.word)
    # print(",".join(words))

    phrases = tr4w.get_keyphrases(keywords_num=5, min_occur_num=1)
    # print(",".join(phrases))

    phrases.extend(words)
    # print(list(set(phrases+words)))
    tr4w_kwords = []
    for i in phrases:
        if i not in tr4w_kwords:
            tr4w_kwords.append(i)
    # print(tr4w_kwords)

    tr4w_kwords.extend(jieba_kwords)
    all_kwords = tr4w_kwords
    print("all key words:" + str(all_kwords))
    nearby_words = []
    for word in all_kwords:
        nearby_words.extend(synonyms.nearby(word)[0])
    print(nearby_words)
    all_kwords.extend(nearby_words)

    for app in appl_list:
        for word in all_kwords:
            # print(app)
            if word in app['kwords']:
                print('%s %s', (word, app['text']))


search()