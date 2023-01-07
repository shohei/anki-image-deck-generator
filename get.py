#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

df = pd.DataFrame(columns=['Question', 'Answer', 'Image'])

driver = webdriver.Chrome()
queries = ["能年玲奈","相武紗季"]
img_folder = "image/female/japan/"

url = "https://images.search.yahoo.com/"



for q in queries:
    driver.get(url)
    search = driver.find_element("name", 'p')
    search.send_keys(q)
    search.send_keys(Keys.ENTER)
    
    width = 700
    height = 860
    driver.set_window_size(width,height)
    
    time.sleep(3)
    
    images = driver.find_element("id", 'main')
    img_name = img_folder+q+".png"
    images.screenshot(img_name)
    
    d = pd.DataFrame(data={"Question":["Who is this?"],
                            "Answer":[q],
                            "Image": ['<img src="{0}">'.format(img_name)]})
    print(d)

    df = pd.concat([df,d])

df.to_csv('out.csv', index=False)

cmd = "find . -name '*.png' -exec pngquant --ext .png --force {} \;"
os.system(cmd)
