
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as req
import re
import time
import unicodecsv as csv
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install()) #Gets the latest Chrome Driver
driver.get('https://extra.bet365.com/promotions/special-offers')
myurl = 'https://extra.bet365.com/promotions/special-offers'

uClient = req(myurl)
page_html = uClient.read()
uClient.close()
pagebs = bs(page_html,'html.parser')

#Build lists to store each parameter scraped
items=list()
urls = list()
titlel = list()
descvl = list()
ldescvl = list()

navigation =driver.find_element_by_xpath('//*[@id="promotion-icons-owl-carousel"]/div')
navigationn =navigation.find_elements_by_tag_name("a")
for el in navigationn:
    item=el.get_attribute("href")
    if item != '':
        items.append(item)

time.sleep(1)

#Create a CSV file locally where you will save the results
filename='results/scroutcome/bet365.csv'
f=open(filename,'w')
headers='company,date,title,s-description,url\n'
f.write(headers)

#Loop through the elements you are interested and get the data you need
for x in items:
    urla = str(x)
    driver.get(urla);
    promotions = driver.find_elements_by_class_name("pod_wrapper")

    for promotion in promotions:
        title = promotion.find_element_by_class_name("promotion-pod-title")
        titlev=title.text
        titlev = titlev.replace(',','')
        titlel.append(titlev)
        desc = promotion.find_element_by_tag_name("p")
        descv=desc.text
        descv = descv.replace(',','')
        descvl.append(descv)

        try:
            ldesc = promotion.find_element_by_class_name('infoTextContainer.podTermsAndConditions')
            ldescv=ldesc.text
            ldescv = ldescv.replace(',','')
        except:
            ldesc = promotion.find_element_by_tag_name("p")
            ldescv=ldesc.text
            ldescv = ldescv.replace(',','')
        if ldescv not in ldescvl:
            ldescvl.append(ldescv)

    links = driver.find_element_by_class_name("promotions-pod-container.container")
    linkss =links.find_elements_by_tag_name("a")
    for link in linkss:
        onel = link.get_attribute("href")
        if onel != '':
                onel = str(onel)
                urls.append(onel)
                print(onel)

i=0
run=len(titlel)

today = date.today()
d1 = today.strftime("%d/%m/%Y")

#Save data scraped in the CSV)
while i < run:
    f.write('Bet365'+ ',' + d1 + ',' + titlel[i] + ',' + descvl[i] + ',' + urls[i] + '\n')
    i=i+1

driver.quit()
