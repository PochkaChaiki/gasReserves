from src.layouts.components import *
from src.constants import *


import dash_bootstrap_components as dbc
from dash import html, dcc

def make_reserves_input_group(values: dict):
    keys = ['init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'num_of_vars']

    data = values.get('parameter_table_calcs', None)
    if data is None:    
        data = [{'parameter': VARNAMES[key], 'value': None} for key in keys]

    return dbc.Col([
        distribution_input(VARNAMES['area'],
                           "area",
                           "Площадь",
                           values.get('p_area', None)),

        distribution_input(VARNAMES['effective_thickness'],
                           "effective_thickness",
                           "Толщина",
                           values.get('p_effective_thickness', None)),

        distribution_input(VARNAMES['porosity_coef'],
                           "porosity_coef",
                           "Пористость",
                           values.get('p_porosity_coef', None)),

        distribution_input(VARNAMES['gas_saturation_coef'],
                           "gas_saturation_coef",
                           "Газонасыщенность",
                           values.get('p_gas_saturation_coef', None)),

        html.Div(make_input_group(data, 'calcs'), className='my-2'),

        dbc.Button("Произвести расчёт", id="calculate_reserves_button", n_clicks=0, class_name='my-2')
    ])

def make_reserves_main_outputs(values: dict):
    keys_to_omit = {'area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef',
                    'init_reservoir_pressure', 'relative_density', 'reservoir_temp',
                    'reserves', 'fin_reservoir_pressure'}

    data = values.get('parameter_table_output_calcs', None)
    if data is None:
        data = [{'parameter': VARNAMES[key], 'value': None} for key in VARNAMES.keys() if key not in keys_to_omit]
    return dbc.Col([
        html.Div(make_input_group(data, 'output_calcs'), className='mb-2'),

        dbc.Button("Очистить", id="clear_main_output", n_clicks=0, class_name='my-2')
    ])

def make_output(values: dict):
    indics_table = []
    if values.get('indics_calcs', None) is not None:
        indics_table = make_indics_table('Параметры', values.get('indics_calcs', []), 'indics'),
    
    output_table = html.Div(indics_table, id="output-table")

    tornado_fig = values.get('tornado_diagram', None)
    tornado_diagram = html.Div(id="tornado-diagram")
    if tornado_fig is not None:
        tornado_diagram.children = [
            dcc.Graph(figure=tornado_fig),
        ]

    ecdf_fig = values.get('ecdf_plot', None)
    ecdf_diagram = html.Div(id="ecdf-diagram")
    if ecdf_fig is not None:
        ecdf_diagram.children = [
            dcc.Graph(figure=ecdf_fig),
        ]

    pdf_fig = values.get('pdf_plot', None)
    pdf_diagram = html.Div(id="pdf-diagram")
    if pdf_fig is not None:
        pdf_diagram.children = [
            dcc.Graph(figure=pdf_fig),
        ]

    return dbc.Col([
        dbc.Row(output_table),
        dbc.Row([dbc.Col(ecdf_diagram), dbc.Col(pdf_diagram)], class_name='table-responsive'),
        dbc.Row(tornado_diagram),
    ])


def render_reserves_calcs(data):
    return html.Div([
        dbc.Row([
            make_reserves_input_group(data),
            make_reserves_main_outputs(data),
        ], class_name='my-2'),
        dbc.Row([make_output(data)], class_name='my-2'),
    ])
