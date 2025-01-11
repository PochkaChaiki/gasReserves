from dash import html, Input, Output, State, callback, ALL, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import json

from layout import *
from gas_reserves.plot import *
from gas_reserves.calculations.reserves_calculations import *
from gas_reserves.calculations.prod_indicators import *



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
        Output("ecdf-diagram", "children"),
        Output('pdf-diagram', 'children'),
        Output('parameter-table-output-calcs', 'rowData'),
        Output("calcs_storage", "data"),
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
    ecdf_fig = plot_ecdf_indicators(reserves, varnames['reserves'])
    pdf_fig = plot_pdf_indicators(reserves, varnames['reserves'])

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

    save_data = {
        'p_area':p_area,
        'p_effective_thickness':p_effective_thickness,
        'p_porosity_coef':p_porosity_coef,
        'p_gas_saturation_coef':p_gas_saturation_coef,
        'params':params,
        'add_params':output_data_calcs,
    }
    return [make_indics_table('Параметры', res_table, 'indics'), 
            dcc.Graph(figure=tornado_fig), 
            dcc.Graph(figure=ecdf_fig), 
            dcc.Graph(figure=pdf_fig), 
            output_data_calcs,
            json.dumps(save_data),
            json.dumps(res_table),
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
        # [
        #     Output('pres-p10', 'figure'),
        #     Output('pres-p50', 'figure'),
        #     Output('pres-p90', 'figure')
        # ],
        Output('pressures-graph', 'figure'),
        Output('prod-kig', 'figure'),

    ],
    inputs=[
        Input('prod_calcs', 'n_clicks'),
        State('parameter-table-permeability', 'rowData'),
        State('parameter-table-indics', 'rowData'),
        State('parameter-table-indics-collapse', 'rowData'),
        State('parameter-table-effective_thickness-indics', 'rowData'),
        State('parameter-table-geo_gas_reserves-indics', 'rowData'),        
    ],
    prevent_initial_call=True
)
def calculate_production_indicators(n_clicks, p_permeability, p_indics, p_indics_collapse, p_et, p_ggr):
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


    effective_thickness_Pinds = [p_et[0]['P90'], p_et[0]['P50'], p_et[0]['P10']]
    geo_gas_reserves_Pinds = [p_ggr[0]['P90'], p_ggr[0]['P50'], p_ggr[0]['P10']]
    

    prod_kig_fig = None
    pressures_graphs = []
    for eft, ggr, perm, name in zip(effective_thickness_Pinds, geo_gas_reserves_Pinds, permeability_Pinds, ['P10', 'P50', 'P90']):
        init_data['permeability'] = perm
        init_data['effective_thickness'] = eft
        init_data['geo_gas_reserves'] = ggr

        input_data = make_init_data_for_prod_indics(pd.DataFrame(init_data, index=["value"]))
        # print(input_data)
        result = calculate_indicators(input_data.to_dict('records')[0])
        pressures_df = result[['current_pressure', 'wellhead_pressure', 'ukpg_pressure']]
        pressures_df['downhole_pressure'] = result['current_pressure'] - input_data.loc['value', 'max_depression']
        # print(pressures_df)
        pressures_graphs.append(plot_pressure_on_production_stages(pressures_df, name))
        prod_kig_fig = plot_summary_chart(prod_kig_fig, result[['annual_production', 'kig', 'n_wells']], name)
    
    # plot_united_pressures(pressures_graphs)
    return plot_united_pressures(pressures_graphs), prod_kig_fig