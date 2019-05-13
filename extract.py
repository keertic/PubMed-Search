import math
import sys
import time

import metapy
import pytoml
import count as cnt
import scraper  as sc
import pandas as pd


class Extract:

    def __init__(self, config_d, cycleFlag):
       self.config_d = config_d
       self.cycleFlag = cycleFlag

    #function for extracting list of url uid and outputting abstract text file with new line
    #usage extractUrlAndOutputAbstract('pubmed_result.txt','abstract.txt')

    def extract_abstracts (self,query_term,tf_term, no_of_docs):
        base_url = self.config_d['base-url']
        pubmed_url = self.config_d['pubmed-url']
        page_limit=max(int(no_of_docs/20),1)

        extract_file =  self.config_d['extract-file']
        query_term = query_term.replace(' ', '+')

        scraper = sc.Scraper(base_url)
        #ncbi_url = pubmed_url+ query_term + '&ncbi_sortorder=relavance'
        ncbi_url = pubmed_url+ query_term

        print (ncbi_url)
        print (page_limit)

        article_links, article_map = scraper.scrape_ncbi_articles(ncbi_url, page_limit)
        article_abstracts = {}
        article_words={}
        count = cnt.Count(self.config_d, self.cycleFlag)
        link_l = []
        abstract_l = []
        term_l = []
        frequency_l = []

        all_abstracts_text=''
        dict_link_abstract= {}

        for link in article_links:
            abstract=scraper.scrape_study_page(link)
            if not abstract:
                continue
            article_abstracts[link]=  abstract
            unigrams = count.analyze(abstract)
            term_unigrams = count.analyze(tf_term)
            term_count = 0;
            for term in term_unigrams:
                if term in unigrams:
                    term_count += unigrams[term]
            print (len(unigrams))
            print (term_count)
            article_words [link] = len(unigrams)
            link_l.append(link)
            abstract_l.append(abstract)
            all_abstracts_text = all_abstracts_text + ' ' + abstract
            term_l.append(len(unigrams))
            frequency_l.append(term_count)
            dict_link_abstract[link] = abstract
        dict = {}
        dict['links'] = link_l
        #dict['abstracts'] = abstract_l
        dict['terms'] =  term_l
        dict['frequency'] =  frequency_l
        # Use a dictionary of dictionaries to store the data so the grpahs can be plotted from the data
        # scatter contains data frame required for scatter plot
        dict_of_dict= {}
        dict_of_dict['scatter'] = dict
        # top_words consists of a dictionary of words to frequency
        dict_of_dict['top_words'] = self.get_word_frequency(all_abstracts_text)

        # link_abstract_map is a dictionary of links to abstract. When the link is clicked on the scatter plot 
        # this map is used to get the corresponding abstract
        dict_of_dict['link_abstract_map'] = dict_link_abstract

        df = pd.DataFrame(dict_of_dict)
        
        return df

    def get_word_frequency (self, abstracts): 
        count = cnt.Count(self.config_d, self.cycleFlag)
        unigrams = count.analyze(abstracts)
        listofTuples = sorted(unigrams.items() ,  reverse=True, key=lambda x: x[1])
 
        # Iterate over the sorted sequence
        top_words_dict = {}  

        index=0;
        word_l = []
        freq_l = []
        index_l = []
        for elem in listofTuples: 
            if (index > 99) :
                break
            index += 1
            index_l.append(index)
            word_l.append(elem[0])
            freq_l.append(elem[1])
            print(elem[0] , " ::" , elem[1] )
        dict = {}
        dict['words'] = word_l
        dict['freq'] = freq_l
        dict['index'] = index_l
        print (dict)
        return dict

#with open('config.toml', 'r') as fin:
#    cfg_d = pytoml.load(fin)
#extract = Extract(cfg_d)
#df = extract.extract_abstracts('antibiotic resistance', 20)

#print (df)
