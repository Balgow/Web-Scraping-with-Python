from distutils.log import info
from selenium.webdriver.common.keys import Keys
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import csv
import os

imgs = os.path.join(os.getcwd(), r'images')

capabilities = webdriver.DesiredCapabilities.CHROME
chromeOptions = webdriver.ChromeOptions() 

temp_driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=capabilities, executable_path='/home/chingizkhan/Downloads/chromedriver')
temp_driver.maximize_window()

driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=capabilities, executable_path='/home/chingizkhan/Downloads/chromedriver')
driver.maximize_window()


def cleaner(data):
    need = ["Статус ",'(111) № регистрации ','(151) Дата регистрации ', '(210) Номер заявки ','(220) Дата подачи заявки ','(730) Владелец ','(181) Срок действия ','(511) Класс МКТУ ','(450) Номер и дата бюллетеня ']
    # need = ['№ регистрации','Дата регистрации','Статус','Владелец','Название','МКТУ','Срок действия','Номер бюллетеня','Дата бюллетеня']
    clean_data = []
    for i, datum in enumerate(data.split('\n')):
        clean_data.append(datum[len(need[i]):])
    return clean_data


def save_data(button):
    
    temp_driver.get(button.get_attribute('href'))

    time.sleep(1)
    try:
        inf = temp_driver.find_element(By.XPATH, '//*[@class="detial_plan_info"]')
        time.sleep(1)
    except:
        return
    
    with open('data.csv', 'a+', newline='') as file:
        data = [datum for datum in inf.text.split('\n')]
        writer = csv.writer(file)
        writer.writerow(data)
    
    name = data[1][len('(111) № регистрации '):]

    


    try:
        logo = temp_driver.find_element(By.XPATH, '//*[@class="dxeImage_Material"]')
        time.sleep(1)
    except:
        return 
    
    with open(imgs+'/'+name+'.png', 'wb') as file:
        file.write(logo.screenshot_as_png)
    time.sleep(1)
    



def go_to_the_list(driver):
    driver.find_element(By.ID,"nbFilters_GHC4").click()
    time.sleep(1)
    driver.find_element(By.ID, "nbTrademarkFilters_GHC1").click()
    time.sleep(1)
    driver.find_element(By.ID, "btnFind1_Trademark_CD").click()
    time.sleep(1)
    
    while(True):
        parse(driver)
        driver.find_elements(By.XPATH, "//*[@class='dxp-button dxp-bi dxRoundRippleTarget dxRippleTarget']")[1].click()
        time.sleep(2)
    

def parse(driver):
    
    buttons = driver.find_elements(By.XPATH, '//*[@class="btn btn-circle btn-success fa fa-file-text btn-view"]')

    time.sleep(1)

    for i in buttons:
        save_data(i)
        time.sleep(1)
    
    


    





def main():
    try:
        driver.get('https://gosreestr.kazpatent.kz')
        go_to_the_list(driver)


    except Exception as e:
        print(e)
    finally:

        driver.close()
        driver.quit()
        temp_driver.close()
        temp_driver.quit()


if __name__ == "__main__":
    main()


