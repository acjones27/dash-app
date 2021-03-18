# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_fruit = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig_fruit = px.bar(df_fruit, x="Fruit", y="Amount", color="City", barmode="group")

df_states = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

markdown_text = '''
    ### Dash and Markdown
    
    Dash apps can be written in Markdown.
    Dash uses the [CommonMark](http://commonmark.org/)
    specification of Markdown.
    Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
    if this is your first introduction to Markdown!
    '''

df_pop = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig_scatter = px.scatter(df_pop, x="gdp per capita", y="life expectancy",
                         size="population", color="continent", hover_name="country",
                         log_x=True, size_max=60)

names = ["Anna", "Jaime", "Carl"]
dates = ["2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06"]
values = [[1, 2, 3, 4, 5, 6], [2, 2, 2, 2, 2, 2], [1, 2, 3, 3, 2, 1]]
df = pd.DataFrame.from_records(data=np.array(values).T.tolist(), index=dates, columns=names)
df = df.stack().reset_index(1)
df.columns = ["Names", "Values"]

app.layout = html.Div([

        dcc.Markdown('''
            # Anna's Dashboard
            Dash: A web application framework for Python.
        ''', style={"textAlign": "center"}),

        dcc.Markdown(children=markdown_text),

        html.Div([
            "Input: ",
            dcc.Input(id='my-input', value='initial value', type='text')]),
        html.Br(),
        html.Div(id='my-output'),

        dcc.Graph(
            id='example-graph',
            figure=fig_fruit
        ),

        dcc.Graph(
            id='life-exp-vs-gdp',
            figure=fig_scatter
        ),

    html.Label('Filter by Name'),
    dcc.Dropdown(id='filter-input', options=[
        {'label': i, 'value': i} for i in df.Names.unique()
    ], multi=True, placeholder='Filter by Name...'),

    html.Div(id='df-output'),

    dcc.Markdown('''
            #### Numbers per person
        '''),
    dcc.Graph(
        id='df-graph',
    ),
])

@app.callback(
    Output(component_id='df-output', component_property='children'),
    Output(component_id="my-output", component_property="children"),
    Output(component_id='df-graph', component_property='figure'),
    Input(component_id='filter-input', component_property='value'),
)
def update_df(filter_value):

    if not filter_value:
        dff = df
    else:
        dff = df[df["Names"].isin(filter_value)]
    tab = dash_table.DataTable(
        id='df_table',
        columns=[{"name": i, "id": i} for i in dff.columns],
        data=dff.to_dict('records'),
        fixed_rows={'headers': True},
        page_action='none',
        style_cell={'textAlign': 'left'},
        style_table={'height': '300px',
                     'overflowY': 'auto',
                     "width": "50%",
                     'fontSize': 14,
                     'font-family':'sans-serif'}
    )
    var = 'Output: {}'.format(filter_value)
    plot = px.line(dff, x=dff.index, y="Values", color="Names")
    return tab, var, plot

if __name__ == '__main__':
    app.run_server(debug=True)
