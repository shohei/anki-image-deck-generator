#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

#url = "https://www.google.co.jp/"
url = "https://images.search.yahoo.com/"
driver.get(url)

#search = driver.find_element("name", 'q')
search = driver.find_element("name", 'p')
search.send_keys("能年玲奈")
search.send_keys(Keys.ENTER)

width= driver.execute_script("return document.body.scrollWidth")
height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(width,height)

time.sleep(3)

driver.save_screenshot("screnshot.png")


time.sleep(100)




