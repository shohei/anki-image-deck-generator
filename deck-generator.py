#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import glob
import os
from tqdm import tqdm
import pdb
import errno
from selenium.webdriver.chrome.options import Options # オプションを使うために必要

DATA_DIR = "data/male" #Change here


def get_image(q, df, csv_filename):
    option = Options()                          # オプションを用意
    option.add_argument('--headless')           # ヘッドレスモードの設定を付与
    driver = webdriver.Chrome(options=option)   
    img_folder = "image/"+csv_filename
    try:
        print("create folder: {0}".format(img_folder))
        os.makedirs(img_folder)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    url = "https://images.search.yahoo.com/"
    
    driver.get(url)
    search = driver.find_element("name", 'p')
    search.send_keys(q)
    search.send_keys(Keys.ENTER)
    
    width = 700
    height = 860
    driver.set_window_size(width,height)
    
    time.sleep(3)
    
    images = driver.find_element("id", 'main')
    img_name = img_folder+"/"+q+".png"
    images.screenshot(img_name)
    print("screenshot saved: {0}".format(img_name))
    
    d = pd.DataFrame(data={"Question":["Who is this?"],
                            "Answer":[q],
                            "Image": ['<img src="{0}">'.format(img_name)]})
    df = pd.concat([df,d])

    time.sleep(1)

    return df

filedir = DATA_DIR+"/**/*.txt"
print(filedir)
files = glob.glob(filedir)
print(files)
csv_filename = ""
df = pd.DataFrame(columns=['Question', 'Answer', 'Image'])

for filename in files:
    csv_filename = filename.replace("data/","")
    csv_filename = csv_filename.replace(".txt","")

    print("working on {0}".format(csv_filename))
    fin = open(filename).readlines()
    for name in tqdm(fin):
        name = name.rstrip()
        print(name)
        df = get_image(name, df, csv_filename)

    csv_filename = "data/"+csv_filename+".csv"
    df.to_csv(csv_filename, index=False)

cmd = "find . -name '*.png' -exec pngquant --ext .png --force {} \;"
os.system(cmd)