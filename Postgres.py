import psycopg2
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_table

app = dash.Dash()

#Connect to my localhost DB, than show the list of table names in DB
conn = psycopg2.connect(host="localhost", port = 5432, database="DV_demo", user="postgres", password="sony2014")
statment= "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
df= pd.read_sql_query(statment ,con=conn)
names = df.to_dict('records')

#-----------------------------------------------------------------------

#Create table name in dropdown
def getName(name):
    a = []
    for i in range(len(name)):
        a.append(name[i].get('table_name'))
    return a
#-----------------------------------------------------------------------

#Create Graph
def getGraph(v):
    if v == None:
        return html.H3(children = 'Select table')
    else:
        s = f'Select * from  {v};'
        statment= s
        df= pd.read_sql_query(statment ,con=conn)
        return html.Div([
            dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15),
            html.Hr(),
            html.P("Insert X axis data"),
            dcc.Dropdown(id='xaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
            html.P("Insert Y axis data"),
            dcc.Dropdown(id='yaxis-data',
            options=[{'label':x, 'value':x} for x in df.columns]),
            html.P("Choose Chart type"),
            dcc.Dropdown(id='graph-data',
            options=['Bar', 'Line', 'Scatter']),
            html.Button(id="submit-button", children="Create Graph", style = {'marginTop':40}),
            dcc.Store(id='stored-data', data=df.to_dict('records'))
        ])
#--------------------------------------------------------------------------

#Dropdown call back function
@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'
#-----------------------------------------------------------------------------

#Table building for selected table function
@app.callback(
    Output('output-datatable', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    children = getGraph(value)
    return children
#-----------------------------------------------------------------------------

#Callback to create Graphs
@app.callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'),
              State('graph-data', 'value'))
def make_graphs(n, data, x_data, y_data, chart_type):
    if n is None:
        return dash.no_update
    else:
        if chart_type == 'Bar':
            bar_fig = px.bar(data, x=x_data, y=y_data)
            return dcc.Graph(figure=bar_fig)
        elif chart_type == "Line":
            line_fig = px.line(data, x=x_data, y=y_data)
            return dcc.Graph(figure=line_fig)
        elif chart_type =='Scatter':
            pie_fig = px.scatter(data, x=x_data, y=y_data)
            return dcc.Graph(figure=pie_fig)
#------------------------------------------------------------------------------

#Main 
table_name = getName(names)
app.layout = html.Div([
    html.H1(children = 'Select Table:'),
    dcc.Dropdown(table_name, id='demo-dropdown'),
    html.Div(id='dd-output-container'),
    html.Div(id='output-datatable'),
    html.Div(id='output-div')
])
#-------------------------------------------------------------------------------

# app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

if __name__ == '__main__':
    app.run_server(debug=True)

