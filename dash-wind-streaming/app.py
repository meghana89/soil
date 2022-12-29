import os
import pathlib
import numpy as np
import datetime as dt
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from scipy.stats import rayleigh
#from db.api import get_wind_data, get_wind_data_by_id
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.subplots as sp
import plotly.graph_objects as go

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=.9"}],
    external_stylesheets=[dbc.themes.GRID],
)
app.title = "Soil Moisture Dashboard"

server = app.server 

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",


}
colors = {"graph_bg": "#082255",
         "graph_line": "#007ACE",
         'background': '#111111',
            'text': '#7FDBFF'}
#load data
df = pd.read_csv("../soil.csv")
df.set_index(['date'], inplace = True)
fig1= px.line(df,x=df.index,y='segment1(10-30cm)'),

#render content

content = html.Div(
    [
        # header
        html.Div(
            [
                #title
                html.Div(
                    [
                        html.H3("SOIL MOISTURE STREAMING", className="app__header__title"),
                        html.P(
                            "This app continually queries a database and displays live charts of wind speed and wind direction.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                #source and logo
                html.Div(
                    [
                        html.A(
                            html.Button("SOURCE CODE", className="link-button"),
                            href="https://github.com/ayor213/soil",
                        ),
                        html.A(
                            html.Img(
                                src=app.get_asset_url("dash-new-logo.png"),
                                className="app__menu__img",
                            ),
                            href="https://plotly.com/dash/",
                        ),
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                # first column
                html.Div(
                    [
                        html.Div(
                            [html.H6("Soil Moisture", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="wind-speed",
                            figure= dict(
                                        layout=dict(
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                        ),
                            ),
                        )
                      
                    ],
                    className="two-thirds column wind__speed__container",
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "second graph",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Slider(
                                            id="bin-slider",
                                            min=1,
                                            max=60,
                                            step=1,
                                            value=20,
                                            updatemode="drag",
                                            marks={
                                                20: {"label": "20"},
                                                40: {"label": "40"},
                                                60: {"label": "60"},
                                            },
                                        )
                                    ],
                                    className="slider",
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="bin-auto",
                                            options=[
                                                {"label": "Auto", "value": "Auto"}
                                            ],
                                            value=["Auto"],
                                            inputClassName="auto__checkbox",
                                            labelClassName="auto__label",
                                        ),
                                        html.P(
                                            "# of Bins: Auto",
                                            id="bin-size",
                                            className="auto__p",
                                        ),
                                    ],
                                    className="auto__container",
                                ),
                                dcc.Graph(
                                    id="wind-histogram",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "WIND DIRECTION", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="wind-direction",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container")



app.layout = html.Div([content])
if __name__ == "__main__":
    app.run_server(debug=True)
