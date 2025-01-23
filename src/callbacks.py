from dash import Input, Output, State, callback, ALL, dcc, ctx, no_update
from dash.exceptions import PreventUpdate

from layout import *
from gas_reserves.plot import *
from gas_reserves.calculations.reserves_calculations import *
from gas_reserves.calculations.prod_indicators import *

from utils import *

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

@callback(
    Output('parameter-table-output_calcs', 'rowData', allow_duplicate=True),
    Input('clear_main_output', 'n_clicks'),
    State('parameter-table-output_calcs', 'rowData'),
    prevent_initial_call=True
)
def clear_main_output(n_clicks, rowData):
    if rowData is None or rowData == []:
        return rowData
    
    for row in rowData:
        row['value'] = None
    return rowData

@callback(
    output=[
        Output('output-table', "children"),
        Output('tornado-diagram', "children"),
        Output('ecdf-diagram', "children"),
        Output('pdf-diagram', 'children'),
        Output('parameter-table-output_calcs', 'rowData', allow_duplicate=True),
        Output('persistence_storage', 'data', allow_duplicate=True),
    ],
    
    inputs=[
        Input("calculate_reserves_button", "n_clicks"),
        State('parameter-table-area', 'rowData'),
        State('parameter-table-effective_thickness', 'rowData'),
        State('parameter-table-porosity_coef', 'rowData'),
        State('parameter-table-gas_saturation_coef', 'rowData'),
        State('parameter-table-calcs', 'rowData'),
        State('parameter-table-output_calcs', 'rowData'),
        State('persistence_storage', 'data'),
    ],
    prevent_initial_call=True,
    )
def calculate_gas_reserves(n_clicks: int,
                           p_area: list[dict],
                           p_effective_thickness: list[dict],
                           p_porosity_coef: list[dict],
                           p_gas_saturation_coef: list[dict],
                           params: list[dict],
                           add_params: list[dict],
                           storage_data: dict):
    
    if n_clicks is None or n_clicks == 0 or ctx.triggered_id != 'calculate_reserves_button':
        return [no_update for _ in range(6)]

# Processing input values to pass them to gas_reserves lib later ------------------------------------------------------------------------------------
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
    params_df = pd.DataFrame(params).set_index(['parameter'])

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

# Making calculations -------------------------------------------------------------------------------------------------------------------------------

    input_data = make_input_data(pd.DataFrame(init_data, index=["value"], dtype=np.float64))
    stat_data = generate_stats(stat_params, np.int64(init_data['num_of_vars']))
    reserves = calculate_reserves(stat_data, input_data)
    df_affection = calculate_sensitivity(stat_data, input_data, reserves)
    df_affection.rename(index=varnames, inplace=True)
    tornado_fig = plot_tornado(df_affection)
    ecdf_fig = plot_ecdf_indicators(reserves, varnames['geo_gas_reserves'])
    pdf_fig = plot_pdf_indicators(reserves, varnames['geo_gas_reserves'])

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


    res_table = [{'parameter': var, 'P90': result_df.loc[var, 'P90'], 'P50': result_df.loc[var, 'P50'], 'P10': result_df.loc[var, 'P10']} for var in result_df.index]

    output_data_columns = ['area_volume', 'pore_volume', 'temp_correction', 'critical_pressure',
                           'critical_temp', 'init_overcompress_coef', 'fin_overcompress_coef',
                           'geo_gas_reserves', 'dry_gas_init_reserves']

    output_data_calcs = [{'parameter': varnames[var], 'value': input_data.loc['value', var]} for var in output_data_columns]

# Save data for tab persistence ---------------------------------------------------------------------------------------------------------------------

    save_data = save_tab_reserves_calcs(storage_data=storage_data,
                                        field_name='Месторождение1',
                                        p_area=p_area,
                                        p_effective_thickness=p_effective_thickness,
                                        p_porosity_coef=p_porosity_coef,
                                        p_gas_saturation_coef=p_gas_saturation_coef,
                                        parameter_table_calcs=params,
                                        parameter_table_output_calcs=output_data_calcs,
                                        indics_calcs=res_table,
                                        tornado_diagram=tornado_fig,
                                        ecdf_plot=ecdf_fig,
                                        pdf_plot=pdf_fig)
    
# Adding calculated earlier in reserves' calculation tab values to inputs of production indicators tab ----------------------------------------------
    pass_df = result_df.copy()
    pass_df = pass_df.drop(varnames['area'])
    pass_data = [{'parameter': var, 'P90': result_df.loc[var, 'P90'], 'P50': result_df.loc[var, 'P50'], 'P10': result_df.loc[var, 'P10']} for var in pass_df.index]
    save_data = save_to_storage(storage_data=save_data, 
                                field_name='Месторождение1', 
                                tab='tab-production-indicators', 
                                prop='parameter_table_stat_indics',
                                data=pass_data)


    keys = dict(
        keys_input = ['init_reservoir_pressure', 'reservoir_temp', 'relative_density', 'init_overcompress_coef'],
        keys_input_hide = ['critical_temp', 'critical_pressure']
    )
    for prop, keys_to_add in zip(['parameter_table_indics', 'parameter_table_indics_collapse'], ['keys_input', 'keys_input_hide']):
        data = get_value(storage_data=save_data,
                         field_name='Месторождение1',
                         tab='tab-production-indicators',
                         prop=prop,
                         default=None)
        
        if data is None:
            data = []
            for var in keys[keys_to_add]:
                data.append({'parameter': varnamesIndicators[var], 'value': input_data.loc['value', var]})
        else:
            for row in data:
                if reversed_varnamesIndicators[row['parameter']] in set(keys[keys_to_add]):
                    row['value'] = input_data.loc['value', reversed_varnamesIndicators[row['parameter']]]
        
        save_data = save_to_storage(storage_data=save_data, 
                                    field_name='Месторождение1', 
                                    tab='tab-production-indicators',
                                    prop=prop,
                                    data=data)

    return [make_indics_table('Параметры', res_table, 'indics'), 
            dcc.Graph(figure=tornado_fig), 
            dcc.Graph(figure=ecdf_fig), 
            dcc.Graph(figure=pdf_fig), 
            output_data_calcs,
            save_data,
        ]


@callback(
    output=[
        [
            Output('prod_calcs_table_P10', 'rowData'),
            Output('prod_calcs_table_P50', 'rowData'),
            Output('prod_calcs_table_P90', 'rowData'),
        ],
        Output('pressures-graph', 'children'),
        Output('prod-kig', 'children'),
        Output('persistence_storage', 'data', allow_duplicate=True),
    ],
    
    inputs=[
        Input('prod_calcs', 'n_clicks'),
        State('parameter-table-permeability', 'rowData'),
        State('parameter-table-indics', 'rowData'),
        State('parameter-table-indics_collapse', 'rowData'),
        State('parameter-table-stat_indics', 'rowData'),
        State('persistence_storage', 'data'),
    ],
    prevent_initial_call=True,
)
def calculate_production_indicators(n_clicks: int, 
                                    p_permeability: list[dict], 
                                    p_indics: list[dict], 
                                    p_indics_collapse: list[dict], 
                                    p_stat_indics: list[dict], 
                                    storage_data: dict):
    if n_clicks is None or n_clicks == 0 or ctx.triggered_id != 'prod_calcs':
        return [[no_update for _ in range(3)], no_update, no_update, no_update]

    _, permeability_params = *parse_params(dist_dict[p_permeability[0]['distribution']], p_permeability[0]),
    stat_params = {"permeability": permeability_params}
    stat_perm = generate_stats(stat_params, 3000)
    
    permeability_Pinds = st.scoreatpercentile(stat_perm['permeability'], [10, 50, 90])

    init_data = {}
    for el in p_indics:
        if el['value'] is not None:
            init_data[reversed_varnamesIndicators[el['parameter']]] = el['value']

    for el in p_indics_collapse:
        if el['value'] is not None:
            init_data[reversed_varnamesIndicators[el['parameter']]] = el['value']

    stat_indics_data = {}
    for row in p_stat_indics:
        stat_indics_data[row['parameter']] = {'P90': row['P90'], 'P50': row['P50'], 'P10': row['P10']}

    prod_kig_fig = None
    pressures_graphs = []
    results_list = []
    save_filtr_resistance_A, save_filtr_resistance_B = None, None
    for perm, name in zip(permeability_Pinds, ['P10', 'P50', 'P90']):
        init_data['permeability'] = perm
        init_data['effective_thickness'] = stat_indics_data[varnamesIndicators['effective_thickness']][name]
        init_data['geo_gas_reserves'] = stat_indics_data[varnamesIndicators['geo_gas_reserves']][name]
        init_data['porosity_coef'] = stat_indics_data[varnamesIndicators['porosity_coef']][name]
        init_data['gas_saturation_coef'] = stat_indics_data[varnamesIndicators['gas_saturation_coef']][name]

        input_data = make_init_data_for_prod_indics(pd.DataFrame(init_data, index=["value"]))

        result = calculate_indicators(input_data.to_dict('records')[0])
        result['year'] = [i for i in range(1, len(result.index)+1)]
        result['avg_production'] = result['annual_production'] / result['n_wells']

        results_list.append(result.to_dict('records'))
        pressures_df = result[['current_pressure', 'wellhead_pressure', 'ukpg_pressure']]
        pressures_df['downhole_pressure'] = result['current_pressure'] - input_data.loc['value', 'max_depression']
        pressures_graphs.append(plot_pressure_on_production_stages(pressures_df, name))
        prod_kig_fig = plot_summary_chart(prod_kig_fig, result[['annual_production', 'kig', 'n_wells']], name)

        if name == 'P50':
            save_filtr_resistance_A, save_filtr_resistance_B = input_data['filtr_resistance_A']['value'], input_data['filtr_resistance_B']['value']
    

    pressures_fig = plot_united_pressures(pressures_graphs)

    save_data = save_tab_production_indicators(storage_data=storage_data,
                                               field_name='Месторождение1',
                                               p_permeability=p_permeability,
                                               parameter_table_indics=p_indics,
                                               parameter_table_stat_indics=p_stat_indics,
                                               parameter_table_indics_collapse=p_indics_collapse,
                                               prod_calcs_table=results_list,
                                               pressures_on_stages_plot=pressures_fig,
                                               prod_kig_plot=prod_kig_fig,
                                               filtr_resistance_A=save_filtr_resistance_A,
                                               filtr_resistance_B=save_filtr_resistance_B)
    
    return [results_list, 
            dcc.Graph(figure=pressures_fig), 
            dcc.Graph(figure=prod_kig_fig), 
            save_data]





# def make_data_to_excel(storage_data: dict) -> dict:
#     data = {}
    
#     for field_name in list(storage_data.keys()):
#         field = {}


#         stat_params = {}
#         dist_params = ['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'permeability']
#         tabs_list = ['tab-reserves-calcs' for _ in range(4)].append('tab-production-indicators')
#         for tab, param_name in zip(tabs_list, dist_params):
#             param = get_value(storage_data=storage_data,
#                               field_name=field_name,
#                               tab=tab,
#                               prop=f'p_{param_name}', default = [])
#             if len(param) != 1:
#                 stat_params[param_name] = {'distribution': '', 'params': ''}
#                 continue
#             row = param[0]
#             parsed = parse_params(row['distribution'], row)
#             var = {
#                 'distribution': row['distribution'],
#                 'params': params_to_string(parsed)
#             }
#             stat_params[reversed_varnames[row['parameter']]] = var


#         init_data = {}
#         parameter_table_calcs = get_value(storage_data=storage_data,
#                                           field_name=field_name,
#                                           tab='tab-reserves-calcs',
#                                           prop='parameter_table_calcs', default=[])
#         parameter_table_output_calcs = get_value(storage_data=storage_data,
#                                           field_name=field_name,
#                                           tab='tab-reserves-calcs',
#                                           prop='parameter_table_output_calcs', default=[])
#         init_data_params = {'relative_density', 'reservoir_temp', 'init_reservoir_pressure', 
#                             'temp_correction', 'init_overcompress_coef', 'num_of_vars'}
#         for row in parameter_table_calcs:
#             if reversed_varnames[row['parameter']] in init_data_params:
#                 init_data[reversed_varnames[row['parameter']]] = row['value']
        
#         for row in parameter_table_output_calcs:
#             if reversed_varnames[row['parameter']] in init_data_params:
#                 init_data[reversed_varnames[row['parameter']]] = row['value']


#         prod_profile_init_data = {}
#         parameter_table_indics = get_value(storage_data=storage_data,
#                                           field_name=field_name,
#                                           tab='tab-production-indicators',
#                                           prop='parameter_table_indics', default=[])
#         parameter_table_indics_collapse = get_value(storage_data=storage_data,
#                                           field_name=field_name,
#                                           tab='tab-production-indicators',
#                                           prop='parameter_table_indics_collapse', default=[])
#         filtr_resistance_A = get_value(storage_data=storage_data,
#                                           field_name=field_name,
#                                           tab='tab-production-indicators',
#                                           prop='filtr_resistance_A', default=None)
#         filtr_resistance_B = get_value(storage_data=storage_data,
#                                           field_name=field_name,
#                                           tab='tab-production-indicators',
#                                           prop='filtr_resistance_B', default=None)
        
#         prod_init_data_params = {'prod_rate', 'operations_ratio', 'reserve_ratio', 'machines_num',
#                                  'time_to_build', 'well_height', 'pipe_diameter', 'main_gas_pipeline_pressure',
#                                  'abandon_pressure_rate', 'filtr_resistance_A', 'filtr_resistance_B',
#                                   'macro_roughness_l', 'trail_length', 'input_cs_temp' }
        
#         for row in parameter_table_indics:
#             if reversed_varnamesIndicators[row['parameter']] in prod_init_data_params:
#                 prod_profile_init_data[reversed_varnamesIndicators[row['parameter']]] = row['value']
        
#         for row in parameter_table_indics_collapse:
#             if reversed_varnamesIndicators[row['parameter']] in prod_init_data_params:
#                 prod_profile_init_data[reversed_varnamesIndicators[row['parameter']]] = row['value']
        
#         prod_profile_init_data['filtr_resistance_A'] = filtr_resistance_A
#         prod_profile_init_data['filtr_resistance_B'] = filtr_resistance_B

#         profiles_report = {'P10': {}, 'P50': {}, 'P90': {}}
#         parameter_table_stat_indics = get_value(storage_data=storage_data,
#                                                 field_name=field_name,
#                                                 tab='tab-production-indicators',
#                                                 prop='parameter_table_stat_indics',
#                                                 default=[])
#         for row in parameter_table_stat_indics:
#             for key in profiles_report.keys():
#                 profiles_report[key][reversed_varnamesIndicators[row['parameter']]] = row[key]
#         images = {}