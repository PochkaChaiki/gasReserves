from dash import html, dcc
import dash_bootstrap_components as dbc
from gas_reserves.constants import *

Layout = html.Div(
    [
        dcc.Store(id="session_storage", storage_type="session"),
        dcc.Store(id="indics_storage", storage_type="local"),
        dcc.Store(id="indics_result_storage", storage_type="session"),
        # dcc.Store(id="indics_input_storage", storage_type="session"),
        html.Header(
        dcc.Tabs(id="tabs-calcs", value="tab-reserves-calcs", children=[
            dcc.Tab(label="Подсчёт запасов", value="tab-reserves-calcs"),
            dcc.Tab(label="Показатели разработки", value="tab-production-indicators")
        ])),
        html.Div(id="tabs-content")
    ])

distribution_options=[
    {"label": "Нормальное", "value": "norm"}, 
    {"label": "Равномерное", "value": "uniform"},
    {"label": "Треугольное", "value": "triang"},
    {"label": "Усечённое нормальное", "value": "truncnorm"},
]

def distribution_input(name, id, placeholder):
    return html.Div([
        dbc.Label(name, id=id, html_for=id+"-select"),
        dbc.Select(distribution_options, id=id+"-select", placeholder=placeholder),
        html.Div(id=id+"-input-div")
    ])

def make_inputgroup(name, id, value):
    return html.Div([
        dbc.Label(name, id=id, html_for=id+"-input"),
        dbc.Input(type="number", id=id+"-input", value=value)
    ])


def get_reserves_input_group(values):
    keys = ['init_reservoir_pressure', 'relative_density', 'reservoir_temp']

    return dbc.Col([
        distribution_input("Площадь, м2", "area", "Площадь"),

        distribution_input("Эффективная газонасыщенная толщина, м", "effective_thickness", "Толщина"),

        distribution_input("Коэффициент пористости, д.е", "porosity_coef", "Пористость"),

        distribution_input("Коэффициент газонасыщенности, д.е.", "gas_saturation_coef", "Газонасыщенность"),

        *tuple([make_inputgroup(varnames[key], key, values.get(key, {'value': 0})['value']) for key in keys]),

        dbc.Button("Расчитать", id="calculate_reserves_button", n_clicks=0)
    ])

def get_reserves_main_outputs(values):
    keys_to_omit = {'area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'reserves'}

    return dbc.Col([
        *tuple([make_inputgroup(varnames[key], key, values.get(key, {'value': 0})['value']) for key in varnames.keys() if key not in keys_to_omit]),
    ])


ReservesOutputTable = html.Div(id="output_table")

TornadoDiagram = html.Div(id="tornado-diagram" )

IndicatorsDiagram = html.Div(id="indicators-diagram")



def get_production_indicators_inputs(values, indics_values):
    keys_with_indics, keys_to_collapse = ['effective_thickness', 'geo_gas_reserves'], ['filtr_resistance_A', 'filtr_resistance_B', 'critical_temp', 'critical_pressure']
    keys_to_omit = {'permeability', 'pipe_roughness', 'init_num_wells', 'coef_K', 'adiabatic_index', 'lambda_trail', 'lambda_fontain', 'macro_roughness_l'}

    
    return dbc.Col([
        distribution_input("Проницаемость, мД", "permeability", "Проницаемость"),

        *tuple([make_inputgroup(varnamesIndicators[key], key+"-indics", values.get(key, {'value': 0})['value']) for key in list(varnamesIndicators.keys()) if key not in set(keys_to_collapse) and key not in set(keys_with_indics) and key not in keys_to_omit]),
        dbc.Button("Дополнительные параметры", id="collapse-button", className="mb-3", color="primary", n_clicks=0),
        dbc.Collapse([
            dbc.Card(dbc.CardBody([
                dbc.Label(varnamesIndicators['effective_thickness'], id="effective_thickness-indics"),
                html.Div([
                    dbc.Label('P10'),   
                    dbc.Input(type='number', id='effective_thickness-indics-input-p10', value=indics_values.get('P10', {'effective_thickness': None})['effective_thickness']),

                    dbc.Label('P50'),
                    dbc.Input(type='number', id='effective_thickness-indics-input-p50', value=indics_values.get('P50', {'effective_thickness': None})['effective_thickness']),

                    dbc.Label('P90'),
                    dbc.Input(type='number', id='effective_thickness-indics-input-p90', value=indics_values.get('P90', {'effective_thickness': None})['effective_thickness']),
                ]),

                dbc.Label(varnamesIndicators['geo_gas_reserves'], id="geo_gas_reserves-indics"),
                html.Div([
                    dbc.Label('P10'),
                    dbc.Input(type='number', id='geo_gas_reserves-indics-input-p10', value=indics_values.get('P10', {'reserves': None})['reserves']),

                    dbc.Label('P50'),
                    dbc.Input(type='number', id='geo_gas_reserves-indics-input-p50', value=indics_values.get('P50', {'reserves': None})['reserves']),

                    dbc.Label('P90'),
                    dbc.Input(type='number', id='geo_gas_reserves-indics-input-p90', value=indics_values.get('P90', {'reserves': None})['reserves']),
                ]),

                *tuple([make_inputgroup(varnamesIndicators[key], key+"-indics", values.get(key, {'value':0})['value']) for key in keys_to_collapse])
        ]))
        ], id='collapse', is_open=False)
    ])  


PressureOnStages = html.Div([
    dcc.Graph(id='pres-p10'),
    dcc.Graph(id='pres-p50'),
    dcc.Graph(id='pres-p90'),
], id='pressures-graph')
ProdKig = dcc.Graph(id='prod-kig')