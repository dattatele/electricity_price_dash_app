import os
import json
import pandas as pd
import numpy as np
import plotly
from flask import Flask
from pandas_datareader import data as web
from datetime import datetime as db
import xlrd

server = Flask(__name__)


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


#PURCHASE price, Crude Oil, Refinary dataset import

combine_df = pd.read_excel('https://dattatele.github.io/url_data/electric_data/electricity_price.xlsx')

price_df = combine_df.set_index('Year')

#Net generation for all sectors in thousand megawatthours dataset

oil = pd.read_excel('https://dattatele.github.io/url_data/oil_data/oil_transform.xlsx', index_col='Date')

#app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

#Table dataset Refinery Capacity Report

DF_GAPMINDER = pd.read_excel('https://dattatele.github.io/url_data/electric_data/retail_sales_3_columns.xlsx')

DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['Year'] == 2017]
DF_GAPMINDER.loc[0:20]

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [4, 3, 1, 2, 3, 6],
    'z': ['a', 'b', 'c', 'a', 'b', 'c']
})

ROWS = [
    {'a': 'AA', 'b': 1},
    {'a': 'AB', 'b': 2},
    {'a': 'BB', 'b': 3},
    {'a': 'BC', 'b': 4},
    {'a': 'CC', 'b': 5},
    {'a': 'CD', 'b': 6}
]

#Start of app

app = dash.Dash('Hello Guest')


app.layout = html.Div([
    html.Div([
        html.Div([html.H3('Retail Sales of electricity'),
                  html.P('Select table values or filter to check the sale value as per sector'),
        dt.DataTable(
        rows=DF_GAPMINDER.to_dict('records'),

        # optional - sets the order of columns
        columns=sorted(DF_GAPMINDER.columns),

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-gapminder'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-gapminder'
    ),
], style={'width': '61%', 'float': 'right'}, className="container"),


        html.Div([html.H3('Electricity Price'),
                  html.P('Select dropdown list to check the price'),
        dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Electricity Residential Price: U.S. Average cents per kilowatthour',
             'value': 'Electricity Residential Price: U.S. Average cents per kilowatthour'},
            {'label': 'Electricity Commercial Sector Price: U.S. Average cents per kilowatthour',
             'value': 'Electricity Commercial Sector Price: U.S. Average cents per kilowatthour'},
            {'label': 'Electricity Industrial Price: U.S. Average cents per kilowatthour',
             'value': 'Electricity Industrial Price: U.S. Average cents per kilowatthour'}
        ],
        value = 'Electricity Residential Price: U.S. Average cents per kilowatthour'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '35%'})]),


html.Div([
        html.H3('Daily Stock Price'),
        html.P('Enter the symbol name of the organization or company to check stock value'),
        dcc.Input(placeholder='Enter a value...', value='VST', id='my-Input', type = 'text'),
        dcc.Graph(figure={'data': [{'x':[1,2], 'y': [3, 1]}]}, id='my-stock')
],

style={'width': '35%'}),

html.Div([html.H4('Net Generation of Energy in All Sectors'),
          html.P('Select dropdown list to check the energy generation with respect to different energy sources values in thousand megawatthours'),
        dcc.Dropdown(
        id='fuel-dropdown',
        options=[
            {'label': 'All_fuels', 'value': 'all_fuels'},
            {'label': 'coal', 'value': 'coal'},
            {'label': 'Petroleum Liquids', 'value': 'petroleum_liquids'},
            {'label': 'Petroleum Coke', 'value': 'petroleum_coke'},
            {'label': 'Natural Gas', 'value': 'natural_gas'},
            {'label': 'Other Gases', 'value': 'other_gases'},
            {'label': 'Nuclear', 'value': 'Nuclear'},
            {'label': 'Conventional Hydroelectric', 'value': 'conventional_hydroelectric'},
            {'label': 'Wind', 'value': 'Wind'},
            {'label': 'All Utility Scale Solar', 'value': 'All_utility_scale_solar'},
            {'label': 'Geothermal', 'value': 'geothermal'},
            {'label': 'Biomass', 'value': 'biomass'},
            {'label': 'Wood and Wood Derived Fuels', 'value': 'wood_and_wood-_derived_fuels'},
            {'label': 'Other Biomass', 'value': 'Other_biomass'},
            {'label': 'Hydro Electric Pumped Storage', 'value': 'Hydro_electric_pumped_storage'},
            {'label': 'Other', 'value': 'Other'}
        ],
        value='all_fuels'
    ),
    dcc.Graph(id='fuel-graph')
], style={'width': '100%'}),

html.Div([html.H3('Power Plant Status'),
          html.P('Zoom out to expand the cluster and click to see the status'),
          html.Iframe(src="https://dattatele.github.io/url_data/power_plant.html", width="100%", height="500")]),
html.Div([html.H6('Connect with me @LinkdIn/Datta-Tele | @GitHub/dattatele | dattatele.tk',style={'color': '#7F90AC'}),
          html.P('Copyright © Datta Tele 2017', style={'float': 'right','width': '20%'})])])



@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=1, cols=1,
        subplot_titles=('million kilowatthours',),
        shared_xaxes=True)
    marker = {'color': ['#18fff3']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#51ff18'
    fig.append_trace({
        'x': dff['Sector_cross'],
        'y': dff['million kilowatthours'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    #fig['layout']['yaxis3']['type'] = 'log'
    return fig


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    sales_dff = price_df[selected_dropdown_value]
    return {
        'data': [{
            'x': price_df.index,
            'y': sales_dff
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

@app.callback(Output('my-stock', 'figure'), [Input('my-Input', 'value')])
def update_graph(input_value):
    df = web.DataReader(
        input_value,
        'google',
        db(2017, 1, 1),
        db.now()
    )
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

@app.callback(Output('fuel-graph', 'figure'), [Input('fuel-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dff = oil[selected_dropdown_value]
    return {
        'data': [{
            'x': oil.index,
            'y': dff
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.component_suites = [
    'dash_core_components',
    'dash_html_components'
]


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.server.run('0.0.0.0', port=port)
