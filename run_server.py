from __future__ import print_function
from __future__ import division

import os
import sys
from absl import flags
from absl import logging

import json

from flask import Flask
import waitress

import find_mengren
from find_service import feat_search

app = Flask(__name__)


@app.route('/mengren/<word>')
def mengren(word):
    if len(word.strip()) == 0 or word == 'favicon.ico':
        return ""
    else:
        result = find_mengren.find_synonyms(word)
        return word + " %s" % (result,)


@app.route('/service/<word>')
def service(word):
    if len(word.strip()) == 0 or word == 'favicon.ico':
        return ""
    else:
        result = feat_search.search(word)
        return word + " %s" % (result,)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
