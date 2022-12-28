app.layout = html.Div( sidebar, content, style={'backgroundColor': colors['background']}, children =
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
    html.Div(children=[
        html.Label('Soil_Properties'),
        dcc.Dropdown(target)],  
        style={'width': '48%',
             'float': 'center', 
             'display': 'inline-block',
                'color': colors['text']},
                id='dropdown_selecter'
        ),
        dcc.Graph(
            id = 'soil-graph',
            figure = fig
        )
    ])

@app.callback(
    Output('soil-graph', 'figure'),
    Input('dropdown_selecter', 'value'))
def update_figure(selected_value):
    filtered_df = [target == selected_value]

   
    return fig
