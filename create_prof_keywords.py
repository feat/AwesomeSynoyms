#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :create_prof_keywords.py
@说明        :生成职业的关键词，并保存到文件
@时间        :2020/09/07 10:38:54
@作者        :王力
@版本        :1.0
'''

from __future__ import print_function
from __future__ import division

import os
import sys
from absl import flags
from absl import logging

import json
from ltp import LTP


def create():
    """create profession keywords json file.
    """
    ltp = LTP()  # 默认加载 Small 模型
    # import the professions file
    with open('./dataset/profession.json', 'rb') as jsonfile:
        profession_json = json.load(jsonfile, encoding='utf-8')

    for i, profession in enumerate(profession_json['data']):
        profession_json['data'][i]['kwords'] = find_kwords_by_ltp(
            profession['name'], ltp)

    with open('./dataset/profession2.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(profession_json, jsonfile, ensure_ascii=False)


def find_kwords_by_ltp(text, ltp):
    """find_kwords_by_ltp

    Args:
        text (string): text
        ltp (LTP object): [description]

    Returns:
        string: keyword
    """
    seg, hidden = ltp.seg([text])
    srl = ltp.srl(hidden)
    dep = ltp.dep(hidden)
    # print(seg)
    # print(dep)

    att = 0
    hed = 0
    dep = dep[0]
    for e in dep:
        l_e = list(e)
        if l_e[2] == 'ATT':  # ATT 表示定语修饰
            att = l_e[1]
        # HED 表示核心关系,其它关系可参考https://blog.csdn.net/asialee_bird/article/details/102610588
        elif l_e[2] == 'HED' and l_e[1] == 0:
            hed = l_e[0]

    if att != 0 and hed != 0 and att == hed:  # 策略是同时满足时候，判定该词语为key word
        return seg[0][att-1]
    return ''


create()
