import math
import sys
import time

import metapy
import pytoml
import count as cnt
import extract  as ext

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)


    cfg = sys.argv[1]
    print('Building or loading index...')

    # Read the config file
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    extract = ext.Extract(cfg_d)
    extract.extract_abstracts()
   
    count = cnt.Count(cfg_d)
    unigrams = count.analyze()

    tokens, counts = [], []

    # unigrams.items returns token and count of each token
    for token, count in unigrams.items():
        counts.append(count)
        tokens.append(token)

    #printing tokens
    print (tokens)
    #printing counts
    print (counts)
    # print unigrams
    print (unigrams.items())
    

