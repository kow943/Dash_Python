import os
import pandas as pd
import json
from tkinter import filedialog
from tkinter import *
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

df = pd.DataFrame(columns=['Location/Country',
 'Mode of Travel',
 'Total distance km travelled in the reporting year (per travel mode)',
 'Source',
 'Remarks if any',
 'entityName'])

def runCompanyDF(data):
    global df
    dataframe = pd.DataFrame(data)
    df = pd.concat([df,dataframe], ignore_index=True)

def getDF(company):
    headers = company['response'][0]['table_data']['columns']
    datajson = []

    for i in company['response'][0]['table_data']['rows']:
        a ={}
        for x in range(0, len(headers)):
          companyList = company['response'][0]['table_data'][i]
          a[headers[x]] = companyList[x]
        a['entityName'] = company['entity_name']
        datajson.append(a)
    runCompanyDF(datajson)

def openFile(file, folder):
    company = open('%s//%s//responses//responses.json' % (folder, file))
    company = json.load(company) 
    getDF(company[4])

def getLocation():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected


folder = getLocation()
for file in os.listdir(folder):
    if(file != 'projects.json'):
        print('Opening %s folder: %s loading ... ' % (folder, file))
        value = openFile(file, folder)

df = df.set_axis([
    'LOCATIONCOUNTRY',
	'MODE_OF_TRAVEL',
    'TOTAL_DISTANCE_KM_TRAVELLED',
	'SOURCE',
	'REMARKS_IF_ANY',
	'ENTITYNAME'
], axis = 1, inplace = False)

ctx = snowflake.connector.connect(
    user='Skanagasabai',
    password='Dxc2022####',
    account='qx10182.ap-southeast-1',
    warehouse = 'compute_wh',
    database = 'siva',
    schema = 'public'
    )
try:
    success, nchunks, nrows, _ = write_pandas(ctx, df, 'EMPLOYEE_COMMUTING')
finally:
    ctx.close()

print(str(success)+ ', ' + str(nchunks) + ', ' + str(nrows))
        

