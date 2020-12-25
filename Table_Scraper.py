import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import json
import os

currpath = os.getcwd()

with open(f'{currpath}/config.json') as f:
    data = json.load(f)

MongoConnectURL = data["MongoConnectUrl"]

cluster = MongoClient(f"{MongoConnectURL}")
db = cluster["COVID-19"]
collection = db['Countries']

def tableScraper():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    while True:
        try:
        
            driver.get("https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?%22")
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "nav-tabContent")))
            time.sleep(10)
            pandaTable = pd.read_html(driver.page_source)[0]
            driver.quit()
            pandaTable.drop(["#"], axis = 1, inplace = True) 
            pandaTable.to_json(path_or_buf = f"{currpath}/assets/countries.json", orient = 'records')
            #pandaTable.to_csv('countries.csv', index = False)
            with open(f'{currpath}/assets/countries.json') as file:
                data = json.loads(file.read())
                file.close()
            collection.delete_many({})
            collection.insert_many(data)
            print("Data Collected") 
            time.sleep(60)
        except:
            print("Temp Blocked, trying again")
            time.sleep(1)
            tableScraper()

tableScraper()