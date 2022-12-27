# Run this app with `python app.py`and
# visit http: //127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(
    __name__,
    meta_tags = [{
        "name": "viewport",
        "content": "width=device-width, initial-scale=1"
    }],
)
app.title = "Soil Moisture Dashboard"

app_color = {
    "graph_bg": "#082255",
    "graph_line": "#007ACE"
}

# assume you have a "long-form" data frame
# see https: //plotly.com/python/px-arguments/ for more options
df = pd.read_csv("soil.csv")
df.set_index(['date'], inplace = True)

fig = px.line(df, x = df.index, y = "segment1(10-30cm)")
app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H1("WIND SPEED STREAMING", className = "app__header__title"),
                        html.P(
                            "This app continually queries a database and displays live charts of wind speed and wind direction.",
                            className = "app__header__title--grey",
                        ),
                    ],
                    className = "app__header__desc",
                )
            ]
        ),
        dcc.Graph(
            id = 'example-graph',
            figure = fig
        )
    ])
if __name__ == '__main__':
    app.run_server(debug = True)