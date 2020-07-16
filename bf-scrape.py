
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as req
import re
import time
import unicodecsv as csv
from datetime import date
today = date.today()
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://promos.betfair.com/sport')

myurl = 'https://promos.betfair.com/sport'

uClient = req(myurl)
page_html = uClient.read()
uClient.close()
pagebs = bs(page_html,'html.parser')


try:
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/main/div/div/button"))
    time.sleep(3)
except:
    pass

promotions = driver.find_elements_by_class_name("promo-refer_and_earn")
promotions.extend(driver.find_elements_by_class_name("promo-exchange"))
promotions.extend(driver.find_elements_by_class_name("promo-sportsbook"))
promotions.extend(driver.find_elements_by_class_name("promo-arcade"))

promocodet=list()

for promotion in promotions:
    promocode = promotion.get_attribute('data-qa')
    promocodet.append(promocode)


filename='results/scroutcome/betfair.csv'
f=open(filename,'w')
headers='company,date,title,s-description,url\n'
#headers='company,code,title,description,url\n'
f.write(headers)
d1 = today.strftime("%d/%m/%Y")

print(len(promocodet))

for i in promocodet:
    pnum = str(i)
    url = 'https://promos.betfair.com/promotion?promoCode='+i
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')

    value = soup.find('h1', {'class': ['promo-name bf-refer_and_earn','promo-name bf-arcade','promo-name bf-sportsbook','promo-name bf-exchange']}).text.strip()
    value = value.replace(',','')

    value2 = soup.find('div', {'class': ['description']}).text.strip()
    value2 = str(value2.splitlines())
    value2 = value2.replace(',','')
    value2 = value2.replace('[','')
    value2 = value2.replace(']','')

    print(url)

    #f.write('BetFair' + ',' + i + ',' + value  + ',' + value2 + ',' + url + '\n')
    f.write('BetFair' + ',' + d1 + ',' + value  + ',' + value2 + ',' + url + '\n')


driver.quit()
