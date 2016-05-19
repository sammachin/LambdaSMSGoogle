from __future__ import print_function

import json
import requests
from time import strftime as timestamp
from oauth2client.service_account import ServiceAccountCredentials
import gspread 
import nexmo

print('Loading function')

scopes =  ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scopes=scopes)
#Nexmo Credentials
nexmo_key = 'XXXXXX'
nexmo_secret = 'XXXXXX"

def addrow(sender, text):
    gc = gspread.authorize(credentials)
    sheet = gc.open('msgtest').worksheet("Sheet1")
    sheet.append_row([timestamp('%Y-%m-%d %H:%M:%S'), sender, text])
    

def lambda_handler(event, context):
    print("Received SMS: "  + json.dumps(event, indent=2))
    addrow(event['msisdn'], event['text'])
    client = nexmo.Client(key=nexmo_key, secret=nexmo_secret)
    client.send_message({'from': event['to'], 'to': event['msisdn'], 'text': 'thank-you'})
    return "OK"
