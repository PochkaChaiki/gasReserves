from dash import html, Input, Output, State, callback, ALL, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import json

from gas_reserves.calculations.reserves_calculations import *
from gas_reserves.calculations.prod_indicators import *

def show_norm(id):
    return html.Div([
        dbc.Label("Мат. ожидание: ", id=id+"-m", html_for=id+"-m-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-m-input"
        }),

        dbc.Label("Ст. откл: ", id=id+"-s", html_for=id+"-s-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-s-input"
        })
    ], style={"display":"flex", "flexDirection": "row"})

def show_uniform(id):
    return html.Div([
        dbc.Label("Мин. значение: ", id=id+"-a", html_for=id+"-a-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-a-input"
        }),
        
        dbc.Label("Макс. значение: ", id=id+"-b", html_for=id+"-b-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-b-input"
        })
    ], style={"display":"flex", "flexDirection": "row"})

def show_triang(id):
    return html.Div([
        dbc.Label("Мин. значение: ", id=id+"-a", html_for=id+"-a-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-a-input"
        }),
        
        dbc.Label("Макс. значение: ", id=id+"-b", html_for=id+"-b-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-b-input"
        }),
        
        dbc.Label("Мода: ", id=id+"-m", html_for=id+"-m-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-m-input"
        })
    ], style={"display":"flex", "flexDirection": "row"})

def show_truncnorm(id):
    return html.Div([
        dbc.Label("Мат. ожидание: ", id=id+"-m", html_for=id+"-m-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-m-input"
        }),
        
        dbc.Label("Ст. откл: ", id=id+"-s", html_for=id+"-s-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-s-input"
        }),

        dbc.Label("Мин. значение: ", id=id+"-a", html_for=id+"-a-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-a-input"
        }),
        
        dbc.Label("Макс. значение: ", id=id+"-b", html_for=id+"-b-input"),
        dbc.Input(type="number", id={
            "type": id,
            "index": id+"-b-input"
        }),

    ], style={"display":"flex", "flexDirection": "row"})

def show_dist_input(dist, id):
    if dist=="norm":
        return show_norm(id)
    elif dist=="uniform":
        return show_uniform(id)
    elif dist=="triang":
        return show_triang(id)
    elif dist=="truncnorm":
        return show_truncnorm(id)

@callback(
    Output("area-input-div", "children"),
    Input("area-select", "value"),
    prevent_initial_call=True)
def show_area_input(dist):
    return show_dist_input(dist, "area")

@callback(
    Output("effective_thickness-input-div", "children"),
    Input("effective_thickness-select", "value"),
    prevent_initial_call=True)
def show_effective_thickness_input(dist):
    return show_dist_input(dist, "effective_thickness")

@callback(
    Output("porosity_coef-input-div", "children"),
    Input("porosity_coef-select", "value"),
    prevent_initial_call=True)
def show_porosity_coef_input(dist):
    return show_dist_input(dist, "porosity_coef")

@callback(
    Output("gas_saturation_coef-input-div", "children"),
    Input("gas_saturation_coef-select", "value"),
    prevent_initial_call=True)
def show_gas_saturation_coef_input(dist):
    return show_dist_input(dist, "gas_saturation_coef")

@callback(
    Output("permeability-input-div", "children"),
    Input("permeability-select", "value"),
    prevent_initial_call=True)
def show_permeability_input(dist):
    return show_dist_input(dist, "permeability")

def parse_params(dist: str, list: list):
    if dist=="norm":
        return list[0], { 
            "distribution": dist,
            "params":{
                "loc":list[0],
                "scale":list[1]
            },
            "adds": {}
        }
    elif dist=="uniform":
        return (list[0]+list[1])/2, { 
            "distribution": dist,
            "params":{
                "loc":list[0],
                "scale":list[1]
            },
            "adds": {}
        }
    elif dist=="triang":
        return sum(list)/3, {
            "distribution": dist,
            "params":{
                "loc":list[0],
                "scale":list[1],
            },
            "adds":{
                "c": list[2]
            }
        }
    elif dist=="truncnorm":
        return list[0], {
            "distribution": dist,
            "params":{
                "loc":list[0],
                "scale":list[1],
            },
            "adds":{
                "a":list[2],
                "b":list[3]
            }
        }

@callback(
    output=[
        Output("output_table", "children"),
        Output("tornado-diagram", "children"),
        Output("indicators-diagram", "children"),
        dict(
            area_volume=dict(value=Output("area_volume-input", "value")),
            pore_volume=dict(value=Output("pore_volume-input", "value")),
            temp_correction=dict(value=Output("temp_correction-input", "value")),
            fin_reservoir_pressure=dict(value=Output("fin_reservoir_pressure-input", "value")),
            critical_pressure=dict(value=Output("critical_pressure-input", "value")),
            critical_temp=dict(value=Output("critical_temp-input", "value")),
            init_overcompress_coef=dict(value=Output("init_overcompress_coef-input", "value")),
            fin_overcompress_coef=dict(value=Output("fin_overcompress_coef-input", "value")),
            geo_gas_reserves=dict(value=Output("geo_gas_reserves-input", "value")),
            dry_gas_init_reserves=dict(value=Output("dry_gas_init_reserves-input", "value"))
        ),
        Output("session_storage", "data"),
        Output("indics_storage", "data")
    ],
    
    inputs=[
        Input("calculate_reserves_button", "n_clicks"),

        State("area-select", "value"),
        State("effective_thickness-select", "value"),
        State("porosity_coef-select", "value"),
        State("gas_saturation_coef-select", "value"),

        State({"type": "area", "index": ALL}, "value"),
        State({"type": "effective_thickness", "index": ALL}, "value"),
        State({"type": "porosity_coef", "index": ALL}, "value"),
        State({"type": "gas_saturation_coef", "index": ALL}, "value"),

        State("init_reservoir_pressure-input", "value"),
        State("relative_density-input", "value"),
        State("reservoir_temp-input", "value"),
        
        dict(
            area_volume=State("area_volume-input", "value"), 
            pore_volume=State("pore_volume-input", "value"),
            temp_correction=State("temp_correction-input", "value"),
            fin_reservoir_pressure=State("fin_reservoir_pressure-input", "value"),
            critical_pressure=State("critical_pressure-input", "value"),
            critical_temp=State("critical_temp-input", "value"),
            init_overcompress_coef=State("init_overcompress_coef-input", "value"),
            fin_overcompress_coef=State("fin_overcompress_coef-input", "value"),
            geo_gas_reserves=State("geo_gas_reserves-input", "value"),
            dry_gas_init_reserves=State("dry_gas_init_reserves-input", "value")
        )
    ],

    prevent_initial_call=True)
def calculate_reserves(n_clicks,
                       area_dist,
                       et_dist,
                       pc_dist,
                       gsc_dist,
                       area_params,
                       et_params,
                       pc_params,
                       gsc_params,
                       init_reservoir_pressure,
                       relative_density,
                       reservoir_temp,
                       add_params):
    if area_dist is None:
        raise PreventUpdate
    area_value, area = *parse_params(area_dist, area_params),
    et_value, effective_thickness = *parse_params(et_dist, et_params),
    pc_value, porosity_coef = *parse_params(pc_dist, pc_params),
    gsc_value, gas_saturation_coef = *parse_params(gsc_dist, gsc_params),
    
    stat_params={
        "area": area,
        "effective_thickness": effective_thickness,
        "porosity_coef": porosity_coef,
        "gas_saturation_coef": gas_saturation_coef
    }

    init_data={
        "area": area_value,
        "effective_thickness": et_value,
        "porosity_coef": pc_value,
        "gas_saturation_coef": gsc_value,
        "init_reservoir_pressure": init_reservoir_pressure,
        "relative_density": relative_density,
        "reservoir_temp": reservoir_temp
    }

    for var in add_params.keys():
        if add_params[var] != None:
            init_data[var] = add_params[var]

    output_data, table_res, tornado_fig, indicators_fig = calculate_result(init_data, stat_params)
    table_res_out = table_res
    return [dbc.Table.from_dataframe(
                table_res.reset_index(), striped=True, bordered=True, hover=True), 
            dcc.Graph(figure=tornado_fig), 
            dcc.Graph(figure=indicators_fig), 
            output_data[add_params.keys()].to_dict(), 
            output_data.to_json(), table_res_out.to_json()]

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
            required_whole_gas_production=State("required_whole_gas_production-indics-input", "value"),
            reserve_ratio=State("reserve_ratio-indics-input", "value"),
            operations_ratio=State("operations_ratio-indics-input", "value"),
            porosity_coef=State("porosity_coef-indics-input", "value"),
            gas_saturation_coef=State("gas_saturation_coef-indics-input", "value"),
            avg_well_temp=State("avg_well_temp-indics-input", "value"),
            pipe_diameter=State("pipe_diameter-indics-input", "value"),
            well_height=State("well_height-indics-input", "value"),
            pipe_roughness=State("pipe_roughness-indics-input", "value"),
            init_num_wells=State("init_num_wells-indics-input", "value"),
            trail_length=State("trail_length-indics-input", "value"),
            trail_diameter=State("trail_diameter-indics-input", "value"),
            trail_roughness=State("trail_roughness-indics-input", "value"),
            avg_trail_temp=State("avg_trail_temp-indics-input", "value"),
            main_gas_pipeline_pressure=State("main_gas_pipeline_pressure-indics-input", "value"),
            input_cs_temp=State("input_cs_temp-indics-input", "value"),
            coef_K=State("coef_K-indics-input", "value"),
            efficiency_cs=State("efficiency_cs-indics-input", "value"),
            adiabatic_index=State("adiabatic_index-indics-input", "value"),
            density_athmospheric=State("density_athmospheric-indics-input", "value"),
            viscosity=State("viscosity-indics-input", "value"),
            machines_num=State("machines_num-indics-input", "value"),
            time_to_build=State("time_to_build-indics-input", "value"),
            annual_production=State("annual_production-indics-input", "value"),
            lambda_trail=State("lambda_trail-indics-input", "value"),
            lambda_fontain=State("lambda_fontain-indics-input", "value"),
            macro_roughness_l=State("macro_roughness_l-indics-input", "value"),
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