import psycopg2
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_table

app = dash.Dash()

conn = psycopg2.connect(host="localhost", port = 5432, database="DV_demo", user="postgres", password="sony2014")
s = f'Select * from  sales;'
statment= s
df = pd.read_sql_query(statment ,con=conn)
country = df.country.unique().tolist()

def dashboardCreate(c):
    return html.Div([
        html.P(f'You have selected {c}'),
        dcc.Graph(id = 'plot')
    ])

@app.callback(Output(component_id='plot', component_property= 'figure'),
              [Input(component_id='country-dropdown', component_property= 'value')])
def graph_update(value):
    a = [value]
    new_df = df[df["country"].isin(a)]
    fig = px.histogram(new_df, x=new_df['year_id'], y=new_df['sales'], barmode='group')

    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            dtick = 1,
        ),
        bargap =0.1
    )

    return fig 

@app.callback(
    Output('dd-output-container', 'children'),
    Input('submit-button','n_clicks'),
    Input('country-dropdown', 'value')
)
def update_output(n, value):
    if n is None:
        return dash.no_update 
    else:
        return dashboardCreate(value)

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Performance DashBoard', style = {'textAlign':'center','marginBottom':40}),
    dcc.Dropdown(options=country, id='country-dropdown'),
    html.Button(id="submit-button", children="Select Country", style = {'marginTop':20}),
    html.Div(id='dd-output-container')
    ])

if __name__ == '__main__':
    app.run_server(debug=True)