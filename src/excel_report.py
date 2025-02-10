from src.utils import *
from src.gas_reserves.constants import *

import pandas as pd

def collect_stat_params(storage_data: dict, field_name: str) -> dict:
    stat_params = {}
    dist_params = ['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'permeability']
    tabs_list = ['tab-reserves-calcs' for _ in range(4)]
    tabs_list.append('tab-production-indicators')

    for tab, param_name in zip(tabs_list, dist_params):
        param = get_value(storage_data=storage_data,
                          field_name=field_name,
                          tab=tab,
                          prop=f'p_{param_name}', default = [])
        if len(param) != 1:
            stat_params[param_name] = {'distribution': '', 'params': ''}
            continue
        row = param[0]
        _, parsed = parse_params(dist_dict[row['distribution']], row)
        var = {
            'distribution': row['distribution'],
            'params': params_to_string(parsed)
        }

        if reversed_varnames.get(row['parameter'], None):
            stat_params[reversed_varnames[row['parameter']]] = var
        elif reversed_varnamesIndicators.get(row['parameter'], None):
            stat_params[reversed_varnamesIndicators[row['parameter']]] = var

    return stat_params

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
        value = df[constants.get(key, None)]
        out[key] = round(value, 3) if value else None

    return out


def collect_init_data(storage_data: dict, field_name: str) -> dict:
    init_data = {}
    parameter_table_calcs = get_value(storage_data=storage_data,
                                      field_name=field_name,
                                      tab='tab-reserves-calcs',
                                      prop='parameter_table_calcs',
                                      default=[])
    parameter_table_output_calcs = get_value(storage_data=storage_data,
                                             field_name=field_name,
                                             tab='tab-reserves-calcs',
                                             prop='parameter_table_output_calcs',
                                             default=[])
    calcs_params = ['relative_density', 'reservoir_temp', 'init_reservoir_pressure', 'num_of_vars']
    output_calcs_params = ['temp_correction', 'init_overcompress_coef']

    init_data = get_values_from_records(parameter_table_calcs, init_data, calcs_params, varnames)

    init_data = get_values_from_records(parameter_table_output_calcs, init_data, output_calcs_params, varnames)

    return init_data



def collect_prod_profile_init_data(storage_data: dict, field_name:str) -> dict:
    prod_profile_init_data = {}
    parameter_table_indics = get_value(storage_data=storage_data,
                                       field_name=field_name,
                                       tab='tab-production-indicators',
                                       prop='parameter_table_indics', default=[])


    # ! Have to keep in mind, that I don't add filtr_resistance to page !
    filtr_resistance_A = get_value(storage_data=storage_data,
                                   field_name=field_name,
                                   tab='tab-production-indicators',
                                   prop='filtr_resistance_A', default=None)
    filtr_resistance_B = get_value(storage_data=storage_data,
                                   field_name=field_name,
                                   tab='tab-production-indicators',
                                   prop='filtr_resistance_B', default=None)
    
    # ! Mock for now ! ----------------------------------------------------------!!!!!!
    hydraulic_resistance = 0.019
        
    prod_init_data_params = ['prod_rate', 'operations_ratio', 'reserve_ratio', 'machines_num',
                             'time_to_build', 'well_height', 'pipe_diameter', 'main_gas_pipeline_pressure',
                             'abandon_pressure',
                             'trail_length', 'input_cs_temp']


    prod_profile_init_data = get_values_from_records(parameter_table_indics,
                                                     prod_profile_init_data,
                                                     prod_init_data_params,
                                                     varnamesIndicators)

        
    prod_profile_init_data['filtr_resistance_A'] = filtr_resistance_A
    prod_profile_init_data['filtr_resistance_B'] = filtr_resistance_B
    prod_profile_init_data['hydraulic_resistance'] = hydraulic_resistance
    return prod_profile_init_data



def collect_profiles_report(storage_data: dict, field_name: str) -> dict:
    profiles_report = {'P10': {}, 'P50': {}, 'P90': {}}
    parameter_table_stat_indics = get_value(storage_data=storage_data,
                                            field_name=field_name,
                                            tab='tab-production-indicators',
                                            prop='parameter_table_stat_indics',
                                            default=[])

    parameter_table_indics = get_value(storage_data=storage_data,
                                       field_name=field_name,
                                       tab='tab-production-indicators',
                                       prop='parameter_table_indics', default=[])
    
    parameter_table_output_calcs = get_value(storage_data=storage_data,
                                             field_name=field_name,
                                             tab='tab-reserves-calcs',
                                             prop='parameter_table_output_calcs',
                                             default=[])

    stat_indics_params = ['effective_thickness', 'geo_gas_reserves',
                          'porosity_coef', 'gas_saturation_coef']
    for key in profiles_report.keys():
        profiles_report[key] = get_values_from_records(parameter_table_stat_indics,
                                                       profiles_report[key],
                                                       stat_indics_params,
                                                       varnamesIndicators,
                                                       col=key)


    indics_params = ['relative_density', 'reservoir_temp',
                     'init_reservoir_pressure',
                     'init_overcompress_coef']

    indics_data = get_values_from_records(parameter_table_indics,
                                          {},
                                          indics_params,
                                          varnamesIndicators)

    prod_rate = get_values_from_records(parameter_table_indics,
                                        {},
                                        ['prod_rate'],
                                        varnamesIndicators)

    for key in profiles_report.keys():
        profiles_report[key] = dict(profiles_report[key], **indics_data)

        profiles_report[key]['annual_production'] = round(
            prod_rate['prod_rate'] * profiles_report[key]['geo_gas_reserves'], 3
        ) if prod_rate['prod_rate'] else None



    temp_correction = get_values_from_records(parameter_table_output_calcs,
                                              {},
                                              ['temp_correction'],
                                              varnames)
    for key in profiles_report.keys():
        profiles_report[key] = dict(profiles_report[key], **temp_correction)


    prod_calcs_table = get_value(storage_data=storage_data,
                                 field_name=field_name,
                                 tab='tab-production-indicators',
                                 prop='prod_calcs_table', default=[])
    for data, indic in zip(prod_calcs_table, ('P10', 'P50', 'P90')):
        acc, kig, nw, year = 0, 0, 0, 0
        for row in data:
            acc += row['annual_production']
        profiles_report[indic]['accumulated_production'] = round(acc, 3) if acc else None
        profiles_report[indic]['kig'] = round(data[-1]['kig'], 3) if data[-1]['kig'] else None
        profiles_report[indic]['num_of_wells'] = data[-1]['n_wells']
        profiles_report[indic]['years'] = data[-1]['year']
    
    return profiles_report



def collect_images(storage_data: dict, field_name: str)->dict:
    images = {}

    pdf_plot: go.Figure = go.Figure(
        get_value(storage_data=storage_data,
                  field_name=field_name,
                  tab='tab-reserves-calcs',
                  prop='pdf_plot',
                  default=None)
    )

    images['hist'] = pdf_plot.to_image('png')

    tornado_diagram: go.Figure = go.Figure(
        get_value(storage_data=storage_data,
                  field_name=field_name,
                  tab='tab-reserves-calcs',
                  prop='tornado_diagram',
                  default=None)
    )
    images['tornado'] = tornado_diagram.to_image('png')

    prod_kig_plot: go.Figure = go.Figure(
        get_value(storage_data=storage_data,
                  field_name=field_name,
                  tab='tab-production-indicators',
                  prop='prod_kig_plot',
                  default=None)
    )
    images['profile'] = prod_kig_plot.to_image('png')
    return images

def collect_risks(storage_data: dict, field_name: str)->tuple[dict, dict, float]:
    tab='tab-risks-and-uncertainties'
    parameter_table_risks = get_value(storage_data=storage_data,
                                      field_name=field_name,
                                      tab=tab,
                                      prop='parameter_table_risks',
                                      default=[])
    kriteria_seismic_exploration_work_table = get_value(storage_data=storage_data,
                                                        field_name=field_name,
                                                        tab=tab,
                                                        prop='kriteria_seismic_exploration_work_table',
                                                        default=[])
    kriteria_grid_density_table = get_value(storage_data=storage_data,
                                            field_name=field_name,
                                            tab=tab,
                                            prop='kriteria_grid_density_table',
                                            default=[])
    kriteria_core_research_table = get_value(storage_data=storage_data,
                                             field_name=field_name,
                                             tab=tab,
                                             prop='kriteria_core_research_table',
                                             default=[])
    kriteria_c1_reserves_table = get_value(storage_data=storage_data,
                                           field_name=field_name,
                                           tab=tab,
                                           prop='kriteria_c1_reserves_table',
                                           default=[])
    kriteria_hydrocarbon_properties_table = get_value(storage_data=storage_data,
                                                      field_name=field_name,
                                                      tab=tab,
                                                      prop='kriteria_hydrocarbon_properties_table',
                                                      default=[])
    study_coef = get_value(storage_data=storage_data,
                           field_name=field_name,
                           tab=tab,
                           prop='study_coef',
                           default=0)

    risk_params = {}
    for row in parameter_table_risks:
        risk_params[reversed_varnamesRisks[row['parameter']]] = row['value']

    risks_kriterias = {}
    for param in (kriteria_seismic_exploration_work_table,
                  kriteria_grid_density_table,
                  kriteria_core_research_table,
                  kriteria_c1_reserves_table,
                  kriteria_hydrocarbon_properties_table):
        risks_kriterias[reversed_varnamesRisks[param[0]['parameter']]] = dict(
            kriteria=param[0]['kriteria'],
            value=param[0]['value'],
            weight=param[0]['weight'],
        )

    return risk_params, risks_kriterias, study_coef


def make_data_to_excel(storage_data: dict) -> dict:
    data = {}
    
    for field_name in list(storage_data.keys()):

        stat_params = collect_stat_params(storage_data, field_name)

        init_data = collect_init_data(storage_data, field_name)

        prod_profile_init_data = collect_prod_profile_init_data(storage_data, field_name)

        profiles_report = collect_profiles_report(storage_data, field_name)

        images = collect_images(storage_data, field_name)

        risk_params, risks_kriterias, study_coef = collect_risks(storage_data, field_name)
        field = {
            'stat_params': stat_params,
            'init_data': init_data,
            'prod_profile_init_data': prod_profile_init_data,
            'profiles_report': profiles_report,
            'images': images,
            'risk_params': risk_params,
            'risks_kriterias': risks_kriterias,
            'study_coef': study_coef,
        }
        data[field_name] = field
    return data
