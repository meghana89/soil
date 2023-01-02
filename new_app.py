# Run this app with `python app.py`and
# visit http: //127.0.0.1:8050/ in your web browser.
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.subplots as sp
import plotly.graph_objects as go


app = Dash(
    __name__,
    meta_tags = [{
        "name": "viewport",
        "content": "width=device-width, initial-scale=1"
    }],
)
app.title = "Soil Moisture Dashboard"

server = app.server
#basic styling
SIDEBAR_STYLE= {
    "background-color": "#eee",
  "border": "1px solid #ccc",
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
"background-color": "#3083ff",
}
colors = {"graph_bg": "#082255",
         "graph_line": "#007ACE",
         'background': '#111111',
            'text': '#7FDBFF'}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'background-color' : '#f0f3f7'
}
# assume you have a "long-form" data frame
# see https: //plotly.com/python/px-arguments/ for more options
df = pd.read_csv("soil.csv")
df.set_index(['date'], inplace = True)

figures = [
            px.line(df,x=df.index,y=df['segment1(10-30cm)'],title= "Moisture"),
            px.line(df, x=df.index,y=df['Magna_6 ORP_mV'],title="ORP"),
            px.line(df, x=df.index,y=df['Magna_6 Meteo Relative Humidity'],title="Humidity")
    ]


fig = make_subplots(rows=len(figures), cols=1, shared_yaxes=True)
for i, figure in enumerate(figures):
    for trace in range(len(figure["data"])):
        fig.append_trace(figure["data"][trace], row=i+1, col=1)
        
fig.update_layout(
        template="plotly_dark",
        plot_bgcolor=colors['graph_bg'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        transition_duration=500, 
        showlegend= False,
        yaxis= {"title":"Values"}
    )

#creating sidebar to access multiple apps
sidebar = html.Div(
        [
        html.Div(children=[
        html.Label('Soil_Properties'),
        dcc.Dropdown(df.columns)]
                )
        ],
        style=SIDEBAR_STYLE
        )

#render selected navbar
content = html.Div(
    [
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
        dcc.Graph(
            id = 'soil-graph',
            figure = fig
        )
    ],
    id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

if __name__ == '__main__':
    app.run_server(debug = True)