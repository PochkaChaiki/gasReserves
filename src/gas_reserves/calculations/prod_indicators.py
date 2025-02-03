import pandas as pd
import numpy as np
import scipy.optimize as so
from src.gas_reserves.constants import *


def count_daily_production(x, data):
    return ((-data['filtr_resistance_A']
            + np.sqrt(data['filtr_resistance_A']**2
                      + 4 * data['filtr_resistance_B']
                          * data['max_depression']
                          * (2*x - data['max_depression'])))
            / 2 / data['filtr_resistance_B'])


def count_overcomp_coef(x, data, temp):
    return ((0.4 * np.log10(temp / data['critical_temp']) + 0.73)**(x / data['critical_pressure'])
            + 0.1 * x / data['critical_pressure'])

def __count_downhole_pressure(x, data):
    if x - data['max_depression'] > 0:
        return x - data['max_depression']
    return 0

def __count_wellhead_pressure(data, curr_p, curr_d_prod, downhole_p, overcomp_coef):
    s = 0.03415 * data['relative_density'] * data['well_height'] / overcomp_coef / data['avg_well_temp']
    # using Pt instead of Pcp --->
    overcomp_coef_avg = count_overcomp_coef(curr_p, data, data['avg_well_temp'])
    theta = (0.0132 * 10**(-10) * data['lambda_fontain']
             * overcomp_coef_avg**2 * data['avg_well_temp']**2
             * (np.exp(2 * s) - 1) / data['pipe_diameter']**5)

    if downhole_p > 0 and (downhole_p**2 - theta * curr_d_prod**2) >= 0:
        return np.sqrt((downhole_p**2 - theta * curr_d_prod**2) / np.exp(2 * s))
    return 0


def calculate_indicators(data):
    __list_kig = []
    __list_annual_production = []
    __list_current_pressure = []
    __list_n_wells = []
    __list_wellhead_pressure = []
    __list_ukpg_pressure = []
    __list_cs_power = []


    current_pressure = data['init_reservoir_pressure']
    current_annual_production = 0
    sum_current_annual_production = 0
    overcompress_coef = data['init_overcompress_coef']
    kig = 0
    current_daily_production = 0
    downhole_pressure = 0
    n_wells = 0

    while kig < 0.5:
        if current_daily_production * n_wells * data['operations_ratio'] * 365 / 1000 <= data['annual_production']:
            n_wells += np.trunc(12 / (data['machines_num'] * data['time_to_build']))
    
        def func(x):
            return [data['init_reservoir_pressure'] / data['init_overcompress_coef'] * (1 - sum_current_annual_production / data['geo_gas_reserves']) * x[1] - x[0],
                    count_overcomp_coef(x[0], data, data['reservoir_temp']) - x[1],
                    sum_current_annual_production + 365 * n_wells * data['operations_ratio'] * count_daily_production(x[0], data) / 1000 - x[2]]

        res = so.fsolve(func, [current_pressure, overcompress_coef, sum_current_annual_production], xtol=1e-3, full_output=True)
        
        root = res[0]
        current_pressure, overcompress_coef, _ = root[0], root[1], root[2]

        if res[2] != 1:
            return pd.DataFrame(dict(
                kig = __list_kig,
                annual_production = __list_annual_production,
                current_pressure = __list_current_pressure,
                wellhead_pressure = __list_wellhead_pressure,
                n_wells = __list_n_wells,
                ukpg_pressure = __list_ukpg_pressure,
                cs_power = __list_cs_power))
        
        current_daily_production = count_daily_production(current_pressure, data)

        downhole_pressure = __count_downhole_pressure(current_pressure, data)

        wellhead_pressure = __count_wellhead_pressure(data,
                                                      current_pressure,
                                                      current_daily_production,
                                                      downhole_pressure,
                                                      overcompress_coef)

        if downhole_pressure == 0 and wellhead_pressure == 0:
            return pd.DataFrame(dict(
                kig = __list_kig,
                annual_production = __list_annual_production,
                current_pressure = __list_current_pressure,
                wellhead_pressure = __list_wellhead_pressure,
                n_wells = __list_n_wells,
                ukpg_pressure = __list_ukpg_pressure,
                cs_power = __list_cs_power))


        if 365 * current_daily_production * n_wells * data['operations_ratio'] / 1000 > data['annual_production']:
            current_annual_production = data['annual_production']
        else:
            current_annual_production = 365 * current_daily_production * n_wells * data['operations_ratio'] / 1000

        ukpg_pressure = np.sqrt(
            wellhead_pressure**2 - data['lambda_trail'] * data['relative_density']
            * count_overcomp_coef(
                2/3 * (downhole_pressure + wellhead_pressure**2 / (downhole_pressure + wellhead_pressure)),
                data, data['avg_well_temp'])
            * data['avg_trail_temp'] * data['trail_length'] * (current_daily_production * n_wells)**2
            / data['trail_diameter']**5 / coef_K**2 )

        if np.isnan(ukpg_pressure) or ukpg_pressure <= 0.1:
            ukpg_pressure = 0.1

        power = 0
        if data['main_gas_pipeline_pressure'] > ukpg_pressure > 0:
            power = 0.004 * current_daily_production * n_wells * data['input_cs_temp'] *                                                                                    \
                count_overcomp_coef(ukpg_pressure, data, data['input_cs_temp']) /                                                                                           \
                data['efficiency_cs'] * adiabatic_index / (adiabatic_index - 1) *                                                                                           \
                ((data['main_gas_pipeline_pressure']/ukpg_pressure)**((adiabatic_index - 1) / adiabatic_index) - 1)


        sum_current_annual_production += current_annual_production
        kig = sum_current_annual_production / data['geo_gas_reserves']

        __list_kig.append(kig)
        __list_annual_production.append(current_annual_production)
        __list_current_pressure.append(current_pressure)
        __list_n_wells.append(n_wells)
        __list_wellhead_pressure.append(wellhead_pressure)
        __list_ukpg_pressure.append(ukpg_pressure)
        __list_cs_power.append(power)



    while current_pressure > data['abandon_pressure'] and wellhead_pressure > 0.1:
        def func(x):
            return [data['init_reservoir_pressure'] / data['init_overcompress_coef'] * (1 - x[2] / data['geo_gas_reserves']) * x[1] - x[0],
                    count_overcomp_coef(x[0], data, data['reservoir_temp']) - x[1],
                    sum_current_annual_production + 365 * n_wells * data['operations_ratio'] * (current_daily_production + count_daily_production(x[0], data)) \
                    / (2 * 10**6 * data['reserve_ratio']) *1e3 - x[2]] #*1e3

        res = so.fsolve(func, [current_pressure, overcompress_coef, sum_current_annual_production], xtol=1e-3, full_output=True)
        
        root = res[0]
        current_pressure, overcompress_coef, _ = root[0], root[1], root[2]
        
        if res[2] != 1:
            return pd.DataFrame(dict(
                kig = __list_kig,
                annual_production = __list_annual_production,
                current_pressure = __list_current_pressure,
                wellhead_pressure = __list_wellhead_pressure,
                n_wells = __list_n_wells,
                ukpg_pressure = __list_ukpg_pressure,
                cs_power = __list_cs_power))
        
        new_current_daily_production = count_daily_production(current_pressure, data)


        downhole_pressure = __count_downhole_pressure(current_pressure, data)

        wellhead_pressure = __count_wellhead_pressure(data,
                                                      current_pressure,
                                                      new_current_daily_production,
                                                      downhole_pressure,
                                                      overcompress_coef)

        if downhole_pressure == 0 and wellhead_pressure == 0:
            return pd.DataFrame(dict(
                kig = __list_kig,
                annual_production = __list_annual_production,
                current_pressure = __list_current_pressure,
                wellhead_pressure = __list_wellhead_pressure,
                n_wells = __list_n_wells,
                ukpg_pressure = __list_ukpg_pressure,
                cs_power = __list_cs_power))

        current_annual_production = (
                365 * n_wells * data['operations_ratio']
                / (2 * 10**6 * data['reserve_ratio'])
                * (new_current_daily_production + current_daily_production) * 1e3)

        current_daily_production = new_current_daily_production

        ukpg_pressure = np.sqrt(
            wellhead_pressure ** 2 - data['lambda_trail'] * data['relative_density']
            * count_overcomp_coef(
                2 / 3 * (downhole_pressure + wellhead_pressure ** 2 / (downhole_pressure + wellhead_pressure)),
                data,
                data['avg_well_temp']) \
            * data['avg_trail_temp'] * data['trail_length'] * (current_daily_production * n_wells) ** 2
            / data['trail_diameter'] ** 5 / coef_K ** 2)

        if np.isnan(ukpg_pressure) or ukpg_pressure <= 0.1:
            ukpg_pressure = 0.1

        power = 0
        if data['main_gas_pipeline_pressure'] > ukpg_pressure > 0:
            power = (0.004 * current_daily_production * n_wells * data['input_cs_temp']
                     * count_overcomp_coef(ukpg_pressure, data, data['input_cs_temp'])
                     / data['efficiency_cs'] * adiabatic_index / (adiabatic_index - 1)
                     * ((data['main_gas_pipeline_pressure']/ukpg_pressure)**((adiabatic_index - 1)
                                                                             / adiabatic_index) - 1))


        sum_current_annual_production += current_annual_production
        kig = sum_current_annual_production / data['geo_gas_reserves']


        __list_kig.append(kig)
        __list_annual_production.append(current_annual_production)
        __list_current_pressure.append(current_pressure)
        __list_n_wells.append(n_wells)
        __list_wellhead_pressure.append(wellhead_pressure)
        __list_ukpg_pressure.append(ukpg_pressure)
        __list_cs_power.append(power)
    
    return pd.DataFrame(dict(
        kig = __list_kig,
        annual_production = __list_annual_production,
        current_pressure = __list_current_pressure,
        wellhead_pressure = __list_wellhead_pressure,
        n_wells = __list_n_wells,
        ukpg_pressure = __list_ukpg_pressure,
        cs_power = __list_cs_power))



