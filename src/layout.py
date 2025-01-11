from dash import html, dcc
import dash_bootstrap_components as dbc
from gas_reserves.constants import *
import dash_ag_grid as dag
import pandas as pd

Layout = html.Div(
    [
        # dcc.Store(id='main_storage', storage_type='session'),
        dcc.Store(id="calcs_storage", storage_type="session"),
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

ReservesOutputTable = html.Div(id="output_table")

TornadoDiagram = html.Div(id="tornado-diagram" )

ECDFDiagram = html.Div(id="ecdf-diagram")
PDFDiagram = html.Div(id="pdf-diagram")

PressureOnStages = html.Div(dcc.Graph(id='pressures-graph'))

ProdKig = dcc.Graph(id='prod-kig')


def update_table_columns(cell, rowData):
    if cell and cell[0]['colId'] == 'distribution':
        base_columns = [
            {'headerName': 'Параметр', 'field': 'parameter', 'editable': True},
            {'headerName': 'Распределение', 'field': 'distribution', 'editable': True, 'cellEditor': 'agSelectCellEditor',
             'cellEditorParams': {
                 'values': ['Нормальное', 'Равномерное', 'Треугольное', 'Усечённое нормальное']
             },
            }
        ]

        additional_columns = []
        for row in rowData:
            distribution = row.get('distribution', 'Нормальное')
            if distribution == 'Нормальное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                    
                ]
            elif distribution == 'Треугольное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                ]
            elif distribution == 'Равномерное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                ]
            elif distribution == 'Усечённое нормальное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True, 'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': True, 'cellDataType': 'number'},
                ]

        return base_columns + additional_columns


def distribution_input(name, id, placeholder, initial_data=None):
    initial_columns = []
    if initial_data is None or initial_data == {}:
        initial_data = [
            {'parameter': name, 'distribution': placeholder}
        ]
        initial_columns = [
            {'headerName': 'Параметр', 'field': 'parameter', 'editable': False},
            {'headerName': 'Распределение', 'field': 'distribution', 'editable': True, 'cellEditor': 'agSelectCellEditor',
             'cellEditorParams': {
                 'values': ['Нормальное', 'Равномерное', 'Треугольное', 'Усечённое нормальное']
             },
            },
            {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
            {'headerName': 'Ст. отклонение', 'field': 'std_dev', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
            {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
            {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
            {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        ]
    else:
        initial_columns = update_table_columns([{'colId': 'distribution'}], initial_data)

    return dag.AgGrid(
        id='parameter-table-'+id,
        columnDefs=initial_columns,
        rowData=initial_data,
        defaultColDef={"editable": False, "sortable": False, "filter": False},
        dashGridOptions={
            "rowSelection": "single",
            "stopEditingWhenCellsLoseFocus": True,
        },
        columnSize='responsiveSizeToFit',
        style={'height': '108px'}
    )
    

def make_indics_table(name, data, id):
    if data is None or data == {}:
        data = [
            {'parameter': name, 'P90': None, 'P50': None, 'P10': None}
        ]
    columns = [
        {'headerName': 'Параметр', 'field': 'parameter'},
        {'headerName': 'P90', 'field': 'P90', 'cellDataType': 'number', 
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"}
        },
        {'headerName': 'P50', 'field': 'P50', 'cellDataType': 'number', 
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"}
        },
        {'headerName': 'P10', 'field': 'P10', 'cellDataType': 'number', 
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"}
        },
    ]
    return dag.AgGrid(
        id='parameter-table-'+id,
        columnDefs=columns,
        rowData=data,
        defaultColDef={"editable": False, "sortable": False, "filter": False},
        dashGridOptions={
            "domLayout": "autoHeight",
            "rowSelection": "single",
        },
        columnSize='responsiveSizeToFit',
    )


def make_input_group(initial_data, id):
    
    initial_columns = [
        {'headerName': 'Параметр', 'field': 'parameter'},
        {'headerName': 'Значение', 'field': 'value', 'editable': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
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
    )


def get_reserves_input_group(values):


    keys = ['init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'num_of_vars']

    data = values.get('params', None)
    if data is None:    
        data = [{'parameter': varnames[key], 'value': None} for key in keys]

    return dbc.Col([
        distribution_input(varnames['area'], "area", "Площадь", values.get('p_area', None)),

        distribution_input(varnames['effective_thickness'], "effective_thickness", "Толщина", values.get('p_effective_thickness', None)),

        distribution_input(varnames['porosity_coef'], "porosity_coef", "Пористость", values.get('p_porosity_coef', None)),

        distribution_input(varnames['gas_saturation_coef'], "gas_saturation_coef", "Газонасыщенность", values.get('p_gas_saturation_coef', None)),

        make_input_group(data, 'calcs'),

        dbc.Button("Расчитать", id="calculate_reserves_button", n_clicks=0)
    ])

def get_reserves_main_outputs(values):
    keys_to_omit = {'area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'reserves', 'fin_reservoir_pressure'}

    data = values.get('add_params', None)
    if data is None:
        data = [{'parameter': varnames[key], 'value': None} for key in varnames.keys() if key not in keys_to_omit]
    return dbc.Col([
        make_input_group(data, 'output-calcs')
    ])




def get_production_indicators_inputs(values, indics_values):
    keys_with_indics, keys_to_collapse = ['effective_thickness', 'geo_gas_reserves'], ['filtr_resistance_A', 'filtr_resistance_B', 'critical_temp', 'critical_pressure']
    keys_to_omit = {'permeability', 'annual_production', 'pipe_roughness', 'init_num_wells', 'coef_K', 'adiabatic_index', 'lambda_trail', 'lambda_fontain', 'macro_roughness_l', 
                    'density_athmospheric'}

    values_input_df = pd.DataFrame(None)
    if values.get('params', None) is not None:
        values_input_df = pd.DataFrame(values['params']).set_index('parameter')

    
    if values.get('add_params', None) is not None:
        values_input_df = pd.concat([values_input_df, pd.DataFrame(values['add_params']).set_index('parameter')] )

    data = []
    for key in list(varnamesIndicators.keys()):
        if key not in set(keys_to_collapse) and key not in set(keys_with_indics) and key not in keys_to_omit:
            if varnamesIndicators[key] in values_input_df.index:
                data.append({'parameter': varnamesIndicators[key], 'value': values_input_df.loc[varnamesIndicators[key], 'value']})
            else:
                data.append({'parameter': varnamesIndicators[key], 'value': None})


    data_keys_to_collapse = []
    for key in keys_to_collapse:
        if varnamesIndicators[key] in values_input_df.index:
            data_keys_to_collapse.append({'parameter': varnamesIndicators[key], 'value': values_input_df.loc[varnamesIndicators[key], 'value']})
        else:
            data_keys_to_collapse.append({'parameter': varnamesIndicators[key], 'value': None})

    effective_thickness_data = None
    for el in indics_values:
        if el['parameter'] == varnames['effective_thickness']:
            effective_thickness_data = [el]
            break

    geo_gas_reserves_data = None
    for el in indics_values:
        if el['parameter'] == varnames['geo_gas_reserves']:
            geo_gas_reserves_data = [el]
            break



    return dbc.Col([
        distribution_input("Проницаемость, мД", "permeability", "Проницаемость"),

        make_input_group(data, 'indics'),
        dbc.Button("Дополнительные параметры", id="collapse-button", className="mb-3", color="primary", n_clicks=0),
        dbc.Collapse([
            dbc.Card(dbc.CardBody([
                make_indics_table('eff', effective_thickness_data, 'effective_thickness-indics'),
                make_indics_table('geo', geo_gas_reserves_data, 'geo_gas_reserves-indics'),
                make_input_group(data_keys_to_collapse, 'indics-collapse')
            ]))
        ], id='collapse', is_open=False),
        dbc.Button('Произвести расчёт', id='prod_calcs', n_clicks=0)
    ])  

def make_prod_calcs_table(data=None):
    if data is None:
        data = [{
            'kig': '',
            'annual_production': '',
            'current_pressure': '',
            'wellhead_pressure': '',
            'n_wells': '',
            'ukpg_pressure': '',
            'cs_power': '',
        }]
    columns = [
        {'headerName': displayVarnamesIndicators['kig'], 'field': 'kig', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': displayVarnamesIndicators['annual_production'], 'field': 'annual_production', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': displayVarnamesIndicators['current_pressure'], 'field': 'current_pressure', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': displayVarnamesIndicators['wellhead_pressure'], 'field': 'wellhead_pressure', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': displayVarnamesIndicators['n_wells'], 'field': 'n_wells', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': displayVarnamesIndicators['ukpg_pressure'], 'field': 'ukpg_pressure', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': displayVarnamesIndicators['cs_power'], 'field': 'cs_power', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
    ]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dag.AgGrid(
                    id=f'prod_calcs_table_{id}',
                    columnDefs=columns,
                    rowData=data,
                    defaultColDef={"editable": False, "sortable": False, "filter": False},
                    dashGridOptions={
                        "rowSelection": "single",
                        "stopEditingWhenCellsLoseFocus": True,
                        "domLayout": "autoHeight"
                    },
                    columnSize='responsiveSizeToFit'
                ), 
                title=f'{id} таблица'
            ) for id in ('P10', 'P50', 'P90')
        ],
        start_collapsed=True,
        always_open=True
    )

        


