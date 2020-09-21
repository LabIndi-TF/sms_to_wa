from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep

import config

#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from time import sleep
import urllib.parse
driver = None
Link = "https://web.whatsapp.com/"
wait = None

def whatsapp_login():
    global wait, driver, Link
    firefox_options = Options() #chrome_options = Options()
    firefox_options.add_argument('--user-data-dir=./User_Data') #chrome_options.add_argument('--user-data-dir=./User_Data')
    driver = webdriver.Firefox(options=firefox_options) #driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    print("SCAN YOUR QR CODE FOR WHATSAPP WEB IF DISPLAYED")
    driver.get(Link)
    driver.maximize_window()
    print("QR CODE SCANNED")

def SendBufferToWA(nomor_hape,message_buffer):
    params = {'phone': nomor_hape}
    end = urllib.parse.urlencode(params)
    final_url = Link + 'send?' + end
    print(final_url)
    driver.get(final_url)
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//div[@title = "Menu"]')))
    print("Page loaded successfully.")

    msg_box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")

    for item in message_buffer:
        encoded_msg = item.decode(config.TEXT_ENCODING)
        if '\r' not in encoded_msg:
            msg_box.send_keys(encoded_msg[:-1])
            msg_box.send_keys(Keys.LEFT_SHIFT, Keys.ENTER)
        else:
            msg_box.send_keys(encoded_msg)
            '''
            driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
            '''