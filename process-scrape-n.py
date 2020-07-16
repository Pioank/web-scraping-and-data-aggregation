
import re
import time
import os
import glob
import numpy as np
from datetime import date
import pyodbc 
import pandas as pd
from pandas import DataFrame
import pandas.io.sql as psql
import sqlalchemy as sa
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

os.chdir(r"\Users\pkatidis\Desktop\pythonf\Scraping\results\scroutcome")

extension = 'csv'

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


combined_csv = pd.concat([pd.read_csv(f, encoding='latin1',error_bad_lines=False) for f in all_filenames],sort=False)


combined_csv['key']=(combined_csv['url'].str.lower()+combined_csv['date'])

combined_csv.drop_duplicates(subset ="key", keep = 'first', inplace = True)

combined_csv['all']=(combined_csv['title'].str.lower() + combined_csv['s-description'].str.lower() + combined_csv['url'].str.lower())


combined_csv['Product'] = pd.np.where(combined_csv['all'].str.contains('nfl|nfl football'), 'NFL',
                                pd.np.where(combined_csv['all'].str.contains('dart'),'Darts',
                                pd.np.where(combined_csv['all'].str.contains('fantasy'),'Fantasy Football',
                                pd.np.where(combined_csv['all'].str.contains('goal|soccer|goals|goalscorer|europa league|champions league|premier league|man city|liverpool|arsenal|la liga|football|epl'),'Football',
                                pd.np.where(combined_csv['all'].str.contains('tennis|wimbledon|french open|australian open|us open|atp|wta'), 'Tennis',
                                pd.np.where(combined_csv['all'].str.contains('nrl|rugby|six nations|super league'), 'Rugby',
                                pd.np.where(combined_csv['all'].str.contains('boxing|rign|anthony joshua|aj'), 'Boxing',
                                pd.np.where(combined_csv['all'].str.contains('golf|dp world tour|pga|us open golf|masters tournament|alfred dunhill championship'), 'Golf',
                                pd.np.where(combined_csv['all'].str.contains('basketball|nba'), 'Basketball',
                                pd.np.where(combined_csv['all'].str.contains('snooker'), 'Snooker',
                                pd.np.where(combined_csv['all'].str.contains('cricket'), 'Cricket',
                                pd.np.where(combined_csv['all'].str.contains('greyhound|greyhounds'), 'Greyhounds',
                                pd.np.where(combined_csv['all'].str.contains('horse|each way|extra place|cheltenham|grand national|racing|horses|race|ascot|royal ascot'), 'Horseracing',
                                pd.np.where(combined_csv['all'].str.contains('lotto'), 'Lotto',
                                pd.np.where(combined_csv['all'].str.contains('jackpot|spins|free spins|vegas|bingo|spin|casino|roulette|slot|bonus drop|blackjack|scratch'), 'Gaming',
                                pd.np.where(combined_csv['all'].str.contains('open account|deposit'), 'New customer offer',
                                pd.np.where(combined_csv['all'].str.contains('responsible gambling'), 'Responsible gambling',
                                pd.np.where(combined_csv['all'].str.contains('bet|sportsbook|sport'), 'Sports-other','Unknown',
                                ))))))))))))))))))

os.chdir(r"\Users\pkatidis\Desktop\pythonf\Scraping\results")
combined_csv.to_csv("test_csv.csv", index=False, encoding='utf-8-sig')

cnxn = pyodbc.connect("Driver={SQL Server};Server=SC1WNPRNDB003\\DPE_PROD;Database=DMSandbox;uid=WHGROUP\pkatidis;Trusted_Connection=yes;autocommit=False")
cur = cnxn.cursor()

try:
    sql="""CREATE TABLE COMPOFFERS (company varchar(30) NOT NULL, date varchar(100) NOT NULL, title varchar(100), [s-description] varchar(900), url varchar(900) NOT NULL, [key] varchar(1000) NOT NULL, [all] varchar(1000), product varchar(30) NOT NULL)"""
    cur.execute(sql)
except:
    print('table exists')

cur.commit()
cur.close()

engine = sa.create_engine('mssql+pyodbc://SC1WNPRNDB003\\DPE_PROD/DMSandbox?driver=SQL+Server+Native+Client+11.0')

combined_csv.to_sql('COMPOFFERS', engine, if_exists='append', index = False)


'''
def f(row):
    if row['all'].str.contains('nfl|nfl football')==True:
        val = 'NFL'
    elif row['all'].str.contains('dart')==True:
        val = 'Darts'
    elif row['all'].str.contains('fantasy')==True:
        val = 'Fantasy Football'
    elif row['all'].str.contains('goal|soccer|goals|goalscorer|europa league|champions league|premier league|man city|liverpool|arsenal|la liga|football|epl')==True:
        val = 'Football'
    elif row['all'].str.contains('tennis|wimbledon|french open|australian open|us open|atp|wta')==True:
        val = 'Tennis'
    elif row['all'].str.contains('nrl|rugby|six nations|super league')==True:
        val = 'Rugby'
    elif row['all'].str.contains('boxing|rign|anthony joshua|aj')==True:
        val = 'Boxing'
    elif row['all'].str.contains('golf|dp world tour|pga|us open golf|masters tournament|alfred dunhill championship')==True:
        val = 'Golf'
    elif row['all'].str.contains('basketball|nba')==True:
        val = 'Basketball'
    elif row['all'].str.contains('snooker')==True:
        val = 'Snooker'
    elif row['all'].str.contains('cricket')==True:
        val = 'Cricket'
    elif row['all'].str.contains('greyhound|greyhounds')==True:
        val = 'Geryhounds'
    elif row['all'].str.contains('horse|each way|extra place|cheltenham|grand national|racing|horses|race')==True:
        val = 'Horseracing'
    elif row['all'].str.contains('lotto')==True:
        val = 'Lotto'
    elif row['all'].str.contains('jackpot|spins|free spins|vegas|bingo|spin|casino|roulette|slot|bonus drop|blackjack|scratch')==True:
        val = 'Gaming'
    elif row['all'].str.contains('open account|deposit')==True:
        val = 'New customer offer'
    elif row['all'].str.contains('bet|sportsbook|sport')==True:
        val = 'Sports-other'
    else:
        val = 'Unknown'
    return val


combined_csv['Product'] = combined_csv.apply(f, axis=1)
'''