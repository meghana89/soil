import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime
import plotly.offline as pyo

# initiate the app
app = dash.Dash()

colors = {"background":"#111111", "text":"#7FDBFF"}

## read the file 
df = pd.read_csv("soil.csv")
df['date']= pd.to_datetime(df['date'])
df['Hour']=df['date'].apply(lambda time: time.hour)
df['Month']=df['date'].apply(lambda time: time.month)
df['Year']=df['date'].apply(lambda time: time.year)
df['DOW']=df['date'].dt.day_name()

#heatmap cant accept pandaconvert z has to be python list so we are converting it to it


app.layout = html.Div([
    html.H4('Moisture by DOW'),
    dcc.Graph(id="graph"),
    html.P("Day of Week:"),
    dcc.Checklist(
        id='Day_filter',
        options=['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',],
        value=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        
    ),
])


@app.callback(
    Output("graph", "figure"), 
    Input("Day_filter", "value"))
def filter_heatmap(df2):
    df2= df.groupby(by = ["DOW", "Hour"]).mean()['segment1(10-30cm)'].unstack()
    fig = px.imshow(df2, y=df2.index,color_continuous_scale='Viridis',text_auto=True, aspect="auto")
    fig.update_xaxes(side="top")
    
    #fig.data[0].update(row_filter='x == "DOW"')
    #fig.show()
    return fig


app.run_server(debug=True)
#run the app 
if __name__=="__main__":
    app.run_server(debug=True)