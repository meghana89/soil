import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.subplots as sp
import plotly.graph_objects as go
import os
import pathlib
import numpy as np
import datetime as dt
import dash
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
SIDEBAR_STYLE= {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#3083ff",
    "font-size": "2rem"
}
colors = {"graph_bg": "#082255",
         "graph_line": "#007ACE",
         'background': '#111111',
            'text': '#111'}
CONTENT_STYLE = {
        "position": "relative",
       "margin-left": "8rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'background-color' : '#f0f3f7',
   
}
# Load data from a CSV file
df = pd.read_csv("soil.csv")
df.sort_values(by='date', inplace=True)
df.set_index(['date'], inplace = True)


#####################################################
#                Create a Dropdown                  #
#           menu for selecting a column to          #
#               display on the bar chart            #
####################################################



# Create a bar chart
bar_chart = dcc.Graph(id="bar-chart")

# Create a line chart
line_chart = dcc.Graph(id="line-chart")
# Create a histogram
histogram_plot = dcc.Graph(id='histogram-plot')
histogram_dropdown= html.Div(children=[
                html.Label('Histogram'),
                dcc.Dropdown(
                id="histogram-dropdown",
                options=[{"label": col, "value": col} for col in df.columns],
                value="pop"
                        )
                        ]
                    )       
# Create a scatterplot
#scatter_chart = dcc.Graph(id="scatter-plot")


#creating sidebar to access multiple apps
sidebar = html.Div(
        [
        html.Div(children=[
        html.Label('Line Chart'),
        dcc.Dropdown(
            id="line-chart-dropdown",
            options=[{"label": col, "value": col} for col in df.columns],
            value="pop"
                    )
                    ]
                ),
            html.Br(),
            html.Div(children=[
            html.Label('Bar Chart'),
            dcc.Dropdown(
            id="bar-chart-dropdown",
            options=[{"label": col, "value": col} for col in df.columns],
            value="pop"
                    )
                    ]
                ),
            html.Br(),
            html.Label('Bin Size'),
            dcc.Slider(
                id='bin-size-slider',
                min=1,
                max=50,
                value=30,
                marks={i: str(i) for i in range(1, 51, 5)},
                step=None
            ),
             html.Div([histogram_dropdown]),
           ],
        style=SIDEBAR_STYLE
        )
#####################################################
#                   Call Back                       #
#####################################################

# Function to update the line chart
@app.callback(
    dash.dependencies.Output("line-chart", "figure"),
    [dash.dependencies.Input("line-chart-dropdown", "value")]
)
def update_line_chart(selected_column):
    # Create a line chart using Plotly
    figure = px.line(df, x=df.index, y=selected_column, title=selected_column)
    return figure

    # Function to update the bar chart
@app.callback(
    dash.dependencies.Output("bar-chart", "figure"),
    [dash.dependencies.Input("bar-chart-dropdown", "value")]
)
def update_bar_chart(selected_column):
    # Create a bar chart using Plotly
    figure = px.bar(df, x=df.index, y=selected_column, title=selected_column)
    return figure

# Function to update the histogram
@app.callback(
    dash.dependencies.Output('histogram-plot', 'figure'),
    [dash.dependencies.Input('bin-size-slider', 'value')])

def update_histogram(bin_size):
    # Create a histogram chart using Plotly
    figure=px.histogram(df,x='Magna_6 ORP_mV', nbins=bin_size )

    return figure

#####################################################
#             # Create a content layout             #
#####################################################


content = html.Div([
html.Div([
        
        html.Div([line_chart], className="graph"),
],className="container1"),
html.Div([
            html.Div([bar_chart], className="graph"),
            html.Div([histogram_plot], className="graph")
                    
            #html.Div([scatter_chart], className="graph")
], className="container")], id="page-content", style=CONTENT_STYLE)
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
    app.run_server()
