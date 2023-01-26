import dash
from dash import dcc, html,  Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.subplots as sp
import plotly.graph_objects as go
#from pycaret.time_series import *
import numpy as np
from datetime import datetime as dt
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq


# This loads all the figure template from dash-bootstrap-templates library,
# adds the templates to plotly.io and makes the first item the default figure template.
templates = [
    "bootstrap",
    "cerulean",
    "cosmo",
    "cyborg",
    "darkly",
    "flatly",
    "journal",
    "litera",
    "lumen",
    "lux",
    "materia",
    "minty",
    "morph",
    "pulse",
    "quartz",
    "sandstone",
    "simplex",
    "sketchy",
    "slate",
    "solar",
    "spacelab",
    "superhero",
    "united",
    "vapor",
    "yeti",
    "zephyr",
]
#template=load_figure_template("lux")
template=load_figure_template(templates[2])
#template=load_figure_template("plotly-dark")
#####################################################
#                    Create the Dash app            #
####################################################

app = dash.Dash(
__name__,
   meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=."}],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.GRID,dbc.icons.FONT_AWESOME],)
app.title = "Soil Moisture Dashboard"
server = app.server
#basic styling

colors = {"graph_bg": "#fff",
         "graph_line": "#007ACE",
         'background': '#fff',
         'text': '#111'}
# Load data from a CSV file

df = pd.read_csv("soil.csv")
df.sort_values(by='date', inplace=True)
#df.set_index(['date'], inplace = True)
df['date']= pd.to_datetime(df['date'])
df['Hour']=df['date'].apply(lambda time: time.hour)
df['Month']=df['date'].apply(lambda time: time.month)
df['Year']=df['date'].apply(lambda time: time.year)
df['DOW']=df['date'].dt.day_name()


#####################################################
#              setup pycaret module                #
####################################################

#####################################################
#                Create Dropdowns                 #
#                     #
####################################################
# Create a wind guage and temp guage
wind_gauge = html.Div([
    daq.Gauge(
        id='wind-gauge',
        #value=5,
        label='Average Wind Speed',
        max=df["Magna_6 Wind Speed (m/s)"].max(),
        min=df["Magna_6 Wind Speed (m/s)"].min(),
        #style={'display': 'block' }
    )
])

temp_gauge = html.Div([
    daq.Gauge(
        id='temp-gauge',
        #value=5,
        label='Average Temp',
        max=df["Magna_6 Wind Speed (m/s)"].max(),
        min=df["Magna_6 Wind Speed (m/s)"].min(),
        #style={'display': 'block' }
    )
])

# Create a violin chart
violin_chart = dcc.Graph(id="violin-chart",style={'height': '100%'})

# Create a line chart
fig =px.line(df,x=df['date'], y=df['segment1(10-30cm)'])
             
line_chart = dcc.Graph(id="line-chart",figure=fig,style={'height': '100%'})
# Create a histogram

histogram_plot = html.Div(children=[
                #html.H4('Histogram'),
                dbc.Navbar(className="navbar bg-dark",children=[
                dbc.DropdownMenuItem([html.Div(children=[
                            html.Label('Bin Slider'),
                            dcc.Slider(
                                            id="bin-size-slider",
                                            min=1,
                                            max=100,
                                            step=1,
                                            value=10,
                                            updatemode="drag",
                                            marks={
                                                20: {"label": "20"},
                                                40: {"label": "40"},
                                                60: {"label": "60"},
                                                80: {"label": "80"},
                                                100: {"label": "100"},
                                            },
                                        )
                            ])
                ]),
                dbc.DropdownMenuItem([html.Div(children=[
                            html.Label('Select ßColumn'),
                            dcc.Dropdown(
                            id="histogram-dropdown",
                            options=[{"label": col, "value": col} for col in df.columns],
                            value=df.columns[1]
                                    )
                            ])
                        ])
                        ]),

                dcc.Graph(id='histogram-plot')
    
                    ]
                )
    
# Create a heatmap
heatmap = html.Div(
    children=[ html.H4('Heatmap of Moisture by DOW'),
                dbc.Navbar(className="navbar bg-dark",
                            children=[
                                    dcc.Checklist(
                                    id='Day_filter',
                                    options=['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',],
                                    value=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                    )
                                ]
                        ),
                dcc.Graph(id="heatmap"),
                    ])


# Navbar
navbar = dbc.Navbar(className="navbar navbar-expand-lg navbar-dark bg-dark",
    children=[
            ## logo/home
            ##dbc.NavItem(html.Img(src=app.get_asset_url("logo.PNG"), height="40px")),
            ## links
             dbc.NavItem(className="nav_item",
                children=[
                dbc.NavLink("App", href="/", className="nav-link active", active=True)
                            ]),
            dbc.NavItem(className="nav_item",
                children=[
                dbc.NavLink("Predictions Api", href="/",className="nav-link", active=False)
                            ]),
                dbc.DropdownMenuItem([html.Div(
                children=[
                            html.Div(html.Label('Select Date Range')),
                            dcc.DatePickerRange(
                                    id='date-picker-range',
                                    start_date=df['date'].min(),
                                    end_date=df['date'].max()
                                        )
                            ])
                                ]),
                dbc.DropdownMenuItem([html.Div(children=[
                            html.Div(html.Label('violin Plot')),
                            dcc.Dropdown(
                            id="violin-chart-dropdown",
                            options=[{"label": col, "value": col} for col in df.columns],
                            value=df.columns[1]
                                    )
                                    ])
                ]),
                
                ])
#####################################################
#                   Call Back                       #
#####################################################
# Function to update Wind Guage
@app.callback(
    dash.dependencies.Output('wind-gauge', 'value'),
    dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date')
)
def update_output(start_date, end_date):
    data = df[(df.date >= start_date) & (df.date <= end_date)]
    value = data['Magna_6 Wind Speed (m/s)'].mean()
    return value
# Function to update temp Guage
@app.callback(
    dash.dependencies.Output('temp-gauge', 'value'),
    dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date')
)
def update_output(start_date, end_date):
    data = df[(df.date >= start_date) & (df.date <= end_date)]
    value = data["Magna_6 Meteo Ambient Temperature (C)"].mean()
    return value

  
# Function to update the line chart
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])

def update_line_chart(start_date, end_date):
    df['date']= pd.to_datetime(df['date'])
    df['month']=df['date'].dt.month
    filtered_df = df[(df['date'] > start_date) & (df['date'] < end_date)]
    fig =px.line(filtered_df,x=filtered_df['date'], y=filtered_df['segment1(10-30cm)'],template=template, title="Moisture Content")
    
    return fig


# Function to update the scatter chart
@app.callback(
    dash.dependencies.Output("violin-chart", "figure"),
    [dash.dependencies.Input("violin-chart-dropdown", "value")]
   # dash.dependencies.Input('date-picker-range', 'start_date'),
       # dash.dependencies.Input('date-picker-range', 'end_date')]
)
def update_violin_chart(selected_column):
    # Create scatter chart using Plotly
    #filtered_df = df[(df['date'] > start_date) & (df['date'] < end_date)]
    #figure=px.scatter(filtered_df,x=filtered_df['date'], y=filtered_df[selected_column],  title=selected_column, )
    figure = px.violin(df, y=[selected_column], box=True, # draw box plot inside the violin
    #points='all',  can be 'outliers', or False
               )
    return figure

# Function to update the histogram
@app.callback(
        dash.dependencies.Output('histogram-plot', 'figure'),
        [dash.dependencies.Input('histogram-dropdown', 'value'),
        #dash.dependencies.Input('date-picker-range', 'start_date'),
        #dash.dependencies.Input('date-picker-range', 'end_date'),
        dash.dependencies.Input('bin-size-slider', 'value')]
)
        #,
        #Input('bin-size-slider', 'value'))

    
def update_histogram(value, bin_size):
    # Create a histogram chart using Plotly
    figure = go.Figure(data=[go.Histogram(x=df[value], nbinsx=bin_size)])
    #figure=px.histogram(df,x=[value],nbinsx=bin_size, template = 'plotly_dark' )
    return figure


# Function to update the heatmap
@app.callback(
    dash.dependencies.Output("heatmap", "figure"), 
    dash.dependencies.Input("Day_filter", "value"))
def filter_heatmap(df2):
    df2= df.groupby(by = ["DOW", "Hour"]).mean()['segment1(10-30cm)'].unstack()
    fig = px.imshow(df2, y=df2.index, aspect="auto")
    fig.update_xaxes(side="top")
    
    
    return fig

#####################################################
#             # Create a content layout             #
#####################################################


content = html.Div(
        children=[
                html.Div(
                    children=[
                        html.Div([
                        html.Div([wind_gauge,temp_gauge], className='col-2'),
                       #html.Div([temp_gauge], className='col-3'),
                        html.Div([line_chart],className="col-10")
                        ], className='row'),
                        html.Div(
                            children=[
                                html.Div([
                                    html.Div([histogram_plot], className='col-6'),
                                    html.Div([violin_chart], className='col-6')
                                    ],className='row'),
                                
                                ]),
                                html.Div([heatmap],className="row")
                        ],className="container1"),
                ])

# Create the app layout
app.layout = html.Div(
        children=[
            # Include the CSS file in the app
                html.Link(rel='stylesheet', href='/assets/css/style.css'),
                # header
                html.Div(
                children=[
                        html.Div(
                         children= [
                                    html.H1("Soil Moisture Dashboard"),
                                    html.H3("This app displays charts of soil moisture and other properties over a period", className="app__header__desc"),
                                ],
                            ), 
                        dcc.Location(id="url"), navbar, content
                        ])
                    ],className = "main"
                    )
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
