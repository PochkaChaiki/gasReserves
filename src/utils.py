import plotly.graph_objects as go





# persistence_storage = {
#     'field_name': {
#         'tab-reserves-calcs': {
#             'p_area': dict(),
#             'p_effective_thickness': dict(),
#             'p_porosity_coef': dict(),
#             'p_gas_saturation_coef': dict(),
#             'parameter_table_calcs': dict(),
#             'parameter_table_output_calcs': dict(),
#             'tornado_diagram': go.Figure,
#             'indics_calcs': dict(),
#             'ecdf_plot': go.Figure,
#             'pdf_plot': go.Figure,
#         },
#         'tab-production-indicators': {
#             'p_permeability': dict(),
#             'parameter_table_indics': dict(),
#             'parameter_table_effective_thickness_indics': dict(),
#             'parameter_table_geo_gas_reserves_indics': dict(),
#             'parameter_table_indics_collapse': dict(),
#             'prod_calcs_table': list[dict] ,
#             'pressures_on_stages_plot': go.Figure,
#             'prod_kig_plot': go.Figure,
#         }
#     }
# }

def get_tab(storage_data: dict | None,
            field_name: str,
            tab: str ) -> dict:
    if storage_data is None or storage_data.get(field_name, None) is None or storage_data[field_name].get(tab, None) is None: 
        return {}
    return storage_data[field_name][tab]

def get_value(storage_data: dict | None,
              field_name: str,
              tab: str, 
              prop: str,
              default: object | None = None) -> object:
    if storage_data is None:
        return default
    if storage_data.get(field_name, None):
        return default
    if storage_data[field_name].get(tab, None) is None:
        return default
    if storage_data[field_name][tab].get(prop, None) is None:
        return default
    return storage_data[field_name][tab][prop]

def save_tab_reserves_calcs(storage_data: dict | None,
                            field_name: str,
                            p_area: dict | None = None,
                            p_effective_thickness: dict | None = None,
                            p_porosity_coef: dict | None = None,
                            p_gas_saturation_coef: dict | None = None,
                            parameter_table_calcs: dict | None = None,
                            parameter_table_output_calcs: dict | None = None,
                            indics_calcs: dict | None = None,
                            tornado_diagram: go.Figure | None = None,
                            ecdf_plot: go.Figure | None = None,
                            pdf_plot: go.Figure | None = None ) -> dict:

    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'p_area', p_area)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'p_effective_thickness', p_effective_thickness)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'p_porosity_coef', p_porosity_coef)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'p_gas_saturation_coef', p_gas_saturation_coef)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'parameter_table_calcs', parameter_table_calcs)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'parameter_table_output_calcs', parameter_table_output_calcs)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'indics_calcs', indics_calcs)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'tornado_diagram', tornado_diagram)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'ecdf_plot', ecdf_plot)
    storage_data = save_to_storage(storage_data, field_name, 'tab-reserves-calcs', 'pdf_plot', pdf_plot)

    return storage_data


def save_tab_production_indicators(storage_data: dict | None,
                                   field_name: str,
                                   p_permeability: dict | None = None,
                                   parameter_table_indics: dict | None = None,
                                   parameter_table_effective_thickness_indics: dict | None = None,
                                   parameter_table_geo_gas_reserves_indics: dict | None = None,
                                   parameter_table_indics_collapse: dict | None = None,
                                   prod_calcs_table: list[dict] | None = None,
                                   pressures_on_stages_plot: go.Figure | None = None,
                                   prod_kig_plot: go.Figure | None = None) -> dict:
    
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'p_permeability', p_permeability)
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'parameter_table_indics', parameter_table_indics)
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'parameter_table_effective_thickness_indics', parameter_table_effective_thickness_indics)
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'parameter_table_geo_gas_reserves_indics', parameter_table_geo_gas_reserves_indics)
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'parameter_table_indics_collapse', parameter_table_indics_collapse)
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'prod_calcs_table', prod_calcs_table)
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'pressures_on_stages_plot', pressures_on_stages_plot)
    storage_data = save_to_storage(storage_data, field_name, 'tab-production-indicators', 'prod_kig_plot', prod_kig_plot)
    
    return storage_data

def save_to_storage(storage_data: dict | None, 
                    field_name: str, 
                    tab: str,
                    prop: str,
                    data: object ) -> dict:
    
    if storage_data is None:
        storage_data = {
            field_name: {
                tab: {
                    prop: data,
                }
            }
        }
        return storage_data
    
    if storage_data.get(field_name, None) is None: 
        storage_data[field_name] = {
            tab: {
                prop: data,
            }
        }
        return storage_data

    if storage_data[field_name].get(tab, None) is None:
        storage_data[field_name][tab] = {
            prop: data
        }
    
    storage_data[field_name][tab][prop] = data
    return storage_data



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