import requests
import time 
import math
from lxml import etree
from bs4 import BeautifulSoup

header = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
page = requests.get("https://www.worldometers.info/coronavirus/", headers = header).text

class CovidInfo():
    
    def __init__(self, page):
        self.page = page
        self.soup = BeautifulSoup(self.page, 'lxml')
        
    
    def totalCurrent(self):
        globalCases = self.soup.find(class_ = "maincounter-number").get_text()
        return globalCases.strip()

    def totalDeaths(self):
        globalDeaths = self.soup.findAll(class_ = "maincounter-number")[1].get_text()
        return globalDeaths.strip()
    
    def totalCured(self):
        globalCured = self.soup.findAll(class_ = "maincounter-number")[2].get_text()
        return globalCured.strip()
    
    def totalActiveCases(self):
        activeCases = self.soup.find(class_ = "number-table-main").get_text()
        return activeCases.strip()

    def totalMildCondition(self):
        mildCondition = self.soup.find(class_ = "number-table").get_text()
        return mildCondition.strip()
    
    def totalCriticalCondition(self):
        criticalCondition = self.soup.findAll(class_ = "number-table")[1].get_text()
        return criticalCondition.strip()
        