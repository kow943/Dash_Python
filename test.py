from dash import dash, html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash()   #initialising dash app
df = px.data.stocks() #reading stock price dataset  
 
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
        options = [
            {'labels':'Google', 'value':'GOOG' },
            {'labels': 'Apple', 'value':'AAPL'},
            {'labels': 'Amazon', 'value':'AMZN'},
            ],
        value = 'GOOG'),
        dcc.Graph(id = 'plot')
    ])

@app.callback(Output(component_id='plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])

def graph_update(dropdown_value):
    print(dropdown_value)
    fig = px.bar(x = df['date'], y = df['{}'.format(dropdown_value)])
    
    fig.update_layout(title = 'Stock prices over time',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    return fig  



if __name__ == '__main__': 
    app.run_server()