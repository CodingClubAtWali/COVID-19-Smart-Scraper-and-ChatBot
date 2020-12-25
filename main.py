import requests
from bs4 import BeautifulSoup
import math
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import time
import pymongo
from pymongo import MongoClient
import os
import json
from Corona import CovidInfo

currpath = os.getcwd()
with open(f'{currpath}/config.json') as f:
    data = json.load(f)

AccountSID = data['TwilioAccountSid']
AuthToken = data["TwilioAuthToken"]
PhoneNumber  = data["TwilioPhoneNumber"]
MongoConnectURL = data["MongoConnectUrl"]
GmailEmail = data["email"]
GmailPassword = data["password"]

cluster = MongoClient(f"{MongoConnectURL}") # Sync your MongoDB via 
db = cluster["COVID-19"]
collection = db['Countries']


header = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

with open(f"{currpath}/assets/emails.txt", 'r') as file:
    emailList = [email.strip() for email in file]
    file.close()
    
with open(f"{currpath}/assets/smsnumbers.txt", 'r') as file:
    smsList = [sms.strip() for sms in file]
    file.close()
    
def stats():
    global globalCases, globalDeaths, globalCured, activeCases, mildCondition, mildConditionPercentage, criticalCondition, criticalConditionPercentage
    while True:
        page = requests.get("https://www.worldometers.info/coronavirus/", headers = header).text
        scraper = CovidInfo(page)
        globalCases = scraper.totalCurrent()
        globalDeaths = scraper.totalDeaths()
        globalCured = scraper.totalCured()
        activeCases = scraper.totalActiveCases()
        mildCondition = scraper.totalMildCondition()
        criticalCondition = scraper.totalCriticalCondition()
        emailSender(f"{GmailEmail}", f"{GmailPassword}")
        smsSender(f"{AccountSID}", f"{AuthToken}", f"{PhoneNumber}")
        
        time.sleep(86400) # Make sure to change time

        
        
def emailSender(email, password):
    port = 465
    context = ssl.create_default_context()
    smtpServer = 'smtp.gmail.com'
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'COVID-19 Daily Update'
    msgRoot.preamble = 'Multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('Alternative plain text message.')
    msgAlternative.attach(msgText)
    msgText = MIMEText(f"""As-salamu alaykum,
<br>
The following information contains the daily update on COVID-19:
<br>
<br>
Coronavirus Cases <b>:</b> {globalCases}
<br>
Deaths <b>:</b> {globalDeaths}
<br>
Recovered <b>:</b> {globalCured}
<br>
Currently Infected Patients <b>:</b> {activeCases}
<br>
Patients that are currently in a mild condition <b>:</b> {mildCondition}
<br>
Patients that are in a critical condition <b>:</b> {criticalCondition} 
""", 'html')
    msgAlternative.attach(msgText)
    bcc_emails = emailList
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email, password)
        server.sendmail(email, bcc_emails, msgRoot.as_string())
        server.quit()
    print("Email Has Been Sent To Users")


def smsSender(accountSid, authToken, myNumber):
    client = Client(accountSid, authToken)
    messageBody = f"""As-salamu alaykum,

The following information contains the daily update on COVID-19:

The total number of cases is {globalCases}

The death toll is {globalDeaths}

There are currently {globalCured} cured patients

There is a total of {activeCases} active cases, {mildCondition} are in a non-critical state while {criticalCondition} are currently in a life threatning state.

"""
    for smsNumber in smsList:
        message = client.messages.create(
                    body= messageBody,
                    from_= myNumber,
                    to= smsNumber
                )
    print(message.sid)
        



stats()
