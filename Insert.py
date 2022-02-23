#pip install psycopg2/tkinter
import psycopg2
import pandas as pd
from tkinter import filedialog
from tkinter import *

def getName(name):
    a = ''
    for i in range(len(name)):
        a = a + name[i].get('table_name') + "/"
    return a

def getLocation():
    window = Tk()
    filepath = filedialog.askopenfilename(filetypes=(("xlsx", "*.xlsx"), ("all files", "*.*"))) #===assigns the path to filepath
    label = Label(window, text=filepath) #==Adds Label to window 
    label.pack()
    return filepath

conn = psycopg2.connect(host="localhost", port = 5432, database="DV_demo", user="postgres", password="sony2014")
statment= "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
df= pd.read_sql_query(statment ,con=conn)
names = df.to_dict('records')
name = getName(names)
selected_table = input(f'Select table to input data to ({name}): ')
folder = getLocation()
f = open(folder, 'r')
cur = conn.cursor()
cur.copy_from(f, selected_table, sep=',')
conn.commit()
f.close()
