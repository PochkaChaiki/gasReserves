from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table
from gas_reserves.constants import *
import dash_ag_grid as dag

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


def distribution_input(name, id, placeholder):
    initial_data = [
        {'parameter': name, 'distribution': placeholder}
    ]

    # Определяем начальные колонки
    initial_columns = [
        {'headerName': 'Параметр', 'field': 'parameter'},
        {'headerName': 'Распределение', 'field': 'distribution', 'editable': True, 'cellEditor': 'agSelectCellEditor',
         'cellEditorParams': {
             'values': ['Нормальное', 'Равномерное', 'Треугольное', 'Усечённое нормальное']
         },
        },
        {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True, 'hide': True, 'cellDataType': 'number'},
        {'headerName': 'Ст. отклонение', 'field': 'std_dev', 'editable': True, 'hide': True, 'cellDataType': 'number'},
        {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True, 'hide': True, 'cellDataType': 'number'},
        {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True, 'hide': True, 'cellDataType': 'number'},
        {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': True, 'cellDataType': 'number'},
    ]
    return dag.AgGrid(
        id='parameter-table-'+id,
        columnDefs=initial_columns,
        rowData=initial_data,
        defaultColDef={"editable": False, "sortable": False, "filter": False},
        dashGridOptions={
            "rowSelection": "single",
            "stopEditingWhenCellsLoseFocus": True,
            # "domLayout": "autoHeight"
        },
        columnSize='responsiveSizeToFit',
        style={'height': '108px'}
    )
    

def make_input_group(initial_data, id, value=None):
    
    initial_columns = [
        {'headerName': 'Параметр', 'field': 'parameter'},
        {'headerName': 'Значение', 'field': 'value', 'editable': True, 'cellDataType': 'number'},
    ]
    return dag.AgGrid(
        id='parameter-table-'+id,
        columnDefs=initial_columns,
        rowData=initial_data,
        defaultColDef={"editable": False, "sortable": False, "filter": False},
        dashGridOptions={
            "rowSelection": "single",
            "stopEditingWhenCellsLoseFocus": True,
            "domLayout": "autoHeight"
        },
        columnSize='responsiveSizeToFit'
        # style={'height': '100px'}
    )


def get_reserves_input_group(values):
    keys = ['init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'num_of_vars']
    
    data = [{'parameter': varnames[key], 'value': None} for key in keys]
    
    return dbc.Col([
        distribution_input(varnames['area'], "area", "Площадь"),

        distribution_input(varnames['effective_thickness'], "effective_thickness", "Толщина"),

        distribution_input(varnames['porosity_coef'], "porosity_coef", "Пористость"),

        distribution_input(varnames['gas_saturation_coef'], "gas_saturation_coef", "Газонасыщенность"),

        make_input_group(data, 'calcs'),

        dbc.Button("Расчитать", id="calculate_reserves_button", n_clicks=0)
    ])

def get_reserves_main_outputs(values):
    keys_to_omit = {'area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'reserves', 'fin_reservoir_pressure'}

    data = [{'parameter': varnames[key], 'value': None} for key in varnames.keys() if key not in keys_to_omit]

    return dbc.Col([
        make_input_group(data, 'output-calcs')
    ])


ReservesOutputTable = html.Div(id="output_table")

TornadoDiagram = html.Div(id="tornado-diagram" )

IndicatorsDiagram = html.Div(id="indicators-diagram")



def get_production_indicators_inputs(values, indics_values):
    keys_with_indics, keys_to_collapse = ['effective_thickness', 'geo_gas_reserves'], ['filtr_resistance_A', 'filtr_resistance_B', 'critical_temp', 'critical_pressure']
    keys_to_omit = {'permeability', 'pipe_roughness', 'init_num_wells', 'coef_K', 'adiabatic_index', 'lambda_trail', 'lambda_fontain', 'macro_roughness_l'}

    data = [{'parameter': varnamesIndicators[key], 'value': None} for key in list(varnamesIndicators.keys()) if key not in set(keys_to_collapse) and key not in set(keys_with_indics) and key not in keys_to_omit]
    data_keys_to_collapse = [{'parameter': varnamesIndicators[key], 'value': None} for key in keys_to_collapse]
    return dbc.Col([
        distribution_input("Проницаемость, мД", "permeability", "Проницаемость"),

        make_input_group(data, 'indics'),
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
                make_input_group(data_keys_to_collapse, 'indics')
        ]))
        ], id='collapse', is_open=False)
    ])  


PressureOnStages = html.Div([
    dcc.Graph(id='pres-p10'),
    dcc.Graph(id='pres-p50'),
    dcc.Graph(id='pres-p90'),
], id='pressures-graph')
ProdKig = dcc.Graph(id='prod-kig')