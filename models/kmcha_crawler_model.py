import os
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import traceback
import time
import sys 
sys.path.append("..") 
import thread_utils
import re
# import data_utils
import logging

logger = logging.getLogger(__name__)
local_file = os.path.split(__file__)[-1]
logging.basicConfig(
    format='%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s',
    level=logging.INFO)



def url_parse(url, word):
    word = urllib.parse.quote(word)
    url = url.format(a=word)
    return url



def get_words(soup, word, limit=0):
    result = []
    content = soup.find(text= word + "的相似词").parent.parent.find_next_sibling("p").text
    # p = re.compile('(\S+)')
    m = re.findall('(\S+)', content,re.M)
    #if limit = 0, get all values, otherwise get top limit number values
    if limit is 0:
        result = m
    else:
        result = m[0:limit]
    return result


def baike_synonym_detect(word_code_list):
    out_path = 'output/kmcha_synonym.txt'
    if os.path.exists(out_path):
        os.remove(out_path)

    multi_thread_search(word_code_list)


@thread_utils.run_thread_pool(50)
def multi_thread_search(params):
    kmcha_search(params)


def kmcha_search(params):
    key_word, word_code = params
    # key_word = data_utils.remove_parentheses(key_word)
    file = open('output/kmcha_synonym.txt', 'a', encoding='utf8')
    try:
        base_url = 'https://kmcha.com/similar/{a}'
        url = url_parse(base_url, key_word)
        response = urllib.request.urlopen(url)
        data = response.read()
        soup = BeautifulSoup(data,features="html.parser")

        # item_json = dict()

        # des_dict = get_description(soup)
        # item_json.update(des_dict)

        # info_box_dict = get_info_box(soup)
        # item_json.update(info_box_dict)

        # synonym_list = get_synonym(item_json)
        synonym_list = get_words(soup, key_word)
        if len(synonym_list) > 0:
            write_line = word_code + '\t' + key_word + '\t' + '|'.join(synonym_list) + '\n'
            file.write(write_line)

        logger.info(' input word = {a}, find {b} synonyms...'.format(a=key_word,b=len(synonym_list)))
        return synonym_list

    except Exception:
        logger.error(' input word = {a}, occur an error!'.format(a=key_word))
        traceback.print_exc()
    time.sleep(0.1)





if __name__ == '__main__':
    print(kmcha_search(('程序员', 'cs11.33')))