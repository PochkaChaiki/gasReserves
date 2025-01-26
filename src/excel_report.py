from .utils import *
from gas_reserves.constants import *

def collect_stat_params(storage_data: str, field_name: str) -> dict:
    stat_params = {}
    dist_params = ['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'permeability']
    tabs_list = ['tab-reserves-calcs' for _ in range(4)].append('tab-production-indicators')
    for tab, param_name in zip(tabs_list, dist_params):
        param = get_value(storage_data=storage_data,
                          field_name=field_name,
                          tab=tab,
                          prop=f'p_{param_name}', default = [])
        if len(param) != 1:
            stat_params[param_name] = {'distribution': '', 'params': ''}
            continue
        row = param[0]
        parsed = parse_params(row['distribution'], row)
        var = {
            'distribution': row['distribution'],
            'params': params_to_string(parsed)
        }
        stat_params[reversed_varnames[row['parameter']]] = var
    return stat_params



def collect_init_data (storage_data: str, field_name: str) -> dict:
    init_data = {}
    parameter_table_calcs = get_value(storage_data=storage_data,
                                          field_name=field_name,
                                          tab='tab-reserves-calcs',
                                          prop='parameter_table_calcs', default=[])
    parameter_table_output_calcs = get_value(storage_data=storage_data,
                                          field_name=field_name,
                                          tab='tab-reserves-calcs',
                                          prop='parameter_table_output_calcs', default=[])
    init_data_params = {'relative_density', 'reservoir_temp', 'init_reservoir_pressure', 
                            'temp_correction', 'init_overcompress_coef', 'num_of_vars'}
    for row in parameter_table_calcs:
        if reversed_varnames[row['parameter']] in init_data_params:
            init_data[reversed_varnames[row['parameter']]] = row['value']
        
    for row in parameter_table_output_calcs:
        if reversed_varnames[row['parameter']] in init_data_params:
            init_data[reversed_varnames[row['parameter']]] = row['value']
    return init_data



def collect_prod_profile_init_data(storage_data: str, field_name:str) -> dict:
    prod_profile_init_data = {}
    parameter_table_indics = get_value(storage_data=storage_data,
                                       field_name=field_name,
                                       tab='tab-production-indicators',
                                       prop='parameter_table_indics', default=[])
    parameter_table_indics_collapse = get_value(storage_data=storage_data,
                                                field_name=field_name,
                                                tab='tab-production-indicators',
                                                prop='parameter_table_indics_collapse', default=[])
    filtr_resistance_A = get_value(storage_data=storage_data,
                                   field_name=field_name,
                                   tab='tab-production-indicators',
                                   prop='filtr_resistance_A', default=None)
    filtr_resistance_B = get_value(storage_data=storage_data,
                                   field_name=field_name,
                                   tab='tab-production-indicators',
                                   prop='filtr_resistance_B', default=None)
        
    prod_init_data_params = {'prod_rate', 'operations_ratio', 'reserve_ratio', 'machines_num',
                             'time_to_build', 'well_height', 'pipe_diameter', 'main_gas_pipeline_pressure',
                             'abandon_pressure_rate', 'filtr_resistance_A', 'filtr_resistance_B',
                             'macro_roughness_l', 'trail_length', 'input_cs_temp' }
        
    for row in parameter_table_indics:
        if reversed_varnamesIndicators[row['parameter']] in prod_init_data_params:
            prod_profile_init_data[reversed_varnamesIndicators[row['parameter']]] = row['value']
        
    for row in parameter_table_indics_collapse:
        if reversed_varnamesIndicators[row['parameter']] in prod_init_data_params:
            prod_profile_init_data[reversed_varnamesIndicators[row['parameter']]] = row['value']
        
    prod_profile_init_data['filtr_resistance_A'] = filtr_resistance_A
    prod_profile_init_data['filtr_resistance_B'] = filtr_resistance_B
    return prod_profile_init_data



def collect_profiles_report (storage_data: str, field_name: str) -> dict:
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

    for row in parameter_table_stat_indics:
       for key in profiles_report.keys():
           profiles_report[key][reversed_varnamesIndicators[row['parameter']]] = row[key]


    for row in parameter_table_indics:
       for key in profiles_report.keys():
           if reversed_varnamesIndicators[row['parameter']] in ('relative_density', 'reservoir_temp', 
                                                                    'init_reservoir_pressure', 'temp_correction', 
                                                                    'init_overcompress_coef'):
               profiles_report[key][reversed_varnamesIndicators[row['parameter']]] = row['value']
           elif reversed_varnamesIndicators[row['parameter']] == 'prod_rate':
               profiles_report[key]['annual_production'] = row['value'] * profiles_report[key]['geo_gas_reserves']
        
    prod_calcs_table = get_value(storage_data=storage_data,
                                    field_name=field_name,
                                    tab='tab-production-indicators',
                                    prop='prod_calcs_table', default=[])
    for data, indic in zip(prod_calcs_table, ('P10', 'P50', 'P90')):
       acc, kig, nw, year = 0, 0, 0, 0
       for row in data:
           acc += row[varnamesIndicators['annual_production']]
       kig = data[-1][varnamesIndicators['kig']]
       nw = data[-1][varnamesIndicators['num_of_wells']]
       year = data[-1][varnamesIndicators['year']]
       profiles_report[indic]['accumulated_production'] = acc
       profiles_report[indic]['kig'] = kig
       profiles_report[indic]['num_of_wells'] = nw
       profiles_report[indic]['years'] = year
    return profiles_report



def collect_images(storage_data: str, field_name: str)->dict:
    images = {}
    pdf_plot: go.Figure = get_value(storage_data=storage_data,
                                        field_name=field_name,
                                        tab='tab-reserves-calcs',
                                        prop='pdf_plot')
    images['hist'] = pdf_plot.to_image('png')

    tornado_diagram: go.Figure = get_value(storage_data=storage_data,
                                               field_name=field_name,
                                               tab='tab-reserves-calcs',
                                               prop='tornado_diagram')
    images['tornado'] = tornado_diagram.to_image('png')

    prod_kig_plot: go.Figure = get_value(storage_data=storage_data,
                                             field_name=field_name,
                                             tab='tab-reserves-calcs',
                                             prop='prod_kig_plot')
    images['profile'] = prod_kig_plot.to_image('png')
    return images



def make_data_to_excel(storage_data: dict) -> dict:
    data = {}
    
    for field_name in list(storage_data.keys()):

        stat_params = collect_stat_params(storage_data=storage_data, field_name=field_name)

        init_data = collect_init_data(storage_data=storage_data,field_name=field_name)

        prod_profile_init_data = collect_prod_profile_init_data(storage_data=storage_data, field_name=field_name)

        profiles_report = collect_profiles_report(storage_data=storage_data, field_name=field_name)

        images = collect_images(storage_data=storage_data, field_name=field_name)

        field = {
            'stat_params': stat_params,
            'init_data': init_data,
            'prod_profile_init_data': prod_profile_init_data,
            'profiles_report': profiles_report,
            'images': images
        }
        data[field_name] = field
    return data
