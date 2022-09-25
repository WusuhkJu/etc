import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



driver_path_ = r'C:\Users\usju\Downloads\chromedriver\chromedriver.exe'
url_path_ = r'https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1656295802&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26nlp%3d1%26RpsCsrfState%3d464bb016-6e2b-d92f-e9e6-de41b76564ad&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c'

theme_ = '[한국갤럽조사연구소] 앱 제작 문의'
letter_body_ = """
안녕하십니까? 한국갤럽조사연구소입니다.
항상 좋은 하루 되시길 바랍니다. \n

* 연락처
한국갤럽 데이터사이언스팀 김태우 부장 twkim@gallup.co.kr
한국갤럽 데이터사이언스팀 주우석 선임 usju@gallup.co.kr \n
"""



class Send_mail_by_person:
    def __init__(self, driver_path=driver_path_, url_path=url_path_):
        self.driver = webdriver.Chrome(driver_path)
        self.driver.get(url_path)
    
    def login(self, outlook_id, outlook_pw):                
        self.driver.find_element_by_id('i0116').send_keys(outlook_id)
        time.sleep(5)
        self.driver.find_element_by_id('idSIButton9').click()
        time.sleep(5)
        self.driver.find_element_by_id('i0118').send_keys(outlook_pw)
        time.sleep(5)
        self.driver.find_element_by_id('idSIButton9').click()
        time.sleep(5)
        self.driver.find_element_by_id('idBtn_Back').click()
        time.sleep(10)
        print('####### login has done #######')

    def send_email(self, df_email_list, theme=theme_, letter_body=letter_body_):
        driver = self.driver
        ar_email_list = df_email_list['email_list'].values
                
        for e in range(len(ar_email_list)):
            email = ar_email_list[e]

            driver.find_element_by_xpath('//div[@id="app"]/div[@class="B1J42 body-154"]/div[@class="L_9jp"]/div[@class="Z1wHl"]/div[@class="body-154"]/div/div/div/div/div/div[1]/div[2]').click()
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div[3]/div[1]/div/div/div[1]/div[1]/div[1]/div/div[4]/div/div/div/div/div/div[1]/div/div/input').send_keys(email)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div[3]/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div/input').send_keys(theme_)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div/div/div').send_keys(letter_body_)
            time.sleep(1)            
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div/span/div/div/div/div/div[1]/div[3]').click()
            time.sleep(3)

            i = 1
            s = 0
            while s == 0:
                try:
                    s += 1
                    driver.find_element_by_xpath('/html/body/div[3]/div[{}]/div/div/div/div/div/div/ul/li[2]/button/div/span'.format(i))            
                except:
                    i += 1
                    s -= 1
                    pass

            driver.find_element_by_xpath('/html/body/div[3]/div[{}]/div/div/div/div/div/div/ul/li[2]/button/div/span'.format(i)).click()
            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div[3]/div[{}]/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div[1]/div[2]/div'.format(i)).click()
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[3]/div[{}]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/div/div[1]/div/div/i[2]'.format(i)).click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[3]/div[{}]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[3]/div/button/span/span/span'.format(i)).click()
            time.sleep(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div[3]/div[1]/div/div/div[1]/div[3]/div[3]/div[1]/div/div/span/button[1]').click()
            time.sleep(5)
            print('=========={}/{} has done=========='.format(e+1, len(ar_email_list)))
        
        print("******************** sending mail has completed ********************")





mail_inst = Send_mail_by_person()
mail_inst.login(outlook_id='usju@gallup.co.kr', outlook_pw='Qawsedrf1!')

df_email_list_ = pd.read_csv(r'C:\Users\usju\PycharmProjects\game_company\email_list_test.csv')

mail_inst.send_email(df_email_list=df_email_list_)