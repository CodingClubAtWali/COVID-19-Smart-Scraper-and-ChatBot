from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
import json
from pymongo import MongoClient
import pymongo

app = Flask(__name__)
currpath = os.getcwd()

with open(f'{currpath}/countries.txt', 'r') as file:
    countries = [countryName.strip() for countryName in file]
    file.close() 
    
with open(f'{currpath}/config.json') as f:
    data = json.load(f)

MongoConnectURL = data["MongoConnectUrl"]

cluster = MongoClient(f"{MongoConnectURL}")

db = cluster["COVID-19"]
collection = db['Countries']

@app.route("/sms", methods=['GET', 'POST'])
def incomming_sms():
    resp = MessagingResponse()
    body = request.values.get('Body', None)
    if body not in countries:
        resp.message(f'The country "{body}" is currently not in our database. Please respond with a country (case sensitive) from the following list https://www.infect.services/countries')
        return str(resp)
    else:
        countryInfo = collection.find_one({"Country,Other": body})
        totalCountryCases = countryInfo["TotalCases"]
        totalCountryDeaths = countryInfo['TotalDeaths']
        totalCountryRecovered = countryInfo['TotalRecovered']
        totalCountryActiveCases = countryInfo['ActiveCases']
        totalCountrySeriousCritical  = countryInfo['Serious,Critical']
        newCountryCases = countryInfo['NewCases']
        newCountryDeaths = countryInfo['NewDeaths']
        totalCountryTests = countryInfo['TotalTests']
        totalCountryPopulation = countryInfo['Population']
 
        resp.message(body = f"""Country: {body}
Total Cases: {totalCountryCases}
Total Deaths: {totalCountryDeaths}
Total Recovered: {totalCountryRecovered}
Active Cases: {totalCountryActiveCases}
Serious/Critical Condition: {totalCountrySeriousCritical}
New Cases: {newCountryCases}
New Deaths: {newCountryDeaths}
Total Tests: {totalCountryTests}
Population: {totalCountryPopulation}

If a value is None, it indicates that the information is not currently in our database.
Our database is updated every 10 minutes.
""")
        return str(resp)
        
        
    
if __name__ == "__main__":
    app.debug=True
    app.run(host = '0.0.0.0', port = 80)