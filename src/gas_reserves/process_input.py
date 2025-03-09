import pandas as pd
import numpy as np
from src.gas_reserves.constants import *

'''
------------------------------------------------------------------------------------------------------------------------|
    DATA EXAMPLE:
        init_data = {
            'area': 38_556 * 1e3,
            'effective_thickness': 11.10,
            'porosity_coef': 0.091,
            'gas_saturation_coef': 0.7,
            'init_reservoir_pressure': 32.30 * 1e6,
            'relative_density': 0.6348,
            'reservoir_temp': 320.49,
            'permeability': 0.75,
        }
------------------------------------------------------------------------------------------------------------------------|
'''

def _calc_critics(init_data: pd.DataFrame, mid_data: pd.DataFrame) -> pd.DataFrame:
    if 'critical_pressure' in init_data.columns:
        mid_data['critical_pressure'] = init_data['critical_pressure']
    else:
        mid_data['critical_pressure'] = (4.892 - 0.4048 * init_data['relative_density'])

    if 'critical_temp' in init_data.columns:
        mid_data['critical_temp'] = init_data['critical_temp']
    else:
        mid_data['critical_temp'] = 94.717 + 170.8 * init_data['relative_density']

    return mid_data

def make_input_data(init_data: pd.DataFrame) -> pd.DataFrame:
    mid_data = pd.DataFrame(
        columns = ['area_volume', 'pore_volume', 'temp_correction', 'fin_reservoir_pressure', 'critical_pressure',
                   'critical_temp', 'init_overcompress_coef', 'fin_overcompress_coef', 'geo_gas_reserves',
                   'dry_gas_init_reserves'],
        index=['value']
    )

    # Проверка и присваивание значений
    if 'area_volume' in init_data.columns:
        mid_data['area_volume'] = init_data['area_volume']
    else:
        mid_data['area_volume'] = init_data['area'] * init_data['effective_thickness']

    if 'pore_volume' in init_data.columns:
        mid_data['pore_volume'] = init_data['pore_volume']
    else:
        mid_data['pore_volume'] = mid_data['area_volume'] * init_data['porosity_coef']

    if 'temp_correction' in init_data.columns:
        mid_data['temp_correction'] = init_data['temp_correction']
    else:
        mid_data['temp_correction'] = (ZERO_C_TO_K + NORM_TEMP_C) / init_data['reservoir_temp']

    if 'fin_reservoir_pressure' in init_data.columns:
        mid_data['fin_reservoir_pressure'] = init_data['fin_reservoir_pressure']
    else:
        mid_data['fin_reservoir_pressure'] = np.exp(1293 * 1e-9 * 2700 * float(init_data['relative_density'].iloc[0])) / 1e6

    mid_data = _calc_critics(init_data, mid_data)

    if 'init_overcompress_coef' in init_data.columns:
        mid_data['init_overcompress_coef'] = init_data['init_overcompress_coef']
    else:
        mid_data['init_overcompress_coef'] = (
                (0.4 * np.log10(init_data['reservoir_temp'] / mid_data['critical_temp'])
                 + 0.73)**(init_data['init_reservoir_pressure'] / mid_data['critical_pressure'])
                + 0.1 * init_data['init_reservoir_pressure'] / mid_data['critical_pressure'])

    if 'fin_overcompress_coef' in init_data.columns:
        mid_data['fin_overcompress_coef'] = init_data['fin_overcompress_coef']
    else:
        mid_data['fin_overcompress_coef'] = (
                (0.4 * np.log10(init_data['reservoir_temp'] / mid_data['critical_temp'])
                 + 0.73)**(mid_data['fin_reservoir_pressure'] / mid_data['critical_pressure'])
                + 0.1 * mid_data['fin_reservoir_pressure'] / mid_data['critical_pressure'])

    if 'geo_gas_reserves' in init_data.columns:
        mid_data['geo_gas_reserves'] = init_data['geo_gas_reserves']
    else:
        mid_data['geo_gas_reserves'] = (init_data['area'] * 1e3
                                        * init_data['effective_thickness']
                                        * init_data['porosity_coef']
                                        * init_data['gas_saturation_coef']
                                        * init_data['init_reservoir_pressure']
                                        / mid_data['init_overcompress_coef']
                                        / PRES_STD_COND
                                        * mid_data['temp_correction'])

    if 'dry_gas_init_reserves' in init_data.columns:
        mid_data['dry_gas_init_reserves'] = init_data['dry_gas_init_reserves']
    else:
        mid_data['dry_gas_init_reserves'] = mid_data['geo_gas_reserves'] * (100 - 0.012 - 0.003 - 0.012) / 100

    init_data = pd.concat([init_data, mid_data[np.setdiff1d(mid_data.columns, init_data.columns)]], axis=1)
    return init_data


def make_init_data_for_prod_indics(init_data: pd.DataFrame) -> pd.DataFrame:
    mid_data = pd.DataFrame(
        columns = ['density_athmospheric', 'lambda_trail', 'lambda_fontain', 'macro_roughness_l', 'filtr_resistance_A',
                   'filtr_resistance_B', 'critical_pressure', 'critical_temp', 'annual_production'],
        index=['value']
    )

    # Проверка и присваивание значений
    if 'density_athmospheric' in init_data.columns:
        mid_data['density_athmospheric'] = init_data['density_athmospheric']
    else:
        mid_data['density_athmospheric'] = init_data['relative_density'] * 1.205

    if 'lambda_trail' in init_data.columns:
        mid_data['lambda_trail'] = init_data['lambda_trail']
    else:
        mid_data['lambda_trail'] = 0.067 * (2 * PIPE_ROUGHNESS / init_data['trail_diameter']) ** 0.2

    if 'lambda_fontain' in init_data.columns:
        mid_data['lambda_fontain'] = init_data['lambda_fontain']
    else:
        mid_data['lambda_fontain'] = (2 * np.log10(7.41 * init_data['pipe_diameter'] / 2 / PIPE_ROUGHNESS)) ** (-2)

    if 'macro_roughness_l' in init_data.columns:
        mid_data['macro_roughness_l'] = init_data['macro_roughness_l']
    else:
        mid_data['macro_roughness_l'] = 0.425 * 1e-9 * init_data['permeability'] ** 1.45 / 100

    if 'filtr_resistance_A' in init_data.columns:
        mid_data['filtr_resistance_A'] = init_data['filtr_resistance_A']
    else:
        mid_data['filtr_resistance_A'] = (init_data['viscosity'] * init_data['init_overcompress_coef'] * 0.1013
                                          * init_data['reservoir_temp']
                                          / (np.pi * init_data['permeability'] * init_data['effective_thickness'] * 293.15)
                                          * np.log(500 / 0.1) * 11.347 * 1e3)

    if 'filtr_resistance_B' in init_data.columns:
        mid_data['filtr_resistance_B'] = init_data['filtr_resistance_B']
    else:
        mid_data['filtr_resistance_B'] = (mid_data['density_athmospheric'] * 0.1013
                                          * init_data['init_overcompress_coef'] * init_data['reservoir_temp']
                                          / mid_data['macro_roughness_l']
                                          / (2 * np.pi**2 * init_data['effective_thickness']**2 * 293.15)
                                          * (1 / 0.1 - 1 / 500) * 10**(-6) / 86400**2 * 1e3)

    mid_data = _calc_critics(init_data, mid_data)

    if 'annual_production' in init_data.columns:
        mid_data['annual_production'] = init_data['annual_production']
    else:
        mid_data['annual_production'] = init_data['geo_gas_reserves'] * init_data['prod_rate']

    init_data = pd.concat([init_data, mid_data[np.setdiff1d(mid_data.columns, init_data.columns)]], axis=1)
    return init_data

