import math
import sys
import time

import metapy
import pytoml



class Count: 
   def __init__(self, cfg_d):
       self.cfg_d = cfg_d



   def analyze(self, content):

       # construct a metapy doc
       doc = metapy.index.Document()
       doc.content(content)
   
       # tokenizers. Use ICUTokenizer
       tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)

       # Filter stop words using the stopwords.txt
       stop_words_file=self.cfg_d['stop-words']
       tok = metapy.analyzers.ListFilter(tok, stop_words_file, metapy.analyzers.ListFilter.Type.Reject)


       #Removes short words. lower cases it
       #lowercases, removes words with less than 2 and more than 25  characters
       tok = metapy.analyzers.LengthFilter (tok, min=2,max=25)
       tok = metapy.analyzers.LowercaseFilter(tok)

       #performs stemming. 
       tok = metapy.analyzers.Porter2Filter(tok)

       ana = metapy.analyzers.NGramWordAnalyzer(1, tok)  
       unigrams = ana.analyze(doc)
    
       return unigrams

#with open('config.toml', 'r') as fin:
#    cfg_d = pytoml.load(fin)
#count = Count(cfg_d)
#unigrams=count.analyze("the quick brown fox jumped over the fence")

#print (unigrams)
#print (len(unigrams))
