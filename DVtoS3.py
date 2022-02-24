import json
import requests
import pandas as pd
from tkinter import filedialog
from tkinter import *

def getToken(API):
    headers = {
        'accept': 'application/json',
        'X-API-KEY': API,
        'Content-Type': 'application/json',
    }

    response = requests.get('https://api.diligencevault.com/api/v2/get-token/', headers=headers)
    data = json.loads(response.text)
    token = data.get('access_token')
    token = 'Bearer ' + token
    return token

def fileLocation():
    root = Tk()
    root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("Zip files","*.zip"),("all files","*.*")))
    return root.filename

def getQns(key, token, start_date, end_date, f, status):
    headers = {
        'accept': 'application/json',
        'Authorization': token,
        'X-API-KEY': key,
    }

    if status == "All":
        url = 'https://api.diligencevault.com/api/v2/projects/projects_download?start_date=%s&end_date=%s'% (start_date, end_date)
    else:
        url = 'https://api.diligencevault.com/api/v2/projects/projects_download?start_date=%s&end_date=%s&status=%s'% (start_date, end_date, status)

    response = requests.get(url, headers=headers)

    file = open(f, "wb")
    file.write(response.content)
    file.close()

API_key = input('Please enter API Key: ')
token = getToken(API_key)
print('Extracting Questionnaires ... ')
start_date = input("Please input start date(yyyy-mm-dd): ")
end_date = input("Please input end date(yyyy-mm-dd): ")
status = input("Please input project status (All, Approved, Completed, Followup): ")
file = fileLocation()
getQns(API_key, token, start_date, end_date, file, status)