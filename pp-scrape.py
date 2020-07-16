
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

driver = webdriver.Chrome(ChromeDriverManager().install()) # Installs the latest version of Chrome Driver
driver.get('https://promos.paddypower.com/sport')
myurl = 'https://promos.paddypower.com/sport'
uClient = req(myurl)
page_html = uClient.read()
uClient.close()
pagebs = bs(page_html,'html.parser')

driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/main/div/div/button"))
time.sleep(3)
try:
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/main/div/div/div/div/button"))
    time.sleep(3)
except:
    print('no second button')

# Create CSV file to save the data
filename='results/scroutcome/paddypower.csv'
f=open(filename,'w')
headers='company,date,title,s-description,url\n'
f.write(headers)

# Find elements that you would like to get data from
promotions = driver.find_elements_by_class_name("promo-games")
promotions.extend(driver.find_elements_by_class_name("promo-sportsbook"))
promotions.extend(driver.find_elements_by_class_name("promo-vegas"))
promotions.extend(driver.find_elements_by_class_name("promo-refer_and_earn"))

promocodet=list()

for promotion in promotions:
    promocode = promotion.get_attribute('data-qa')
    promocodet.append(promocode)

today = date.today()
d1 = today.strftime("%d/%m/%Y")
print(len(promocodet))

for i in promocodet:
    pnum = str(i)
    url = 'https://promos.paddypower.com/promotion?promoCode='+i
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    print(url)

    value = soup.find('h1', {'class': ['promo-name pp-sportsbook','promo-name pp-games','promo-name pp-refer_and_earn','promo-name pp-vegas']}).text.strip()
    value = value.replace(',','')

    value2 = soup.find('div', {'class': ['description']}).text.strip()
    value2 = str(value2.splitlines())
    value2 = value2.replace(',','')
    value2 = value2.replace('[','')
    value2 = value2.replace(']','')

    f.write('PaddyPower' + ',' + d1 + ',' + value  + ',' + value2 + ',' + url + '\n') # Save data points collected in a CSV

driver.quit()
