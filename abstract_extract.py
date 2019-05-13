from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib

#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

#remove tags in the text when getting text
def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup

#function for extracting abstract from links pages
def scrape_study_page(fac_url,browser):
    print('scrapping:'+fac_url)
    soup = get_js_soup(fac_url,browser)
    abstract = ''
    for item in soup.find_all('div', class_='abstr'):
        abstractText = remove_script(item.find('p')).get_text()
        return abstractText

#helper function for extracting txt file filled with uid
def extract_txt_file(filename):
    print('reading txt file:'+filename)
    with open(filename) as f:
            lines = f.readlines()
    print('number of links:'+str(len(lines)))
    completeLinks=[]


    with open('pubmed_result.txt') as myfile:
        head = [next(myfile) for x in range(10)]
    print(head)
    write_lst(head,'top10.txt')



    for links in lines:
        strippedLinks=links.strip()
        

        completeLinks.append('https://www.ncbi.nlm.nih.gov/pubmed/'+head)
    return completeLinks

#function for outputting one textfile for all abstracts extracted from the link
def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')
            
#function for extracting list of url uid and outputting abstract text file with new line
#usage extractUrlAndOutputAbstract('pubmed_result.txt','abstract.txt')
def extractUrlAndOutputAbstract(inputFileName, outputFileName):
    completeLinks=extract_txt_file('pubmed_result.txt')


  
    allAbstractTxt=[]
    for url in completeLinks:
        allAbstractTxt.append(scrape_study_page(url, browser))
    write_lst(allAbstractTxt,'abstract.txt')    


#create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
browser = webdriver.Chrome('chromedriver',options=options)

    



extractUrlAndOutputAbstract('top10.txt','abstract.txt')
