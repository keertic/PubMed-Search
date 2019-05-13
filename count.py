import math
import sys
import time

import metapy
import pytoml
from operator import itemgetter, attrgetter



class Count:
   def __init__(self, cfg_d, cycleFlag):
       self.cfg_d = cfg_d
       self.cycleFlag = cycleFlag


   def analyze(self, content):
       if content is None:
           content = ""

       # construct a metapy doc
       doc = metapy.index.Document()
       doc.content(content)

       # tokenizers. Use ICUTokenizer
       tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)


       #Removes short words. lower cases it
       #lowercases, removes words with less than 2 and more than 25  characters
       tok = metapy.analyzers.LengthFilter (tok, min=2,max=25)
       tok = metapy.analyzers.LowercaseFilter(tok)

       # Filter stop words using the stopwords.txt
       if self.cycleFlag:
           stop_words_file=self.cfg_d['user-stop-words']
           tok = metapy.analyzers.ListFilter(tok, stop_words_file, metapy.analyzers.ListFilter.Type.Reject)
       else:
           stop_words_file=self.cfg_d['default-stop-words']
           tok = metapy.analyzers.ListFilter(tok, stop_words_file, metapy.analyzers.ListFilter.Type.Reject)

       #performs stemming.
       tok = metapy.analyzers.Porter2Filter(tok)

       ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
       unigrams = ana.analyze(doc)

       return unigrams

