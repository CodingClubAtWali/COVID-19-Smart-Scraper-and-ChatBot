# COVID-19 Smart Scraper

## Overview
The COVID-19 Smart Scraper is a tool that is developed by the members of the Wali Ul Asr Learning Institute Coding Club! This tool scrapes statistical information related to COVID-19 such as the total cases, deaths, cured, amount in critical / mild condition worldwide and for individual countries. Our tool monitors the statistics of over 220 countires at 10 minute intervals. All the information is stored in a secure database (MongoDB). The information is coneveyd by SMS and Email. We also took this project one step forward by making it a chatbot to go along with the sms delviery. When a user messages the phone number (+1 647-360-6629) with a country name, it will respond with the following information about the country:
    
    - Total Cases
    - Total Deaths
    - Total Recovered
    - Active Cases
    - Serious/Critical Condition
    - New Cases
    - New Deaths
    - Total Tests
    - Population

## Installation

You will need to use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following modules

```bash
pip3 install pymongo
pip3 install flask
pip3 install requests
pip3 install selenium
pip3 install pandas
pip3 install ssl
pip3 install twilio
pip3 install lxml
pip3 install bs4
pip3 install dnspython
```

You will also need the appropriate chromedriver that maches your chrome version installed. 

## Usage

In order to get the code up and running you will need to configure the "config.json" file with the required values. Once the config.json file is filled, you can run the Table_Scraper.py in one screen and main.py in another (assuming you are running linux). If you are using windows, run Table_Scraper.py file in one terminal and main.py in another.

## Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

