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
    need = ['№ регистрации','Дата регистрации','Статус','Владелец','Название','МКТУ','Срок действия','Номер бюллетеня','Дата бюллетеня']
    clean_data = []
    for i, datum in enumerate(data.split('\n')):
        clean_data.append(datum[len(need[i])+1:])
    return clean_data


def save_data(data):

    with open('data.csv', 'a+', newline='') as file:
        data = cleaner(data)
        writer = csv.writer(file)
        writer.writerow(data)
    return data[0]
    

# def save_image(button, name):

#     button.click()
    
#     old_window = driver.window_handles[0]
#     new_window = driver.window_handles[1]
#     driver.switch_to.window(new_window)
    

#     time.sleep(1)
#     try:
#         l = driver.find_element(By.XPATH, '//*[@class="dxeImage_Material"]')
#     except:

#         driver.switch_to.window(old_window)
#         return 
    
#     with open(imgs+'/'+name+'.png', 'wb') as file:
#         file.write(l.screenshot_as_png)
    
#     driver.switch_to.window(old_window)

def save_image(button, name):
    temp_driver.get(button.get_attribute('href'))
    # time.sleep(1)

    try:
        logo = temp_driver.find_element(By.XPATH, '//*[@class="dxeImage_Material"]')
    except:
        return 
    
    with open(imgs+'/'+name+'.png', 'wb') as file:
        file.write(logo.screenshot_as_png)
    



def go_to_the_list(driver):
    driver.find_element(By.ID,"nbFilters_GHC4").click()
    time.sleep(1)
    driver.find_element(By.ID, "nbTrademarkFilters_GHC1").click()
    time.sleep(1)
    driver.find_element(By.ID, "btnFind1_Trademark_CD").click()
    time.sleep(1)
    
    while(True):
        parse(driver)
        tempe = "//*[@class='dxp-button dxp-bi dxRoundRippleTarget dxRippleTarget']"
        driver.find_elements(By.XPATH, tempe)[1].click()
        time.sleep(2)
    

def parse(driver):
    ids = []

    tovar = driver.find_elements(By.XPATH, '//*[@class="dxcvFlowCard_Material FlowCard"]')
    
    for i in tovar:
        id = save_data(i.text)
        ids.append(id)
    
    buttons = driver.find_elements(By.XPATH, '//*[@class="btn btn-circle btn-success fa fa-file-text btn-view"]')
    
    for i, id in zip(buttons,ids):
        save_image(i, id)
        time.sleep(1)
    
    


    





def main():
    try:
        driver.get('https://gosreestr.kazpatent.kz')
        # time.sleep(1)
        go_to_the_list(driver)
        # time.sleep(1)


        # driver.find_elements(By.XPATH, '//*[@class="dxp-button dxp-bi dxRoundRippleTarget dxRippleTarget"]')[1].click()
        
        # tempe = "//a[@class='dxp-button dxp-bi dxRoundRippleTarget dxRippleTarget'][@alt='Следующая']"
        # driver.find_element(By.XPATH, tempe)
        
        
            
        

    except Exception as e:
        print(e)
    finally:

        driver.close()
        driver.quit()
        temp_driver.close()
        temp_driver.quit()


if __name__ == "__main__":
    main()


