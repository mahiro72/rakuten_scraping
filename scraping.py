import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd
from dotenv import load_dotenv
import datetime
import time
import random

load_dotenv()

# browser start
option = Options()
option.add_argument('--headless')
executable_path = os.environ.get('DRIVER_PATH')
driver = webdriver.Chrome(executable_path=executable_path,options=option)


col_name = ["総合評価","投稿日時","投稿本文","目的","同伴者","回答本文","施設ID"]
test_csv = pd.DataFrame(columns=col_name)

check_date = datetime.datetime(year=2019,month=12,day=1)

def wait(sel):
    WebDriverWait(driver,3).until(
    expected_conditions.presence_of_element_located((By.CSS_SELECTOR,sel)))


def check(sel):
    bool = False
    try:
        wait(sel)
        bool=True
    except:
        pass
    return bool


def date_shaping(text):
    date,_ = text.split()
    year,month,day = int(date[0:4]),int(date[5:7]),int(date[8:10])
    dt = datetime.datetime(year=year,month=month,day=day)
    return dt



def scraping_start(p,num):
    global test_csv
    time.sleep(2)

    ne = True
    driver.get(p)


    if not check('#RthNameArea > h2 > a'):
        return
    
    if driver.find_element_by_css_selector('#htlBrdCrmbs > a:nth-child(1)').text=="海外旅行":
        return
    

    cnt = len(driver.find_elements_by_css_selector('#commentArea > div'))
    dict = {}

    dict["施設ID"] = num

    for i in range(1,cnt+1):
        try:
            date  =driver.find_element_by_css_selector('#commentArea > div:nth-child('+str(i)+') > div.commentReputationBoth > dl.commentReputation > dt > span.time').text
            date = date_shaping(date)
            if check_date>date:
                ne = False
                continue

            dict["投稿日時"] = date

            dict["投稿本文"] = driver.find_element_by_css_selector('#commentArea > div:nth-child('+str(i)+') > div.commentReputationBoth > dl.commentReputation > dd > p').text
            dict["総合評価"] = driver.find_element_by_css_selector('#commentArea > div:nth-child('+str(i)+') > p > span').text
            
            dict["目的"] = driver.find_element_by_css_selector('#commentArea > div:nth-child('+str(i)+') > div.commentReputationBoth > dl.commentReputation > dd > dl > dd:nth-child(2)').text
            dict["同伴者"] = driver.find_element_by_css_selector('#commentArea > div:nth-child('+str(i)+') > div.commentReputationBoth > dl.commentReputation > dd > dl > dd:nth-child(4)').text
            dict["回答本文"] = driver.find_element_by_css_selector('#commentArea > div:nth-child('+str(i)+') > div.commentReputationBoth > dl.commentHotel > dd > p').text
            
            test_csv = test_csv.append(dict,ignore_index=True)

        except:
            ne=False
            pass
    
    if ne and check('#primary > div:nth-child(5) > ul > li.pagingNext > a'):
        url = driver.find_element_by_css_selector('#primary > div:nth-child(5) > ul > li.pagingNext > a').get_attribute("href")
        scraping_start(url,num)

    return 




data = pd.read_table(r"C:\Users\mahir\デスクトップ\ジョイリデータ\data\travel_20200131\02_Travel_HotelMaster.tsv\02_Travel_HotelMaster.tsv")
id_list = set()
while len(id_list)<10000:
    id_list.add(random.choice(data["施設ID"].unique()))


for i,num in enumerate(list(id_list)): 
    print('%d 番目(id: %d)' % (i+1,num))
    url = 'https://review.travel.rakuten.co.jp/hotel/voice/'+str(num)
    
    try:
        scraping_start(url,num)
    except:
        print('%d 番目(id: %d) エラーが発生しました。' % (i+1,num))
        pass
    

driver.quit()

test_csv.to_csv("test_csv.csv",index=False)



