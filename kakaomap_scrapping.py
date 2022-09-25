
# - Scrapping information on places
# - Scrapping results from a given query(e.g. "스타벅스").
# - Information including name, address, and working time
# - Data from Kakao map


import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import Keys

import time
import re

driver = webdriver.Chrome(r'C:\Users\usju\Downloads\chromedriver_win32\chromedriver.exe')
driver.get(r'https://map.kakao.com/')
driver.find_element('xpath', '//*[@id="dimmedLayer"]').click()

region = np.array(['강원','세종','경기','경남','대구','광주','대전','부산','울산','인천','전북','제주','충북','경북','서울','전남','충남'])
region_list = []
name_addr_dic = {}

for reg in region:
    temp = []
    q = reg + ' ' + '투썸플레이스'
    driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(q)
    driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(Keys.ENTER)
    time.sleep(1.5)

    try:
        ac = ActionChains(driver)
        dobogi = driver.find_element('xpath', '//*[@id="info.search.place.more"]')
        ac.move_to_element(dobogi)
        driver.find_element('xpath', '//*[@id="info.search.place.more"]').click()
        time.sleep(1.5)
    except:
        pass

    try:
        while True:
            for i in range(1, 6):
                driver.find_element('xpath', '//*[@id="info.search.page.no{}"]'.format(i)).click()
                time.sleep(1.5)
                name_list = driver.find_elements('xpath', '//*[@id="info.search.place.list"]/li/div[3]/strong/a[2]')
                addr_list = driver.find_elements('xpath', '//*[@id="info.search.place.list"]/li/div[5]/div[2]/p[1]')
                for n, a in zip(name_list, addr_list):
                    name_addr_dic[n.text] = a.text
                    temp.append(n)

            next_button = driver.find_element('xpath', '//*[@id="info.search.page.next"]')
            if next_button.get_attribute('class') != 'next disabled':
                driver.find_element('xpath', '//*[@id="info.search.page.next"]').click()
                time.sleep(1.5)
            elif next_button.get_attribute('class') == 'next disabled':
                break
    except:
        pass

    for _ in range(len(temp)):
        region_list.append(reg)

    for _ in range(50):
        driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(Keys.BACKSPACE)

n = np.array([])
a = np.array([])
for nn,aa in zip(name_addr_dic.keys(), name_addr_dic.values()):
    n = np.append(n,nn)
    a = np.append(a,aa)

pd.DataFrame({'name':n, 'address':a}).to_excel(r'atwosomeplace.xlsx')




# -*- 추가 크롤링(영업시간) -*-
name_df = pd.read_excel('twosome_name.xlsx')

driver = webdriver.Chrome(r'C:\Users\usju\Downloads\chromedriver_win32\chromedriver.exe')
driver.get(r'https://map.kakao.com/')
driver.find_element('xpath', '//*[@id="dimmedLayer"]').click()

name = name_df['name'].values
time_table = {}
for i in range(len(name)):
    time_get = None
    place_name = name[i]
    try:
        driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(place_name)
        driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(Keys.ENTER)
        time.sleep(1.5)
        driver.find_element('xpath', '//*[@id="info.search.place.list"]/li[1]/div[5]/div[3]/p/a').click()
    except:
        pass

    if len(driver.window_handles) == 1:
        try:
            for _ in range(30):
                driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(Keys.BACKSPACE)
            driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(name[i])
            driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(Keys.ENTER)
            time.sleep(1.5)
            driver.find_element('xpath', '//*[@id="info.search.place.list"]/li[1]/div[5]/div[3]/p/a').click()
        except:
            for _ in range(30):
                driver.find_element('xpath', '//*[@id="search.keyword.query"]').send_keys(Keys.BACKSPACE)

    try:
        time.sleep(1.5)
        driver.switch_to.window(driver.window_handles[1])
        time_get = driver.find_element('xpath', '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[2]/div/ul').text
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass

    if time_get is None:
        try:
            time.sleep(1.5)
            time_get = driver.find_element('xpath', '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div/ul/li/span').text
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            time_get = ''
            if len(driver.window_handles) == 2:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    time_get = re.sub('\n', '|', time_get)
    time_table[name[i]] = time_get

    for _ in range(30):
        driver.find_element('xpath','//*[@id="search.keyword.query"]').send_keys(Keys.BACKSPACE)




# df['time_table'] = time_table
# df.to_excel(r'20220913_starbucks_finished.xlsx')

name_get = np.array([])
time_get = np.array([])
for k,v in zip(time_table.keys(), time_table.values()):
    name_get = np.append(name_get, k)
    time_get = np.append(time_get, v)

pd.DataFrame({'name':name_get,'time':time_get}).to_excel('atwosome_time.xlsx')
