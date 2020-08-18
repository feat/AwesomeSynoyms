from __future__ import print_function
from __future__ import division

import os
import sys
from absl import flags
from absl import logging

import synonyms
import json

from flask import Flask

import find as f

app = Flask(__name__)


@app.route('/<word>')
def find(word):
    if len(word.strip()) == 0:
        return ""
    else: 
        result = f.findSynonyms(word)
        return word + " %s" % (result,)



if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)