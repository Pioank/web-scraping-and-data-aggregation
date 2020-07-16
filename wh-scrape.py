from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlopen as req
import re
import time
from itertools import *
import unicodecsv as csv
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome()
driver.get('https://promotions.williamhill.com/');


time.sleep(2)

urls=list()
ldescription5=list()
ldescription=list()
titlel=list()
sdescriptionl=list()
i=0
x=0


promotions = driver.find_elements_by_class_name("wf-splash-grid__tile")

for promotion in promotions:
    title2=promotion.find_element_by_tag_name('h2')
    title=title2.text
    title = str(title)
    title = title.replace(',','')
    titlel.append(title)
    sdescription=promotion.find_element_by_class_name('wf-splash-grid__product-terms.ng-binding.ng-scope')
    sdescription=sdescription.text
    sdescription = str(sdescription)
    sdescription = sdescription.replace(',','')
    sdescriptionl.append(sdescription)


promotions = driver.find_elements_by_class_name("wf-splash-grid__single-link")
x=len(promotions)
print(x)

for promotion in promotions:
    url=promotion.get_attribute('href')
    urls.append(url)
    print(url)


today = date.today()
d1 = today.strftime("%d/%m/%Y")

run=len(urls)

filename='results/scroutcome/williamhill.csv'
f=open(filename,'w')

headers='company,date,title,s-description,url\n'
#headers='company,code,title,description,url\n'
f.write(headers)

while i < run:
    f.write('WilliamHill' + ',' + d1 + ',' + titlel[i] + ',' + sdescriptionl[i] + ',' + urls[i] + '\n')
    #f.write('WilliamHill' + ',' + v1[i] + ',' + v2[i] + ',' + v3[i] + '\n')
    i=i+1


driver.quit()
