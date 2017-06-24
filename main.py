#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by Gwenael Griffon
"""

import time
import json
import requests
from bittrex import Bittrex

#Getting API keys
json_secrets=open("secrets.json")
secrets = json.load(json_secrets)
api_key = secrets["key"]
api_secret = secrets["secret"]

#Initialization
list_currency=[]
list_balance=[]
list_available=[]
list_pending=[]
list_last=[]
list_btcvalue=[]
list_market=[]
list_percent=[]
totalworth=0
i=0
n=0
k=0
btceuro=0
btcusd=0
wallet1=Bittrex(api_key,api_secret)
data=wallet1.get_balances()

#Date
print "\n","=====",time.strftime("%A %d %B %Y %H:%M:%S"),"=====","\n"

#Requesting BTC price
contenteuro=requests.get("https://www.bitstamp.net/api/v2/ticker/btceur/")
contenteuro=contenteuro.json()
btceuro=contenteuro["last"]
contentusd=requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/")
contentusd=contentusd.json()
btcusd=contentusd["last"]

#BTC percentage
btcfloat=float(btcusd)
btcopen=contentusd["open"]
btcopen=float(btcopen)
btcpercent=(1-(btcopen/btcfloat))*100
btcpercent=float(btcpercent)

#Picking non empty currencies
while i<len(data["result"]):
    if data["result"][i]["Balance"]==0 and data["result"][i]["Pending"]==0:
         i+=1
    else:
        list_currency.append((data["result"][i]["Currency"]))
        list_market.append(("BTC-"+data["result"][i]["Currency"]))
        list_balance.append(data["result"][i]["Balance"])
        list_available.append(data["result"][i]["Available"])
        list_pending.append(data["result"][i]["Pending"])
        i+=1
        
amount=len(list_currency)

#Getting currency price
while n<=amount-1:
    if list_market[n]=="BTC-BTC":
        list_last.append(btceuro+ " eur | "+btcusd+ " usd")
        list_btcvalue.append(list_balance[n])
        list_percent.append(btcpercent)
        n+=1
    else:
        ticker=wallet1.get_ticker(list_market[n])
        summary=requests.get("https://bittrex.com/api/v1.1/public/getmarketsummary?market="+list_market[n])
        summary=summary.json()
        summary=summary["result"][0]["PrevDay"]
        summary=float(summary)
        percent=(1-(summary/ticker["result"]["Last"]))*100
        percent=float(percent)
        ticker=ticker["result"]["Last"]
        ticker=float(ticker)
        list_last.append(ticker)
        list_btcvalue.append(list_last[n]*list_balance[n])
        list_percent.append(percent)
        n+=1
        
#Printing wallet details
while k<=amount-1:
    totalworth+=list_btcvalue[k]
    if k==0:
        print list_currency[k],"(",list_last[k],"|","%+.2f" % list_percent[k],"%",")","\n","Balance : ","%.8f" % list_balance[k],"\n","Available : ","%.8f" % list_available[k],"\n","Pending : ","%.8f" % list_pending[k],"\n","Worth : ","%.8f" % list_btcvalue[k]," btc","\n","\n"
    else :
        print list_currency[k],"(","%.8f" % list_last[k],"|","%+.2f" % list_percent[k],"%",")","\n","Balance : ","%.8f" % list_balance[k],"\n","Available : ","%.8f" % list_available[k],"\n","Pending : ","%.8f" % list_pending[k],"\n","Worth : ","%.8f" % list_btcvalue[k]," btc","\n","\n"
    k+=1
btceuro=float(btceuro)
btcusd=float(btcusd)

print "Total worth : ","%.8f" % totalworth," btc", "\n","              ","%.2f" % (totalworth*btceuro), "eur", "\n","              ","%.2f" % (totalworth*btcusd), "usd", "\n"

    
