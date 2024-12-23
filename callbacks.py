from dash import html, Input, Output, State, callback, ALL, dcc
import dash_bootstrap_components as dbc


from gas_reserves.calculations.reserves_calculations import *

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
                "c": list[3]
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
        )
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
    
    return [dbc.Table.from_dataframe(table_res.reset_index(), striped=True, bordered=True, hover=True), dcc.Graph(figure=tornado_fig), dcc.Graph(figure=indicators_fig), output_data[add_params.keys()].to_dict()]


    