#pip install psycopg2/tkinter
import psycopg2
import psycopg2.extras as extras
import pandas as pd
from tkinter import filedialog
from tkinter import *
import os 

def getName(name):
    a = []
    for i in range(len(name)):
        a.append(name[i].get('table_name'))
    return a

def getLocation():
    window = Tk()
    filepath = filedialog.askopenfilename(filetypes=(("xlsx", "*.xlsx"), ("all files", "*.*"))) #===assigns the path to filepath
    label = Label(window, text=filepath) #==Adds Label to window 
    label.pack()
    return filepath

def returnName(file):
    x = file.split('.')
    return x[0]


conn = psycopg2.connect(host="localhost", port = 5432, database="DV_demo", user="postgres", password="sony2014")
statment= "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
df= pd.read_sql_query(statment ,con=conn)
names = df.to_dict('records')
name = getName(names)

folder = getLocation()
fileName = returnName(os.path.basename(folder))

if(fileName not in name):
    print('Uploaded unsuitable file! Please check title!')
else:
    df = pd.read_csv(folder)
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (fileName, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
    print("the dataframe is inserted")
    cursor.close()
