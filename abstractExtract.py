from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib

#create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
browser = webdriver.Chrome('./chromedriver',options=options)

#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


#function for extracting abstract from links pages
def scrape_study_page(fac_url,browser):
    print(fac_url)
    soup = get_js_soup(fac_url,browser)
    abstract = ''
    for item in soup.find_all('div', class_='abstr'):
        abstractText = remove_script(item.find('p')).get_text()
        print(abstractText)
        return abstractText

studyUrlList=['https://www.ncbi.nlm.nih.gov/pubmed/30917300','https://www.ncbi.nlm.nih.gov/pubmed/30917276','https://www.ncbi.nlm.nih.gov/pubmed/30917255']
for url in studyUrlList:
    scrape_study_page(url, browser)
