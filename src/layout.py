from dash import html, dcc
import dash_bootstrap_components as dbc
from gas_reserves.constants import *
import dash_ag_grid as dag

Layout = html.Div(
    [
        dcc.Store(id='persistence_storage', storage_type='session'),
        html.Header(
        dcc.Tabs(id="tabs-calcs", value="tab-reserves-calcs", children=[
            dcc.Tab(label="Подсчёт запасов", value="tab-reserves-calcs"),
            dcc.Tab(label="Показатели разработки", value="tab-production-indicators")
        ])),
        html.Div(id="tabs-content")
    ])

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
    if initial_data is None or initial_data == []:
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
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Ст. отклонение', 'field': 'std_dev', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': True, 'cellDataType': 'number', 
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
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
    

def make_indics_table(name: str, data: dict, id: int, editable: bool = False):
    if data is None or data == {}:
        data = [
            {'parameter': name, 'P90': None, 'P50': None, 'P10': None}
        ]
    columns = [
        {'headerName': 'Параметр', 'field': 'parameter'},
        {'headerName': 'P90', 'field': 'P90', 'cellDataType': 'number', 
            'editable': editable,
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"}
        },
        {'headerName': 'P50', 'field': 'P50', 'cellDataType': 'number', 
            'editable': editable,
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"}
        },
        {'headerName': 'P10', 'field': 'P10', 'cellDataType': 'number', 
            'editable': editable,
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
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
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


def make_reserves_input_group(values: dict):
    keys = ['init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'num_of_vars']

    data = values.get('parameter_table_calcs', None)
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

def make_reserves_main_outputs(values: dict):
    keys_to_omit = {'area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'init_reservoir_pressure', 'relative_density', 'reservoir_temp', 'reserves', 'fin_reservoir_pressure'}

    data = values.get('parameter_table_output_calcs', None)
    if data is None:
        data = [{'parameter': varnames[key], 'value': None} for key in varnames.keys() if key not in keys_to_omit]
    return dbc.Col([
        make_input_group(data, 'output_calcs'),

        dbc.Button("Очистить", id="clear_main_output", n_clicks=0)
    ])

def make_output(values: dict):
    indics_table = []
    if values.get('indics_calcs', None) is not None:
        indics_table = make_indics_table('Параметры', values.get('indics_calcs', None), 'indics'),
    
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
        dbc.Row([dbc.Col(ecdf_diagram), dbc.Col(pdf_diagram)]),
        dbc.Row(tornado_diagram),
    ])



def get_production_indicators_inputs(values: dict):
    keys_with_indics, keys_to_collapse = ['effective_thickness', 'geo_gas_reserves'], ['filtr_resistance_A', 'filtr_resistance_B', 'critical_temp', 'critical_pressure']
    keys_to_omit = {'permeability', 'annual_production', 'pipe_roughness', 'init_num_wells', 'coef_K', 'adiabatic_index', 'lambda_trail', 'lambda_fontain', 'macro_roughness_l', 
                    'density_athmospheric', 'porosity_coef', 'gas_saturation_coef'}

    data: list[dict] = values.get('parameter_table_indics', None)
    keys_not_to_include = set(keys_to_collapse) | set(keys_with_indics) | keys_to_omit
    if data is None:
        data = []
        for key in list(varnamesIndicators.keys()):
            if key not in keys_not_to_include:
                data.append({'parameter': varnamesIndicators[key], 'value': None})
    else:
        keys = [row['parameter'] for row in data]
        keys_to_add = reversed_varnamesIndicators.keys() - set(keys)
        for key in list(reversed_varnamesIndicators.keys()):
            if reversed_varnamesIndicators[key] not in keys_not_to_include and key in keys_to_add:
                data.append({'parameter': key, 'value': None})

    stat_indics_data = values.get('parameter_table_stat_indics', None)
    if stat_indics_data is None:
        stat_indics_data = [{'parameter': varnamesIndicators[key], 'value': None} for key in ('effective_thickness', 'geo_gas_reserves', 'porosity_coef', 'gas_saturation_coef')]
    
    data_to_collapse: list[dict] = values.get('parameter_table_indics_collapse', None)
    if data_to_collapse is None:
        data_to_collapse = [{'parameter': varnamesIndicators[key], 'value': None} for key in keys_to_collapse]
    else:
        keys = [reversed_varnamesIndicators[row['parameter']] for row in data_to_collapse]

        keys_to_add = set(keys_to_collapse) - set(keys)
        for key in keys_to_collapse:
            if key in keys_to_add:
                data_to_collapse.append({'parameter': varnamesIndicators[key], 'value': None})

    return dbc.Col([
        distribution_input(varnamesIndicators['permeability'], "permeability", "Проницаемость", values.get('p_permeability', None)),

        make_input_group(data, 'indics'),
        dbc.Accordion([
            dbc.AccordionItem([
                make_indics_table(None, stat_indics_data, 'stat_indics', True),
                make_input_group(data_to_collapse, 'indics_collapse')
            ], title='Дополнительные параметры')
        ],         
        start_collapsed=True,
        always_open=True),
        dbc.Button('Произвести расчёт', id='prod_calcs', n_clicks=0)
    ])  

def make_prod_calcs_table(values: dict = None):
    
    data = values.get('prod_calcs_table', None)
    if data is None:
        data = [
            [{
                'kig': '',
                'annual_production': '',
                'current_pressure': '',
                'wellhead_pressure': '',
                'n_wells': '',
                'ukpg_pressure': '',
                'cs_power': '',
            }] for i in range(3)
        ]
    columns = [
        {'headerName': shortnamesVarnamesIndicators['year'], 'headerTooltip': displayVarnamesIndicators['year'], 'field': 'year', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['avg_production'], 'headerTooltip':displayVarnamesIndicators['avg_production'], 'field': 'avg_production', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['kig'], 'headerTooltip':displayVarnamesIndicators['kig'], 'field': 'kig', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['annual_production'], 'headerTooltip':displayVarnamesIndicators['annual_production'], 'field': 'annual_production', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['current_pressure'], 'headerTooltip':displayVarnamesIndicators['current_pressure'], 'field': 'current_pressure', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['wellhead_pressure'], 'headerTooltip':displayVarnamesIndicators['wellhead_pressure'], 'field': 'wellhead_pressure', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['n_wells'], 'headerTooltip':displayVarnamesIndicators['n_wells'], 'field': 'n_wells', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['ukpg_pressure'], 'headerTooltip':displayVarnamesIndicators['ukpg_pressure'], 'field': 'ukpg_pressure', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
        {'headerName': shortnamesVarnamesIndicators['cs_power'], 'headerTooltip':displayVarnamesIndicators['cs_power'], 'field': 'cs_power', 'cellDataType': 'number', 
                       'valueFormatter': {"function": "d3.format('.2f')(params.value)"}},
    ]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dag.AgGrid(
                    id=f'prod_calcs_table_{id}',
                    columnDefs=columns,
                    rowData=data[i],
                    defaultColDef={"editable": False, "sortable": False, "filter": False},
                    dashGridOptions={
                        "rowSelection": "single",
                        "stopEditingWhenCellsLoseFocus": True,
                        "domLayout": "autoHeight"
                    },
                    columnSize='responsiveSizeToFit'
                ), 
                title=f'{id} таблица'
            ) for id, i in zip(('P10', 'P50', 'P90'), range(3))
        ],
        start_collapsed=True,
        always_open=True
    )

def make_prod_indics_plots(values: dict):

    pressures_fig = values.get('pressures_on_stages_plot', None)
    pressures_diagram = html.Div(id='pressures-graph')
    if pressures_fig is not None:
        pressures_diagram.children = [
            dcc.Graph(figure=pressures_fig),
        ]

    prod_kig_fig = values.get('prod_kig_plot', None)
    prod_kig_diagram = html.Div(id='prod-kig')
    if prod_kig_fig is not None:
        prod_kig_diagram.children = [
            dcc.Graph(figure=prod_kig_fig),
        ]

    return dbc.Row([
        pressures_diagram,
        prod_kig_diagram
    ])


