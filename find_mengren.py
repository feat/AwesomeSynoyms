#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :find_mengren.py
@说明        :寻找猛人
@时间        :2020/09/07 11:51:44
@作者        :王力
@版本        :1.0
'''


from __future__ import print_function
from __future__ import division

import os
import sys
from absl import flags
from absl import logging

import synonyms
import json
from models import kmcha_crawler_model


def find_synonyms(word):
    """ use various tech to find the synonym for the input "word"

    Args:
        word (string): [description]

    Returns:
        list: [description]
    """
    # import the professions file
    with open('./dataset/profession2.json', 'rb') as jsonfile:
        profession_json = json.load(jsonfile, encoding='utf-8')

    profession_list = []
    prof_kwords_list = []
    for profession in profession_json['data']:
        profession_list.append(profession['name'])
        prof_kwords_list.append(profession['kwords'])

    # find the nearby words in Synonyms module
    nearby_words = synonyms.nearby(word)
    if len(nearby_words[0]):
        s_words = nearby_words[0][0:5]
        print(s_words)

    # if nearby_word not found, using word segmentation（分词）
    else:
        seg_words = []  # 分词
        seg = synonyms.seg(word)
        for i, v in enumerate(seg[1]):
            if v == 'n':
                seg_words.append(seg[0][i])
        s_words = seg_words

    # use kmcha to search synonyms
    km_words = kmcha_crawler_model.kmcha_search((word, '01'))

    # insert kmcha result into already found synonyms
    for word in km_words:
        if word not in s_words:
            s_words.append(word)

    # add synonyms to result if exist in professions lists
    result = []
    for i, profession in enumerate(profession_list):
        prof_kword = prof_kwords_list[i]
        for seg in s_words:
            # if seg == profession or seg in profession: # fully match
            if seg == profession or seg == prof_kword:  # partly match only with kwords
                result.append(profession)
    return result


if __name__ == '__main__':
    print(find_synonyms(('程序')))
