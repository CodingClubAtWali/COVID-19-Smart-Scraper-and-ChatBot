import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from twilio.rest import Client
import os

currpath = os.getcwd()


with open(f"{currpath}/assets/emails.txt", 'r') as file:
    emailList = [email.strip() for email in file]
    file.close()
    
with open(f"{currpath}/assets/smsnumbers.txt", 'r') as file:
    smsList = [sms.strip() for sms in file]
    file.close()


def emailSender(self):
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
    msgText = MIMEText(f"""Hello,

The following information contains the daily update on COVID-19:

Coronavirus Cases : {globalCases}
Deaths : {globalDeaths}
Recovered : {globalCured}
Currently Infected Patients : {activeCases}
Patients in mild condition: 
Patients in critical condition: 
""", 'html')
    msgAlternative.attach(msgText)
    bcc_emails = emailList
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(self.email, self.password)
        server.sendmail(self.email,bcc_emails, msgRoot.as_string())
        server.quit()
    print("Email Has Been Sent To Users")


def smsSender(self, accountSid, authToken, myNumber):
    client = Client(accountSid, authToken)
    messageBody = f"""Hello,

The following information contains the daily update on COVID-19:

Coronavirus Cases : {globalCases}
Deaths : {globalDeaths}
Recovered : {globalCured}
Currently Infected Patients : {activeCases}
Patients in mild condition: 
Patients in critical condition: 
"""
    for smsNumber in self.numberList:
        message = client.messages.create(
                    body= messageBody,
                    from_= myNumber,
                    to= smsNumber
                )
    print(message.sid)
        


        
    
