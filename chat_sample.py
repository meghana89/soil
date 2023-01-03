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
   meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=.9"}],
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
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'background-color' : '#f0f3f7'
}
# Load data from a CSV file
df = pd.read_csv("soil.csv")
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


#creating sidebar to access multiple apps
sidebar = html.Div(
        [
        html.Div(children=[
        html.Label('Bar Chart'),
        dcc.Dropdown(
            id="bar-chart-dropdown",
            options=[{"label": col, "value": col} for col in df.columns],
            value="pop"
                    )
                    ]
                ),
           html.Div(children=[
        html.Label('Line Chart'),
        dcc.Dropdown(
            id="line-chart-dropdown",
            options=[{"label": col, "value": col} for col in df.columns],
            value="pop"
                    )
                    ]
                )
           ],
        style=SIDEBAR_STYLE
        )
#####################################################
#                   Call Back                       #
####################################################
# Function to update the bar chart
@app.callback(
    dash.dependencies.Output("bar-chart", "figure"),
    [dash.dependencies.Input("bar-chart-dropdown", "value")]
)
def update_bar_chart(selected_column):
    # Create a bar chart using Plotly
    figure = px.bar(df, x=df.index, y=selected_column, title=selected_column)
    return figure

# Function to update the line chart
@app.callback(
    dash.dependencies.Output("line-chart", "figure"),
    [dash.dependencies.Input("line-chart-dropdown", "value")]
)
def update_line_chart(selected_column):
    # Create a line chart using Plotly
    figure = px.line(df, x=df.index, y=selected_column, title=selected_column)
    return figure
#####################################################
#             # Create a content layout             #
#####################################################

 
content = html.Div([
        
        html.Div([bar_chart], className="graph"),
        html.Div([line_chart], className="graph")
], id="page-content", style=CONTENT_STYLE)
 # Create the app layout
app.layout = html.Div([
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
                        html.H1("WIND SPEED STREAMING", className = "app__header__title",
                        style={'textAlign': 'center', 'color': colors['text']}),
                        html.P(
                            "This app continually queries a database and displays live charts of wind speed and wind direction.",
                            className = "app__header__title--grey",
                            style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    }
                        ),
                    ],
                    className = "app__header__desc",
                ), 
            ]
        ),
    dcc.Location(id="url"), sidebar, content])
# Run the app
if __name__ == '__main__':
    app.run_server()
