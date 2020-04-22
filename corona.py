import time 
import json
import requests
from difflib import get_close_matches
from collections import OrderedDict

scraping_url = "https://covidapi.info/api/v1/"

def get_country_iso(country_name = None):
    try:
        if country_name:        
            with open('data.country') as file:
                content = file.read()
            data_iso = json.loads(content)
            country_name = get_close_matches(country_name, data_iso.keys())[0]
            isocode = data_iso.get(country_name, False)
            return isocode
        else:
            return
    except Exception as ex:
        print(ex)
        print('Error occured while scraping ..probably internet is not working')
        return

 
def scrap_number_from_cloud():
    country_name = input('Enter country name : ')
    isocode = get_country_iso(country_name)
    if isocode:
        payload = {};headers= {}
        country_url = scraping_url+'country/'+isocode
        response = requests.request("GET", country_url, headers=headers, data = payload)
        info = response.json()['result']
        date  = list(OrderedDict(sorted(info.items())))[-1]
        data = info[date]
        message = "According to John Hopkins {} released on {} \n numbers are \nConfirmed cases {}\nDeath {} \nRecovered {}".format("https://coronavirus.jhu.edu/", date, data['confirmed'], data['deaths'], data['recovered'])
        print(message)
        return message
    else:
        response = 'Can\'t find match for your country'
        print(response)
        return response

while True:
    scrap_number_from_cloud()
    time.sleep(2)
