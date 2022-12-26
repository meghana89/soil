# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df= pd.read_csv("soil.csv")
#df.set_index(['date'],inplace= True)

fig = px.line(df, x="date", y="segment1(10-30cm)")

app.layout = html.Div(children=[
    html.H1(children='Soil Moisture Dashboard'),

    html.Div(children='''
        Dashboard: A simple web application framework for displaying soil moisture data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)