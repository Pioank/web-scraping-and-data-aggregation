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
driver.get('https://m.skybet.com/promotions');

time.sleep(2)

x=0

filename='results/scroutcome/skybet.csv'
f=open(filename,'w')
headers='company,date,title,s-description,url\n'
f.write(headers)

v1=list()
v2=list()
v3=list()

while x < 5:
    z=0
    promotions = driver.find_elements_by_class_name("hero__copy__head")
    promodesc = driver.find_elements_by_class_name("hero__copy__sub")

    try:
        url=driver.find_element_by_xpath('//*[@id="react-promotions-page"]/div/div[3]/div[1]/div/div/div[3]/div/a')
        b=url.get_attribute("href")
        v3.append(b)
        url1=driver.find_element_by_xpath('//*[@id="react-promotions-page"]/div/div[3]/div[1]/div/div/div[4]/div/a')
        c=url1.get_attribute("href")
        v3.append(c)
        url2=driver.find_element_by_xpath('//*[@id="react-promotions-page"]/div/div[3]/div[1]/div/div/div[5]/div/a')
        v=url2.get_attribute("href")
        v3.append(v)
        print(v)
    except:
        url=driver.find_element_by_xpath('//*[@id="react-promotions-page"]/div/div[2]/div[1]/div/div/div[3]/div/a')
        b=url.get_attribute("href")
        v3.append(b)
        url1=driver.find_element_by_xpath('//*[@id="react-promotions-page"]/div/div[2]/div[1]/div/div/div[4]/div/a')
        c=url1.get_attribute("href")
        v3.append(c)
        url2=driver.find_element_by_xpath('//*[@id="react-promotions-page"]/div/div[2]/div[1]/div/div/div[5]/div/a')
        v=url2.get_attribute("href")
        v3.append(v)
        print(v)


    for i, j in zip(promotions,promodesc):

        v1b = str(i.text)
        v1b = v1b.replace(',','')
        v2b = str(j.text)
        v2b = v2b.replace(',','')

        if v1b != '':
            if v1b in v1:
                break
                x=5
                z=5
            else:
                v1.append(v1b)
                v2.append(v2b)

    while z < 3:
        button = driver.find_element_by_class_name("panels-next").click()
        time.sleep(0.5)
        z=z+1

    x=x+1

i=0
run=len(v1)

today = date.today()
d1 = today.strftime("%d/%m/%Y")

while i < run:
    f.write('Skybet' + ',' + d1 + ',' + v1[i] + ',' + v2[i] + ',' + v3[i] + '\n')
    #f.write('Skybet' + ',' + v1[i] + ',' + v2[i] + ',' + v3[i] + '\n')
    i=i+1


driver.quit()
