from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import urllib
import urllib.request
from urllib.parse import urlparse

#options = Options()
#options.headless = True
#browser = webdriver.Chrome('chromedriver', options=options)



class Scraper:
    def __init__(self, base_url):
       options = Options()
       options.headless = True
       self.browser = webdriver.Chrome('chromedriver', options=options)
       self.base_url = base_url

    def get_js_soup(self, url):
       self.browser.get(url)
       res_html = self.browser.execute_script('return document.body.innerHTML')
       soup = BeautifulSoup(res_html, 'html.parser')
       return soup
    def remove_script(self, soup):
       for script in soup(["script", "style"]):
           script.decompose()
       return soup

    def is_absolute(self, url):
       return bool(urlparse(url).netloc)

    def scrape_ncbi_articles(self, ncbi_url, sz):
       article_links = []
       article_map = {}

       self.browser.get(ncbi_url)
       index=0;
       while (True and index < sz) :
           index += 1
           print ('-'*20,'Scraping directory page','-'*20)
           soup = BeautifulSoup(self.browser.page_source, 'html.parser')
           for rprt in soup.find_all('div', class_='rprt'):
               for link_holder in rprt.find_all('div', class_='rslt'):
                   if link_holder is not None and link_holder.find('a') is not None:
                       rel_link = link_holder.find('a')['href'] #get url
                       a_link = link_holder.find('a')   # get anchor
                       title = link_holder.find('a').text   # get anchor
                       article_map[rel_link] = title
                       #url returned is relative, so we need to add base url
                       if not bool(urlparse(rel_link).netloc):
                           rel_link = self.base_url+rel_link
                       article_links.append(rel_link)
                       print(rel_link)
               # Get next link
               try:
                   next_link=self.browser.find_element_by_partial_link_text('Next')
                   if [next_link != 'None']:
                       next_link.click()
                   else:
    	               break
               except:
                   break
        
       return article_links, article_map

    #function for extracting abstract from links pages
    def scrape_study_page(self, article_link):
        soup = self.get_js_soup(article_link)
        for item in soup.find_all('div', class_='abstr'):
            abstractText = self.remove_script(item.find('p')).get_text()
            return abstractText



#scraper = Scraper('https://www.ncbi.nlm.nih.gov')

#ncbi_url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=antibiotic+resistance' #url of directory listings of articles relating to antibiotic resistance
#article_links, article_map = scraper.scrape_ncbi_articles(ncbi_url, 2)

#print (article_links)
#print (article_map)

#print (article_links)
#for link in article_links:
#    abstract=scraper.scrape_study_page(link)
#    print (abstract)
    





