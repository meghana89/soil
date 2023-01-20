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

#####################################################
#                    Create the Dash app            #
####################################################

app = dash.Dash(
__name__,
   meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=.7"}],
    external_stylesheets=[dbc.themes.GRID],
)
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

# Create a scatter chart
scatter_chart = dcc.Graph(id="scatter-chart")

# Create a line chart
fig =px.line(df,x=df['date'], y=df['segment1(10-30cm)'],template = 'plotly_dark')
                
line_chart = dcc.Graph(id="line-chart",figure=fig)
# Create a histogram

histogram_plot = dcc.Graph(id='histogram-plot')
histogram_dropdown= html.Div(children=[
                html.Label('Select Histogram Column'),
                dcc.Dropdown(
                id="histogram-dropdown",
                options=[{"label": col, "value": col} for col in df.columns],
                value=df.columns[1]
                        )
                        ]
                    )       
# Create a heatmap
heatmap = html.Div([
                #html.H4('Moisture by DOW'),
                dcc.Graph(id="heatmap"),
               # html.P("Day of Week:"),
                dcc.Checklist(
                    id='Day_filter',
                    options=['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',],
                    value=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                    
                ),
            ])


#creating sidebar to access multiple apps
sidebar = html.Div(
        [
        html.Div(children=[
        html.Label('Select Date Range'),
        dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=df['date'].min(),
                    end_date=df['date'].max()
                        )
                    ]
                ),
            html.Br(),
            html.Div(children=[
            html.Label('Scatter Plot'),
            dcc.Dropdown(
            id="scatter-chart-dropdown",
            options=[{"label": col, "value": col} for col in df.columns],
            value=df.columns[1]
                    )
                    ]
                ),
            html.Br(),
            html.Label('Bin Slider'),
            dcc.Slider(
                id='bin-size-slider',
                min=10,
                max=101,
                value=20,
                marks={i: str(i) for i in range(10, 110, 10)},
                step=None
            ),
             html.Div([histogram_dropdown]),
           ],className='sidebar'
        )
#####################################################
#                   Call Back                       #
#####################################################

# Function to update the line chart
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])

def update_line_chart(start_date, end_date):
    df['date']= pd.to_datetime(df['date'])
    df['month']=df['date'].dt.month
    filtered_df = df[(df['date'] > start_date) & (df['date'] < end_date)]
    fig =px.line(x=filtered_df['date'], y=filtered_df['segment1(10-30cm)'])
    
    return fig
#@app.callback(
    #dash.dependencies.Output("line-chart", "figure"),
    #[dash.dependencies.Input("line-chart-dropdown", "value")]
#)
#def update_line_chart(selected_column):
    # Create a line chart using Plotly
    #df['rolling'] = df[selected_column].rolling(30).mean()
    #figure=px.line(df, x=df.index, y=[selected_column, "rolling"], title=selected_column,template = 'plotly_dark')
    #figure = px.line(df, x=df.index, y=selected_column, title=selected_column)
    #return figure

    # Function to update the scatter chart
@app.callback(
    dash.dependencies.Output("scatter-chart", "figure"),
    [dash.dependencies.Input("scatter-chart-dropdown", "value"),
    dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')]
)
def update_scatter_chart(selected_column,start_date, end_date):
    # Create scatter chart using Plotly
    filtered_df = df[(df['date'] > start_date) & (df['date'] < end_date)]
    figure=px.scatter(x=filtered_df['date'], y=filtered_df[selected_column],  title=selected_column)
    #figure = px.scatter(df, x=df['date'], y=selected_column, title=selected_column)
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

@app.callback(
    Output("heatmap", "figure"), 
    Input("Day_filter", "value"))
def filter_heatmap(df2):
    df2= df.groupby(by = ["DOW", "Hour"]).mean()['segment1(10-30cm)'].unstack()
    fig = px.imshow(df2, y=df2.index,color_continuous_scale='Viridis',text_auto=True, aspect="auto")
    fig.update_xaxes(side="top")
    
    #fig.data[0].update(row_filter='x == "DOW"')
    #fig.show()
    return fig

#####################################################
#             # Create a content layout             #
#####################################################


content = html.Div([
html.Div([
        html.Div([line_chart], className="graph"),
        ],className="container1"),
html.Div([
            html.Div([heatmap], className="graph"),
            html.Div([histogram_plot], className="graph"),   
    ], className="container"),
html.Div([
        html.Div([scatter_chart], className="container1"),
        ],className="graph")
                    ], id="page-content")
 # Create the app layout
app.layout = html.Div([
    html.Div([
# Include the CSS file in the app
    html.Link(
        rel='stylesheet',
        href='/assets/css/style.css'
    ),

    # header
    html.Div(
            [
                html.Div(
                    [
                        html.H1("Soil Moisture Dashboard ", className = "app__header__title",
                        style={'textAlign': 'center', 'color': colors['text']}),
                        html.P(
                            "This app displays charts of soil moisture and other properties over a period",
                            className = "app__header__title--grey",
                            style={
                                        'textAlign': 'center',

                                    }
                        ),
                    ],
                    className = "app__header__desc"
                ), 
            ]
        ),
    dcc.Location(id="url"), sidebar, content])
    ], className = "main")

    
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
