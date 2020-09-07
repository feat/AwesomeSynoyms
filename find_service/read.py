#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :read.py
@说明        :生成应用场景的关键词
@时间        :2020/09/07 11:40:13
@作者        :王力
@版本        :1.0
'''


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

# import thulac	


# import synonyms
import json
import string
# from models import kmcha_crawler_model


jieba.load_userdict("./dataset/userdict.txt")
jieba.analyse.set_stop_words("./dataset/stopwords.txt")

# import the professions file
with open('./dataset/profession.json', 'rb') as jsonfile:
    profession_json = json.load(jsonfile, encoding='utf-8')

profession_set = set()
for profession in profession_json['data']:
    profession_set.add(profession['name'])

# import the user_expertise file
with open('./dataset/user_expertise.json', 'rb') as jsonfile:
    user_expertise_json = json.load(jsonfile, encoding='utf-8')    

user_expertise_list = []
for user_expertise in user_expertise_json['data']:
    user_expertise_list.append(user_expertise)
#    print (user_expertise['available_services'])


profession_categories_all = []
# Professions
file_prof = open('Professions.txt', 'w', encoding='utf-8')
# Applications
file_appl = open('Applications.txt', 'w', encoding='utf-8')
file_appl_list = []
# jieba.enable_paddle()
# thu1 = thulac.thulac()  # 默认模式

for v in user_expertise_list:
    # print(v)
    # 专长 适用情形(applications) 聘用岗位(available_services) 职业
    expertise = v['name']
    applications = []
    available_services = []
    profession_categories = []
    id = v['id']

    file_prof.write(str(id) + " ")
    # file_appl.write(str(id) + " ")
    for v2 in v['applications']:
        applications.append(v2['label'])
        v2['label'] = str(v2['label'].strip(string.punctuation))

        text = v2['label']
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
        kwords = []
        for i in phrases:
            if i not in kwords:
                kwords.append(i)
        print(kwords)

        if text != "":
            file_appl.write((text) + "\n")

        app_info = {}
        app_info['id'] = id
        app_info['text'] = text
        app_info['kwords'] = kwords
        file_appl_list.append(app_info)
    for v2 in v['available_services']:
        service = v2['name'].split('|')[0].strip()
        if service not in available_services:
            available_services.append(service)
    for v2 in v['profession_categories']:
        profession_categories.append(v2['name'])
        for p in profession_categories:
            file_prof.write(str(p) + ",")
        # profession_categories_all.append(profession_categories)
    file_prof.write("\n")
    # file_appl.write("\n")

# print(profession_categories_all)
file_prof.close()
file_appl.close()
# print(file_appl_list)
with open('ApplicationsKwords.json', 'w', encoding='utf-8') as fp:
    json.dump(file_appl_list, fp, ensure_ascii=False)