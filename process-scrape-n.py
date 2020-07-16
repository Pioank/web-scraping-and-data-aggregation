import re
import os
import glob
import numpy as np
import pyodbc 
import pandas as pd
from pandas import DataFrame
import pandas.io.sql as psql
import sqlalchemy as sa
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # Ignore error messages when running the code

os.chdir(r"\scroutcome") # Browse to the folder where all CSVs from scraping are located
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))] #Get all CSVs in a list
combined_csv = pd.concat([pd.read_csv(f, encoding='latin1',error_bad_lines=False) for f in all_filenames],sort=False) # With pandas concatenate all CSVs in one DF - all CSV columns have the same Headers already

combined_csv['key']=(combined_csv['url'].str.lower()+combined_csv['date']) # Create a unique key to filter out duplicates
combined_csv.drop_duplicates(subset ="key", keep = 'first', inplace = True) # Drop duplicates based on the key
combined_csv['all']=(combined_csv['title'].str.lower() + combined_csv['s-description'].str.lower() + combined_csv['url'].str.lower()) # Creating a key to use for unique values - promotions only - for visualisation purposes - Power BI

# Lengthy piece of code that looks up values in All field to identify the product this promotion is about
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


cnxn = pyodbc.connect("") # Here insert your SQL connection
cur = cnxn.cursor()

# Try create the table in the SQL server - if exists then skip
try:
    sql="""tablename (company varchar(30) NOT NULL, date varchar(100) NOT NULL, title varchar(100), [s-description] varchar(900), url varchar(900) NOT NULL, [key] varchar(1000) NOT NULL, [all] varchar(1000), product varchar(30) NOT NULL)"""
    cur.execute(sql)
except:
    print('table exists')

cur.commit()
cur.close()

engine = sa.create_engine("") # Here insert you SQL connection
combined_csv.to_sql('tablename', engine, if_exists='append', index = False) # Append data to the SQL table

