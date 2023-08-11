from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback, State
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    # dcc.Dropdown(id='dropdown', value = 1),

    dcc.Textarea(
        id='textarea-state-example',
        value='1',
        style={'width': '100%', 'height': 20},
    ),
    # html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
    # html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}),    

    # dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value')
])

def slow_processing_step(value):
    a_dict = {}
    a_dict['x'] = list(range(10))
    a_dict['y'] = [0 for _ in range(10)]
    if type(int(value)) == int:
        a_dict['y'] = [int(value) * i for i in range(10)]
    df = pd.DataFrame(a_dict)
    return df

def create_figure(df):
    fig = px.scatter(
        df,
        x=df['x'],
        y=df['y'],
        opacity=0.8,
        template='plotly_dark',
        color_continuous_scale= 'Teal', #gradient,
        # hover_name = hover_names,
        # color = cols,
        # size = sizes
    )
    return fig

def create_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns]) ] +
        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(len(df))]
    )
    
# @callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
@callback(Output('intermediate-value', 'data'), Input('textarea-state-example', 'value'))
def clean_data(value):
     # some expensive data processing step
     cleaned_df = slow_processing_step(value)

     # more generally, this line would be
     # json.dumps(cleaned_df)
     return cleaned_df.to_json(date_format='iso', orient='split')

@callback(Output('graph', 'figure'), Input('intermediate-value', 'data'))
def update_graph(jsonified_cleaned_data):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    figure = create_figure(dff)
    return figure

@callback(Output('table', 'children'), Input('intermediate-value', 'data'))
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    table = create_table(dff)
    return table

# @callback(
#     Output('textarea-state-example-output', 'children'),
#     Input('textarea-state-example-button', 'n_clicks'),
#     State('textarea-state-example', 'value')
# )
# def update_output(n_clicks, value):
#     if n_clicks > 0:
#         return 'You have entered: \n{}'.format(value)
    

if __name__ == "__main__":
    app.run(debug=True)
    
