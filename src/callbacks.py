from dash import html, Input, Output, State, callback, ALL, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import json

from gas_reserves.calculations.reserves_calculations import *
from gas_reserves.calculations.prod_indicators import *


def update_table_columns(cell, rowData):
    # print(cell)
    if cell and cell[0]['colId'] == 'distribution':
        base_columns = [
            {'headerName': 'Параметр', 'field': 'parameter', 'editable': True},
            {'headerName': 'Распределение', 'field': 'distribution', 'editable': True, 'cellEditor': 'agSelectCellEditor',
             'cellEditorParams': {
                 'values': ['Нормальное', 'Равномерное', 'Треугольное', 'Усечённое нормальное']
             },
            #  'cellEditorPopup': True,
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

@callback(
    Output('parameter-table-area', 'columnDefs'),
    Input('parameter-table-area', 'cellValueChanged'),
    State('parameter-table-area', 'rowData')
)
def update_table_area(cell, rowData):
    return update_table_columns(cell, rowData)


@callback(
    Output('parameter-table-effective_thickness', 'columnDefs'),
    Input('parameter-table-effective_thickness', 'cellValueChanged'),
    State('parameter-table-effective_thickness', 'rowData')
)
def update_table_effective_thickness(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-porosity_coef', 'columnDefs'),
    Input('parameter-table-porosity_coef', 'cellValueChanged'),
    State('parameter-table-porosity_coef', 'rowData')
)
def update_table_porosity_coef(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-gas_saturation_coef', 'columnDefs'),
    Input('parameter-table-gas_saturation_coef', 'cellValueChanged'),
    State('parameter-table-gas_saturation_coef', 'rowData')
)
def update_table_gas_saturation_coef(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-permeability', 'columnDefs'),
    Input('parameter-table-permeability', 'cellValueChanged'),
    State('parameter-table-permeability', 'rowData')
)
def update_table_permeability(cell, rowData):
    return update_table_columns(cell, rowData)


def parse_params(dist: str, params: dict):
    if dist=="norm":
        return params.get('mean', 0), { 
            "distribution": dist,
            "params":{
                "loc": params.get('mean', 0),
                "scale": params.get('std_dev', 1),
            },
            "adds": {}
        }
    elif dist=="uniform":
        min_value = params.get('min_value', 0)
        max_value = params.get('max_value', 1)
        loc = min_value
        scale = max_value - min_value
        return (min_value + max_value)/2, { 
            "distribution": dist,
            "params":{
                "loc": loc,
                "scale": scale,
            },
            "adds": {}
        }
    elif dist=="triang":
        min_value = params.get('min_value', 0)
        max_value = params.get('max_value', 1)
        mode = params.get('mode', 0.5)
        loc = min_value
        scale = max_value - min_value
        c = (mode - loc) / scale
        return (min_value+max_value+mode)/3, {
            "distribution": dist,
            "params":{
                "loc": loc,
                "scale": scale,
            },
            "adds":{
                "c": c,
            }
        }
    elif dist=="truncnorm":
        min_value = params.get('min_value', 0)
        max_value = params.get('max_value', 1)
        a = min_value
        b = max_value - min_value
        return params.get('mean', 0), {
            "distribution": dist,
            "params":{
                "loc": params.get('mean', 0),
                "scale": params.get('std_dev', 1),
            },
            "adds":{
                "a": a,
                "b": b,
            }
        }


@callback(
    output=[
        Output("output_table", "children"),
        Output("tornado-diagram", "children"),
        Output("indicators-diagram", "children"),
        Output('parameter-table-output-calcs', 'rowData'),
        # Output("session_storage", "data"),
        Output("indics_storage", "data")
    ],
    
    inputs=[
        Input("calculate_reserves_button", "n_clicks"),
        State('parameter-table-area', 'rowData'),
        State('parameter-table-effective_thickness', 'rowData'),
        State('parameter-table-porosity_coef', 'rowData'),
        State('parameter-table-gas_saturation_coef', 'rowData'),
        State('parameter-table-calcs', 'rowData'),
        State('parameter-table-output-calcs', 'rowData')
    ],
    prevent_initial_call=True)
def calculate_gas_reserves(n_clicks,
                       p_area: list[dict],
                       p_effective_thickness: list[dict],
                       p_porosity_coef: list[dict],
                       p_gas_saturation_coef: list[dict],
                       params: list[dict],
                       add_params: list[dict]):
    if p_area is None or p_area[0]['distribution'] == 'Площадь':
        raise PreventUpdate
    area_value, area = *parse_params(dist_dict[p_area[0]['distribution']], p_area[0]),
    et_value, effective_thickness = *parse_params(dist_dict[p_effective_thickness[0]['distribution']], p_effective_thickness[0]),
    pc_value, porosity_coef = *parse_params(dist_dict[p_porosity_coef[0]['distribution']], p_porosity_coef[0]),
    gsc_value, gas_saturation_coef = *parse_params(dist_dict[p_gas_saturation_coef[0]['distribution']], p_gas_saturation_coef[0]),
    
    stat_params={
        "area": area,
        "effective_thickness": effective_thickness,
        "porosity_coef": porosity_coef,
        "gas_saturation_coef": gas_saturation_coef
    }
    params_df = pd.DataFrame(params)
    params_df = params_df.set_index(['parameter'])

    init_data={
        "area": area_value,
        "effective_thickness": et_value,
        "porosity_coef": pc_value,
        "gas_saturation_coef": gsc_value,
        "init_reservoir_pressure": params_df.loc[varnames['init_reservoir_pressure'], 'value'],
        "relative_density": params_df.loc[varnames['relative_density'], 'value'],
        "reservoir_temp": params_df.loc[varnames['reservoir_temp'], 'value'],
        "num_of_vars": params_df.loc[varnames['num_of_vars'], 'value']
    }

    for el in add_params:
        var = el.get('parameter', None)
        val = el.get('value', None)
        if var is not None and val is not None:
            init_data[reversed_varnames[var]] = val

    
    input_data = make_input_data(pd.DataFrame(init_data, index=["value"], dtype=np.float64))
    stat_data = generate_stats(stat_params, np.int64(init_data['num_of_vars']))
    reserves = calculate_reserves(stat_data, input_data)
    df_affection = calculate_sensitivity(stat_data, input_data, reserves)
    df_affection.rename(index=varnames, inplace=True)
    tornado_fig = plot_tornado(df_affection)
    indicators_fig = plot_indicators(reserves)
    stat_data['geo_gas_reserves'] = reserves
    result_df = pd.DataFrame(
        columns=['P90', 'P50', 'P10'], 
        index=[
            varnames['geo_gas_reserves'], 
            varnames['area'], 
            varnames['effective_thickness'], 
            varnames['porosity_coef'], 
            varnames['gas_saturation_coef']
        ]
    )
    for var in result_df.index:
        result_df.loc[var, 'P90'] = st.scoreatpercentile(stat_data[reversed_varnames[var]], 10)
        result_df.loc[var, 'P50'] = st.scoreatpercentile(stat_data[reversed_varnames[var]], 50)
        result_df.loc[var, 'P10'] = st.scoreatpercentile(stat_data[reversed_varnames[var]], 90)

    result_df.rename(columns=varnames, inplace=True)

    output_data_columns = ['area_volume', 'pore_volume', 'temp_correction', 'critical_pressure',
                           'critical_temp', 'init_overcompress_coef', 'fin_overcompress_coef',
                           'geo_gas_reserves', 'dry_gas_init_reserves']

    output_data_calcs = [{'parameter': varnames[var], 'value': input_data.loc['value', var]} for var in output_data_columns]
    return [dbc.Table.from_dataframe(
                result_df.reset_index(), 
                striped=True, 
                bordered=True, 
                hover=True), 
            dcc.Graph(figure=tornado_fig), 
            dcc.Graph(figure=indicators_fig), 
            output_data_calcs,
    #         output_data[add_params.keys()].to_dict(), 
    #         output_data.to_json(), 
            result_df.to_json(),
    ]



@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    output=[
        [
            Output('pres-p10', 'figure'),
            Output('pres-p50', 'figure'),
            Output('pres-p90', 'figure')
        ],
        Output('prod-kig', 'figure'),
        # dict(
        #     init_pressure=dict(value=Output("init_pressure-indics-input", "value")),
        #     reservoir_temp=dict(value=Output("reservoir_temp-indics-input", "value")),
        #     relative_density=dict(value=Output("relative_density-indics-input", "value")),
        #     init_overcompress_coef=dict(value=Output("init_overcompress_coef-indics-input", "value")),
        #     porosity_coef=dict(value=Output("porosity_coef-indics-input", "value")),
        #     critical_temp=dict(value=Output("critical_temp-indics-input", "value")),
        #     critical_pressure=dict(value=Output("critical_pressure-indics-input", "value")),
        # ),
    ],
    inputs=[
        Input('prod_calcs', 'n_clicks'),
        State("permeability-select", "value"),

        State({"type": "permeability", "index": ALL}, "value"),
        dict(
            init_reservoir_pressure=State("init_reservoir_pressure-indics-input", "value"), 
            reservoir_temp=State("reservoir_temp-indics-input", "value"),
            relative_density=State("relative_density-indics-input", "value"),
            init_overcompress_coef=State("init_overcompress_coef-indics-input", "value"),
            max_depression=State("max_depression-indics-input", "value"),
            # required_whole_gas_production=State("required_whole_gas_production-indics-input", "value"),
            reserve_ratio=State("reserve_ratio-indics-input", "value"),
            operations_ratio=State("operations_ratio-indics-input", "value"),
            porosity_coef=State("porosity_coef-indics-input", "value"),
            gas_saturation_coef=State("gas_saturation_coef-indics-input", "value"),
            avg_well_temp=State("avg_well_temp-indics-input", "value"),
            pipe_diameter=State("pipe_diameter-indics-input", "value"),
            well_height=State("well_height-indics-input", "value"),
            # pipe_roughness=State("pipe_roughness-indics-input", "value"),
            # init_num_wells=State("init_num_wells-indics-input", "value"),
            trail_length=State("trail_length-indics-input", "value"),
            trail_diameter=State("trail_diameter-indics-input", "value"),
            trail_roughness=State("trail_roughness-indics-input", "value"),
            avg_trail_temp=State("avg_trail_temp-indics-input", "value"),
            main_gas_pipeline_pressure=State("main_gas_pipeline_pressure-indics-input", "value"),
            input_cs_temp=State("input_cs_temp-indics-input", "value"),
            # coef_K=State("coef_K-indics-input", "value"),
            efficiency_cs=State("efficiency_cs-indics-input", "value"),
            adiabatic_index=State("adiabatic_index-indics-input", "value"),
            density_athmospheric=State("density_athmospheric-indics-input", "value"),
            viscosity=State("viscosity-indics-input", "value"),
            machines_num=State("machines_num-indics-input", "value"),
            time_to_build=State("time_to_build-indics-input", "value"),
            annual_production=State("annual_production-indics-input", "value"),
            # lambda_trail=State("lambda_trail-indics-input", "value"),
            # lambda_fontain=State("lambda_fontain-indics-input", "value"),
            # macro_roughness_l=State("macro_roughness_l-indics-input", "value"),
            filtr_resistance_A=State("filtr_resistance_A-indics-input", "value"),
            filtr_resistance_B=State("filtr_resistance_B-indics-input", "value"),
            critical_temp=State("critical_temp-indics-input", "value"),
            critical_pressure=State("critical_pressure-indics-input", "value"),
            effective_thickness_p10=State("effective_thickness-indics-input-p10", "value"),
            effective_thickness_p50=State("effective_thickness-indics-input-p50", "value"),
            effective_thickness_p90=State("effective_thickness-indics-input-p90", "value"),
            geo_gas_reserves_p10=State("geo_gas_reserves-indics-input-p10", "value"),
            geo_gas_reserves_p50=State("geo_gas_reserves-indics-input-p50", "value"),
            geo_gas_reserves_p90=State("geo_gas_reserves-indics-input-p90", "value"),
        )
        
    ],
    prevent_initial_call=True
)
def calculate_production_indicators(n_clicks, perm_dist, perm_params, data):
    _, permeability_params = *parse_params(perm_dist, perm_params),
    stat_params = {"permeability": permeability_params}
    stat_perm = generate_stats(stat_params)
    
    permeability_Pinds = st.scoreatpercentile(stat_perm['permeability'], [10, 50, 90])

    init_data = data
    effective_thickness_Pinds = [init_data['effective_thickness_p10'], init_data['effective_thickness_p50'], init_data['effective_thickness_p90']]
    geo_gas_reserves_Pinds = [init_data['geo_gas_reserves_p10'], init_data['geo_gas_reserves_p50'], init_data['geo_gas_reserves_p90']]
    for key in ['effective_thickness_p10', 'effective_thickness_p50', 'effective_thickness_p90', 'geo_gas_reserves_p10', 'geo_gas_reserves_p50', 'geo_gas_reserves_p90']:
        del init_data[key]

    

    prod_kig_fig = None
    pressures_graphs = []
    for eft, ggr, perm, name in zip(effective_thickness_Pinds, geo_gas_reserves_Pinds, permeability_Pinds, ['P10', 'P50', 'P90']):
        init_data['permeability_k'] = perm
        init_data['effective_thickness'] = eft
        init_data['geo_gas_reserves'] = ggr

        input_data = make_init_data_for_prod_indics(pd.DataFrame(init_data, index=["value"]))
        
        result = calculate_indicators(input_data.to_dict('records')[0])
        pressures_df = result[['current_pressure', 'wellhead_pressure', 'ukpg_pressure']]
        pressures_df['downhole_pressure'] = result['current_pressure'] - input_data['max_depression']
        pressures_graphs.append(plot_pressure_on_production_stages(pressures_df, name))
        prod_kig_fig = plot_prod_kig(prod_kig_fig, result[['annual_production', 'kig']], name)
    
    return pressures_graphs, prod_kig_fig