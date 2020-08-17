from __future__ import print_function
from __future__ import division

import os
import sys
from absl import flags
from absl import logging

import synonyms
import json
from models import kmcha_crawler_model

#use various tech to find the synonym for the input "word"
def findSynonyms(word):
    #import the professions file
    with open('./dataset/profession.json', 'rb') as jsonfile:
        profession_json = json.load(jsonfile, encoding='utf-8')

    profession_set = set()
    for profession in profession_json['data']:
        profession_set.add(profession['name'])

    #find the nearby words in Synonyms module
    nearby_words = synonyms.nearby(word)
    if  len(nearby_words[0]):
        s_words = nearby_words[0][0:5]
        print (s_words)
        
    #if nearby_word not found, using word segmentation（分词）    
    else:
        seg_words = [] #分词
        seg = synonyms.seg(word)
        for i, v in enumerate(seg[1]):
            if v == 'n':
                seg_words.append(seg[0][i])
        s_words = seg_words 

    #use kmcha to search synonyms 
    km_words = kmcha_crawler_model.kmcha_search((word, '01'))

    #insert kmcha result into already found synonyms
    for word in km_words:
        if word  not in s_words:
            s_words.append(word)

    #add synonyms to result if exist in professions lists    
    result = []
    for profession in profession_set:
        for seg in s_words:
            if seg == profession or seg in profession:
                result.append(profession)

    return result

if __name__ == '__main__':
    print(findSynonyms(('老师')))

