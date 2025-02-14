import plotly.graph_objects as go
import pandas as pd

'''
persistence_storage = {
    'field_name': {
        'tab-reserves-calcs': {
            'p_area': dict(),
            'p_effective_thickness': dict(),
            'p_porosity_coef': dict(),
            'p_gas_saturation_coef': dict(),
            'parameter_table_calcs': dict(),
            'parameter_table_output_calcs': dict(),
            'tornado_diagram': go.Figure,
            'indics_calcs': dict(),
            'ecdf_plot': go.Figure,
            'pdf_plot': go.Figure,
        },
        'tab-production-indicators': {
            'p_permeability': dict(),
            'parameter_table_indics': dict(),
            'parameter_table_stat_indics': dict(),
            'parameter_table_indics_collapse': dict(),
            'prod_calcs_table': list[dict] ,
            'pressures_on_stages_plot': go.Figure,
            'prod_kig_plot': go.Figure,
            'filtr_resistance_A': float,
            'filtr_resistance_B': float,
        },
        'tab-risks-and-uncertainties': {
            
        }
    }
} 
'''

def get_tab(storage_data: dict | None,
            field_name: str,
            tab: str) -> dict:
    if (storage_data is None
            or storage_data.get(field_name, None) is None
            or storage_data[field_name].get(tab,None) is None):

        return {}
    return storage_data[field_name][tab]


def get_value(storage_data: dict | None,
              field_name: str,
              tab: str,
              prop: str,
              default: any) -> any:
    if (storage_data is None
            or storage_data.get(field_name, None) is None
            or storage_data[field_name].get(tab, None) is None
            or storage_data[field_name][tab].get(prop, None) is None):
        return default

    return storage_data[field_name][tab][prop]


def save_tab_reserves_calcs(storage_data: dict | None,
                            field_name: str,
                            p_area: list[dict] | None,
                            p_effective_thickness: list[dict] | None,
                            p_porosity_coef: list[dict] | None,
                            p_gas_saturation_coef: list[dict] | None,
                            parameter_table_calcs: list[dict] | None,
                            parameter_table_output_calcs: list[dict] | None,
                            indics_calcs: list[dict] | None,
                            tornado_diagram: go.Figure | None,
                            ecdf_plot: go.Figure | None,
                            pdf_plot: go.Figure | None) -> dict:
    tab = 'tab-reserves-calcs'

    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'p_area',
                                   p_area)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'p_effective_thickness',
                                   p_effective_thickness)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'p_porosity_coef',
                                   p_porosity_coef)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'p_gas_saturation_coef',
                                   p_gas_saturation_coef)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'parameter_table_calcs',
                                   parameter_table_calcs)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'parameter_table_output_calcs',
                                   parameter_table_output_calcs)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'indics_calcs',
                                   indics_calcs)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'tornado_diagram',
                                   tornado_diagram)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'ecdf_plot',
                                   ecdf_plot)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'pdf_plot',
                                   pdf_plot)

    return storage_data


def save_tab_production_indicators(storage_data: dict | None,
                                   field_name: str,
                                   p_permeability: list[dict] | None,
                                   parameter_table_indics: list[dict] | None,
                                   parameter_table_stat_indics: list[dict] | None,
                                   parameter_table_indics_collapse: list[dict] | None,
                                   prod_calcs_table: list[dict] | None,
                                   pressures_on_stages_plot: go.Figure | None,
                                   prod_kig_plot: go.Figure | None,
                                   filtr_resistance_A: float | None,
                                   filtr_resistance_B: float | None) -> dict:
    tab = 'tab-production-indicators'
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'p_permeability',
                                   p_permeability)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'parameter_table_indics',
                                   parameter_table_indics)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'parameter_table_stat_indics',
                                   parameter_table_stat_indics)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'parameter_table_indics_collapse',
                                   parameter_table_indics_collapse)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'prod_calcs_table',
                                   prod_calcs_table)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'pressures_on_stages_plot',
                                   pressures_on_stages_plot)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'prod_kig_plot',
                                   prod_kig_plot)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'filtr_resistance_A',
                                   filtr_resistance_A)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'filtr_resistance_B',
                                   filtr_resistance_B)

    return storage_data

def save_tab_risks_and_uncertainties(storage_data: dict | None,
                                     field_name: str,
                                     parameter_table_risks: list[dict] | None,
                                     kriteria_seismic_exploration_work_table: list[dict] | None,
                                     kriteria_grid_density_table: list[dict] | None,
                                     kriteria_core_research_table: list[dict] | None,
                                     kriteria_c1_reserves_table: list[dict] | None,
                                     kriteria_hydrocarbon_properties_table: list[dict] | None,
                                     study_coef: float) -> dict:

    tab = 'tab-risks-and-uncertainties'

    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'parameter_table_risks',
                                   parameter_table_risks)

    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'kriteria_seismic_exploration_work_table',
                                   kriteria_seismic_exploration_work_table)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'kriteria_grid_density_table',
                                   kriteria_grid_density_table)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'kriteria_core_research_table',
                                   kriteria_core_research_table)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'kriteria_c1_reserves_table',
                                   kriteria_c1_reserves_table)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'kriteria_hydrocarbon_properties_table',
                                   kriteria_hydrocarbon_properties_table)
    storage_data = save_to_storage(storage_data, field_name, tab,
                                   'study_coef',
                                   study_coef)

    return storage_data


def save_to_storage(storage_data: dict | None,
                    field_name: str,
                    tab: str,
                    prop: str,
                    data: object) -> dict:
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


def params_to_string(parsed_params: dict) -> str:
    if parsed_params['distribution'] == 'norm':
        return f'M = {parsed_params['params']['loc']}, std = {parsed_params['params']['scale']}'
    if parsed_params['distribution'] == 'uniform':
        return f'a = {parsed_params['params']['loc']}, b = {parsed_params['params']['loc'] + parsed_params['params']['scale']}'
    if parsed_params['distribution'] == 'triang':
        return f'a = {parsed_params['params']['loc']}, b = {parsed_params['params']['loc'] + parsed_params['params']['scale']}, c = {parsed_params['adds']['c']}'
    if parsed_params['distribution'] == 'truncnorm':
        return f'M = {parsed_params['params']['loc']}, std = {parsed_params['params']['scale']}, ' + \
            f'a = {parsed_params['adds']['a']}, b = {parsed_params['adds']['a'] + parsed_params['adds']['b']}'
    return ''


def parse_params(dist: str,
                 params: dict[str, int | float]
) -> tuple[int | float | None, dict[str, str | dict[str, int | float]] | None]:
    if dist == "norm":
        return params.get('mean', 0), {
            "distribution": dist,
            "params": {
                "loc": params.get('mean', 0),
                "scale": params.get('std_dev', 1),
            },
            "adds": {}
        }
    elif dist == "uniform":
        min_value = params.get('min_value', 0)
        max_value = params.get('max_value', 1)
        loc = min_value
        scale = max_value - min_value
        return (min_value + max_value) / 2, {
            "distribution": dist,
            "params": {
                "loc": loc,
                "scale": scale,
            },
            "adds": {}
        }
    elif dist == "triang":
        min_value = params.get('min_value', 0)
        max_value = params.get('max_value', 1)
        mode = params.get('mode', 0.5)
        loc = min_value
        scale = max_value - min_value
        c = (mode - loc) / scale
        return (min_value + max_value + mode) / 3, {
            "distribution": dist,
            "params": {
                "loc": loc,
                "scale": scale,
            },
            "adds": {
                "c": c,
            }
        }
    elif dist == "truncnorm":
        min_value = params.get('min_value', 0)
        max_value = params.get('max_value', 1)
        a = min_value
        b = max_value - min_value
        return params.get('mean', 0), {
            "distribution": dist,
            "params": {
                "loc": params.get('mean', 0),
                "scale": params.get('std_dev', 1),
            },
            "adds": {
                "a": a,
                "b": b,
            }
        }
    return None, None


def appropriate_name(name: str, list: list[str]) -> str:
    names_count = 0
    name_exists = False
    for el in list:
        if el.startswith(name):
            names_count += 1
            if el == name:
                name_exists = True

    if not name_exists:
        return name

    if names_count:
        better_name = name + f'({str(names_count)})'
        return better_name
    return name


def get_values_from_records(records: list[dict],
                            out: dict,
                            keys: list,
                            constants: dict,
                            index: list = None,
                            col: str = 'value') -> dict:
    index = index or ['parameter']
    df = pd.DataFrame.from_records(records, index=index)
    if not df.empty:
        df = df[col]

    for key in keys:
        value = df.get(constants.get(key, None))
        out[key] = round(value, 3) if value else None

    return out