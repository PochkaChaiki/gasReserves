from src.layouts.components import *
from src.gas_reserves.constants import *
import dash_bootstrap_components as dbc

def get_production_indicators_inputs(values: dict):
    keys_with_indics = ['effective_thickness', 'geo_gas_reserves']
    keys_to_collapse = ['filtr_resistance_A','filtr_resistance_B',
                        'critical_temp', 'critical_pressure']

    keys_to_omit = {'permeability', 'annual_production', 'pipe_roughness',
                    'init_num_wells', 'coef_K', 'adiabatic_index', 'lambda_trail',
                    'lambda_fontain', 'macro_roughness_l', 'density_athmospheric',
                    'porosity_coef', 'gas_saturation_coef', 'trail_roughness'}

    data: list[dict] = values.get('parameter_table_indics', [])
    keys_not_to_include = set(keys_to_collapse) | set(keys_with_indics) | keys_to_omit
    if len(data) == 0:
        for key in list(varnamesIndicators.keys()):
            if key not in keys_not_to_include:
                data.append({'parameter': varnamesIndicators[key], 'value': None})
    else:
        keys = [row['parameter'] for row in data]
        keys_to_add = reversed_varnamesIndicators.keys() - set(keys)
        for key in list(reversed_varnamesIndicators.keys()):
            if (reversed_varnamesIndicators[key] not in keys_not_to_include
                    and key in keys_to_add):
                data.append({'parameter': key, 'value': None})

    stat_indics_data = values.get('parameter_table_stat_indics', None)
    if stat_indics_data is None:
        stat_indics_data = [
            {'parameter': varnamesIndicators[key], 'value': None} for key in
                ('effective_thickness', 'geo_gas_reserves',
                 'porosity_coef', 'gas_saturation_coef')
        ]

    data_to_collapse: list[dict] = values.get('parameter_table_indics_collapse', [])
    if len(data_to_collapse) == 0:
        data_to_collapse = [
            {'parameter': varnamesIndicators[key], 'value': None}
            for key in keys_to_collapse
        ]
    else:
        keys = [
            reversed_varnamesIndicators[row['parameter']]
            for row in data_to_collapse
        ]

        keys_to_add = set(keys_to_collapse) - set(keys)
        for key in keys_to_collapse:
            if key in keys_to_add:
                data_to_collapse.append(
                    {'parameter': varnamesIndicators[key], 'value': None}
                )

    return dbc.Col([
        distribution_input(varnamesIndicators['permeability'],
                           "permeability",
                           "Проницаемость",
                           values.get('p_permeability', None)),

        make_input_group(data, 'indics'),
        dbc.Accordion([
            dbc.AccordionItem([
                make_indics_table(None,
                                  stat_indics_data,
                                  'stat_indics',
                                  True),
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
            }] for _ in range(3)
        ]
    columns = [
        {
            'headerName': shortnamesVarnamesIndicators['year'],
            'headerTooltip': displayVarnamesIndicators['year'],
            'field': 'year',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['avg_production'],
            'headerTooltip': displayVarnamesIndicators['avg_production'],
            'field': 'avg_production',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['kig'],
            'headerTooltip': displayVarnamesIndicators['kig'],
            'field': 'kig',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['annual_production'],
            'headerTooltip': displayVarnamesIndicators['annual_production'],
            'field': 'annual_production',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['current_pressure'],
            'headerTooltip': displayVarnamesIndicators['current_pressure'],
            'field': 'current_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['wellhead_pressure'],
            'headerTooltip': displayVarnamesIndicators['wellhead_pressure'],
            'field': 'wellhead_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['downhole_pressure'],
            'headerTooltip': displayVarnamesIndicators['downhole_pressure'],
            'field': 'downhole_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['n_wells'],
            'headerTooltip': displayVarnamesIndicators['n_wells'],
            'field': 'n_wells',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['ukpg_pressure'],
            'headerTooltip': displayVarnamesIndicators['ukpg_pressure'],
            'field': 'ukpg_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': shortnamesVarnamesIndicators['cs_power'],
            'headerTooltip': displayVarnamesIndicators['cs_power'],
            'field': 'cs_power',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
    ]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dag.AgGrid(
                    id = f'prod_calcs_table_{profile_id}',
                    columnDefs = columns,
                    rowData = data[i],
                    defaultColDef = {
                        "editable": False,
                        "sortable": False,
                        "filter": False
                    },
                    dashGridOptions = {
                        "rowSelection": "single",
                        "stopEditingWhenCellsLoseFocus": True,
                        "domLayout": "autoHeight"
                    },
                    columnSize = 'responsiveSizeToFit'
                ),
                title = f'{profile_id} таблица'
            ) for profile_id, i in zip(('P10', 'P50', 'P90'), range(3))
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


def render_production_indicators(data):
    return html.Div([
        dbc.Row([
            dbc.Col(get_production_indicators_inputs(data)),
            dbc.Col(make_prod_calcs_table(data)),
        ]),
        dbc.Row([
            make_prod_indics_plots(data)
        ])
    ])
