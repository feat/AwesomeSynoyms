
from __future__ import print_function
from __future__ import division

import os
import sys
from absl import flags
from absl import logging

# import synonyms
import json

# sen1 = "程序员"
# sen2 = "软件工程师"
# r = synonyms.compare(sen1, sen2, seg=True)
# print(r)

# ddp = DDParser()
# # 单条句子
# re = ddp.parse("语文老师")
# print(re)

from ltp import LTP
ltp = LTP() # 默认加载 Small 模型
seg, hidden = ltp.seg(["语文老师"])
pos = ltp.pos(hidden)
ner = ltp.ner(hidden)
srl = ltp.srl(hidden)
dep = ltp.dep(hidden)
sdp = ltp.sdp(hidden)

print(seg)
# print(hidden)
print(pos)
print(pos)
print(ner)
print(srl)
print(dep)
