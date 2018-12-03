
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 

# In[2]:


# Setting everything up
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv("C://Users//Max//Dropbox//ESADE//Subjects//Cloud Computing//7 - Data Science in the cloud Data Visualization//CC 7//CC 7//nama_10_gdp//nama_10_gdp_1_Data.csv")
df = df.rename(index = str, columns = {"GEO": "Country Name", "TIME": "Year", "UNIT": "Unit", "NA_ITEM": "Indicator Name"}).set_index("Country Name")
df = df.drop(['European Union (current composition)',
       'European Union (without United Kingdom)',
       'European Union (15 countries)',
       'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
       'Euro area (19 countries)', 'Euro area (12 countries)'], axis = 0)
df = df.drop("Flag and Footnotes", axis = 1)
df = df.rename(index = {'Germany (until 1990 former territory of the FRG)': "Germany", 
                         'Kosovo (under United Nations Security Council Resolution 1244/99)': "Kosovo",
                        'Former Yugoslav Republic of Macedonia, the': "Macedonia"})
df = df[df["Unit"]=='Current prices, million euro'].reset_index()

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['Indicator Name'].unique()
available_countries = df["Country Name"].unique()

# App/Dashboard layout
app.layout = html.Div([
    html.Div([

        html.H1(children='1. Graph: Select two indicators'),
        
        html.Div(
            dcc.Dropdown(
                id='x1axis-column',
                options=[{"label": i, "value": i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ), style={'width': '48%', 'display': 'inline-block'}),

        html.Div(
            dcc.Dropdown(
                id='y1axis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods'
            ), style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        
    ]),

    dcc.Graph(id='indicator-graphic1'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ),
    
    html.H1(children='2. Graph: Select country and indicator'),
    
    html.Div([

        html.Div(
            dcc.Dropdown(
                id='x2axis-column',
                options=[{"label": i, "value": i} for i in available_countries],
                value='Germany'
            ), style={'width': '48%', 'display': 'inline-block'}), #takes 48% of the webpage

        html.Div(
            dcc.Dropdown(
                id='y2axis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods'
            ), style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    dcc.Graph(id='indicator-graphic2')
])

# Function that updates the figure
@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('x1axis-column', 'value'),
     dash.dependencies.Input('y1axis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('x2axis-column', 'value'),
     dash.dependencies.Input('y2axis-column', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name): 
    return {
        'data': [go.Scatter(
            x=df[df['Country Name'] == xaxis_column_name]['Year'].unique(),
            y=df[(df['Indicator Name'] == yaxis_column_name) & (df['Country Name'] == xaxis_column_name)]['Value'],
            text=df[df['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={'title': "Year"},
            yaxis={'title': yaxis_column_name},
            margin={'l': 60, 'b': 40, 't': 10, 'r': 60},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

