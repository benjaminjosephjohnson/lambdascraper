#This is the lambda function
#@Author: Benjamin Johnson

import json
import requests
from bs4 import BeautifulSoup
import re

def getstuff(event, context):

    #get page
    page = requests.get("https://coinmarketcap.com/")
    soup = BeautifulSoup(page.content, 'html.parser')
    #narrow down with css selectors
    coin_name=soup.select("td a.currency-name-container")
    marketcap=soup.select("td.market-cap")
    price=soup.select("td a.price")
    volume=soup.select("td a.volume")
    supply=soup.select("td a.stale")

    #clean the data
    a=[]
    for name in coin_name:
        a.append(name.text.strip())
    b=[]
    for mc in marketcap:
        b.append(mc.text.strip())
    c=[]
    for p in price:
        c.append(p.text.strip())

    #put all the data into a single list
    coins = []
    for i in zip(a,b,c):
        scrape_info={
        'input' : event,
        'status_code' : page.status_code,
        'name' : i[0],
        'marketcap' : i[1],
        'price' : i[2]
        }
        coins.append(scrape_info)

    #convert list of dicts to json
    coins=json.dumps(coins)
    return coins
