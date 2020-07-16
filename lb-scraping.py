from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as req
import re
import time
from itertools import *
import unicodecsv as csv
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://sports.ladbrokes.com/promotions/all');

#myurl = 'https://sports.ladbrokes.com/promotions/all'
#uClient = req(myurl)
#page_html = uClient.read()
#uClient.close()
#pagebs = bs(page_html,'html.parser')

time.sleep(2)

urls=list()
ldescription5=list()
ldescription=list()
titlel=list()
sdescriptionl=list()
i=0
x=0


promotions = driver.find_elements_by_class_name("promotion-item")
print(len(promotions))

for promotion in promotions:
    title=promotion.find_element_by_tag_name('h3').text
    titlel.append(title)
    sdescription=promotion.find_element_by_tag_name("p").text
    sdescription = sdescription.replace(',','')
    sdescriptionl.append(sdescription)
    url2=promotion.find_element_by_tag_name('a')
    url=url2.get_attribute('href')
    urls.append(url)
    print(url)


for u in urls:
    urlclick = u
    driver.get(urlclick)
    time.sleep(2)
    ldescription1 = bs(driver.page_source,'html.parser')
    ldescription2 = ldescription1.find('div', {'class': ['short-description']})
    try:
        ldescription3 = ldescription2.find_all('p')
    except:
        ldescription3 = ldescription1.find('div', {'class': ['header-panel']}) 
    ldescription5=list()

    try:
        for line in ldescription3:
            ldescription4 = line.text.strip()
            ldescritpion4 = str(ldescription4)
            ldescription4 = ldescription4.replace(',','')
            ldescription5.append(ldescription4)
    except:
        ldescription5=str(ldescription3)
        
    ldescription6=''.join(ldescription5)
    ldescription.append(ldescription6)


today = date.today()
d1 = today.strftime("%d/%m/%Y")

run=len(urls)

filename='results/scroutcome/ladbrokes.csv'
f=open(filename,'w')

headers='company,date,title,s-description,url\n'
#headers='company,code,title,description,url\n'
f.write(headers)

while i < run:
    f.write('Ladbrokes' + ',' + d1 + ',' + titlel[i] + ',' + sdescriptionl[i] + ',' + urls[i] + '\n')
    #f.write('Ladbrokes' + ',' + v1[i] + ',' + v2[i] + ',' + v3[i] + '\n')
    i=i+1


driver.quit()
