import pandas as pd
import numpy as np
import scipy.optimize as so
from src.gas_reserves.constants import *

MAX_ITERATIONS = 100



def count_daily_production(x: float, data: dict[str, float]) -> float:
    return ((-data['filtr_resistance_A']
            + np.sqrt(data['filtr_resistance_A']**2
                      + 4 * data['filtr_resistance_B']
                          * data['max_depression']
                          * (2*x - data['max_depression'])))
            / 2 / data['filtr_resistance_B'])


def count_overcomp_coef(x: float, data: dict[str, float], temp: float) -> float:
    return ((0.4 * np.log10(temp / data['critical_temp']) + 0.73)**(x / data['critical_pressure'])
            + 0.1 * x / data['critical_pressure'])

def __count_downhole_pressure(x: float, data: dict[str, float]) -> float:
    if x - data['max_depression'] > 0:
        return x - data['max_depression']
    return 0

def __count_wellhead_pressure(data: dict[str, float],
                              curr_p: float,
                              curr_d_prod: float,
                              downhole_p: float,
                              overcomp_coef: float) -> float:
    s = 0.03415 * data['relative_density'] * data['well_height'] / overcomp_coef / data['avg_well_temp']
    # using Pt instead of Pcp --->
    overcomp_coef_avg = count_overcomp_coef(curr_p, data, data['avg_well_temp'])
    theta = (0.0132 * 10**(-10) * data['lambda_fontain']
             * overcomp_coef_avg**2 * data['avg_well_temp']**2
             * (np.exp(2 * s) - 1) / data['pipe_diameter']**5)

    if downhole_p > 0 and (downhole_p**2 - theta * curr_d_prod**2) >= 0:
        return np.sqrt((downhole_p**2 - theta * curr_d_prod**2) / np.exp(2 * s))
    return 0

def __count_downhole_pressure_after_min_wellhead(data: dict[str, float],
                                                 curr_p: float,
                                                 curr_d_prod: float,
                                                 wellhead_p: float,
                                                 overcomp_coef: float) -> float:
    s = 0.03415 * data['relative_density'] * data['well_height'] / overcomp_coef / data['avg_well_temp']

    overcomp_coef_avg = count_overcomp_coef(curr_p, data, data['avg_well_temp'])
    theta = (0.0132 * 10 ** (-10) * data['lambda_fontain']
             * overcomp_coef_avg ** 2 * data['avg_well_temp'] ** 2
             * (np.exp(2 * s) - 1) / data['pipe_diameter'] ** 5)

    expr_inside_sqrt = wellhead_p**2 * np.exp(2*s) + theta * curr_d_prod**2
    if expr_inside_sqrt >= 0:
        return np.sqrt(expr_inside_sqrt)
    return 0

def __count_bcs_power(data: dict[str, float],
                      ukpg_pressure: float,
                      curr_d_prod: float,
                      n_wells: int) -> float:
    power = 0
    if data['main_gas_pipeline_pressure'] > ukpg_pressure > 0:
        power = (0.004 * curr_d_prod * n_wells * data['input_cs_temp']
                 * count_overcomp_coef(ukpg_pressure, data, data['input_cs_temp'])
                 / data['efficiency_cs'] * ADIABATIC_INDEX / (ADIABATIC_INDEX - 1)
                 * ((data['main_gas_pipeline_pressure'] / ukpg_pressure) ** ((ADIABATIC_INDEX - 1)
                                                                             / ADIABATIC_INDEX) - 1))
    return power

def __count_ukpg_pressure(data: dict[str, float],
                          wellhead_p: float,
                          downhole_p: float,
                          curr_d_prod: float,
                          n_wells: int) -> float:
    value_inside_sqrt_ukpg_pressure = (wellhead_p ** 2 - data['lambda_trail'] * data['relative_density']
                                       * count_overcomp_coef(
                2 / 3 * (downhole_p + wellhead_p ** 2 / (downhole_p + wellhead_p)),
                data,
                data['avg_well_temp'])
                                       * data['avg_trail_temp'] * data['trail_length'] * (
                                               curr_d_prod * n_wells) ** 2
                                       / data['trail_diameter'] ** 5 / COEF_K ** 2)

    if value_inside_sqrt_ukpg_pressure >= 0.1 ** 2:
        ukpg_pressure = np.sqrt(value_inside_sqrt_ukpg_pressure)
    else:
        ukpg_pressure = 0.1

    return ukpg_pressure



def __count_wellhead_and_downhole_pressures(wellhead_p: float,
                                            downhole_p: float,
                                            data: dict[str, float],
                                            curr_p: float,
                                            curr_d_prod: float,
                                            overcomp_coef: float) -> tuple[float, float, dict[str, float]]:
    if round(wellhead_p, 3) <= data['min_necessary_wellhead_pressure']:
        wellhead_p = data['min_necessary_wellhead_pressure']
        downhole_p = __count_downhole_pressure_after_min_wellhead(data,
                                                                  curr_p,
                                                                  curr_d_prod,
                                                                  wellhead_p,
                                                                  overcomp_coef)
        data['max_depression'] = curr_p - downhole_p
    else:
        downhole_p = __count_downhole_pressure(curr_p, data)
        wellhead_p = __count_wellhead_pressure(data,
                                               curr_p,
                                               curr_d_prod,
                                               downhole_p,
                                               overcomp_coef)
        if round(wellhead_p, 3) <= data['min_necessary_wellhead_pressure']:
            wellhead_p = data['min_necessary_wellhead_pressure']
            downhole_p = __count_downhole_pressure_after_min_wellhead(data,
                                                                      curr_p,
                                                                      curr_d_prod,
                                                                      wellhead_p,
                                                                      overcomp_coef)
            data['max_depression'] = curr_p - downhole_p

    return wellhead_p, downhole_p, data


def calculate_indicators(data: dict[str, float]) -> tuple[RESULT, pd.DataFrame]:
    __list_kig = []
    __list_annual_production = []
    __list_current_pressure = []
    __list_n_wells = []
    __list_wellhead_pressure = []
    __list_ukpg_pressure = []
    __list_cs_power = []
    __list_downhole_pressure = []

    current_pressure = data['init_reservoir_pressure']
    current_annual_production = 0
    sum_current_annual_production = 0
    overcompress_coef = data['init_overcompress_coef']
    kig = 0
    current_daily_production = 0
    downhole_pressure = __count_downhole_pressure(current_pressure, data)
    wellhead_pressure = __count_wellhead_pressure(data,
                                                  current_pressure,
                                                  current_daily_production,
                                                  downhole_pressure,
                                                  overcompress_coef)
    n_wells = 0
    while kig < 0.5:
        if current_daily_production * n_wells * data['operations_ratio'] * 365 / 1000 < data['annual_production']:
            n_wells += np.trunc(12 / data['time_to_build'] * data['machines_num'])
    
        def func(x):
            return [data['init_reservoir_pressure'] / data['init_overcompress_coef']
                        * (1 - sum_current_annual_production / data['geo_gas_reserves']) * x[1] - x[0],
                    count_overcomp_coef(x[0], data, data['reservoir_temp']) - x[1],
                    sum_current_annual_production + 365 * n_wells * data['operations_ratio']
                        * count_daily_production(x[0], data) / 1000 - x[2]
                    ]

        res = so.fsolve(func, [current_pressure, overcompress_coef, sum_current_annual_production], xtol=1e-3, full_output=True)
        
        root = res[0]
        current_pressure, overcompress_coef, _ = root[0], root[1], root[2]

        if res[2] != 1:
            return RESULT.EVALUATION_ERROR, pd.DataFrame(dict(
                kig = __list_kig,
                annual_production = __list_annual_production,
                current_pressure = __list_current_pressure,
                wellhead_pressure = __list_wellhead_pressure,
                downhole_pressure = __list_downhole_pressure,
                n_wells = __list_n_wells,
                ukpg_pressure = __list_ukpg_pressure,
                cs_power = __list_cs_power))
        
        current_daily_production = count_daily_production(current_pressure, data)

        current_annual_production = 365 * current_daily_production * n_wells * data['operations_ratio'] / 1000

        if current_annual_production >= data['annual_production']:
            current_annual_production = data['annual_production']
        elif len(__list_n_wells) and __list_n_wells[-1] == n_wells:
            n_wells += np.trunc(12 / data['time_to_build'] * data['machines_num'])
            __list_n_wells[-1] = n_wells
            current_annual_production = 365 * current_daily_production * n_wells * data['operations_ratio'] / 1000
            if current_annual_production > data['annual_production']:
                current_annual_production = data['annual_production']


        wellhead_pressure, downhole_pressure, data = __count_wellhead_and_downhole_pressures(wellhead_pressure,
                                                                                             downhole_pressure,
                                                                                             data,
                                                                                             current_pressure,
                                                                                             current_daily_production,
                                                                                             overcompress_coef)

        ukpg_pressure = __count_ukpg_pressure(data,
                                              wellhead_pressure,
                                              downhole_pressure,
                                              current_daily_production,
                                              n_wells)

        power = __count_bcs_power(data, ukpg_pressure, current_daily_production, n_wells)


        sum_current_annual_production += current_annual_production
        kig = sum_current_annual_production / data['geo_gas_reserves']

        __list_kig.append(kig)
        __list_annual_production.append(current_annual_production)
        __list_current_pressure.append(current_pressure)
        __list_n_wells.append(n_wells)
        __list_wellhead_pressure.append(wellhead_pressure)
        __list_ukpg_pressure.append(ukpg_pressure)
        __list_cs_power.append(power)
        __list_downhole_pressure.append(downhole_pressure)

        if len(__list_kig) > MAX_ITERATIONS:
            return RESULT.PASSED_LIMIT, pd.DataFrame(dict(
                kig=__list_kig,
                annual_production=__list_annual_production,
                current_pressure=__list_current_pressure,
                wellhead_pressure=__list_wellhead_pressure,
                downhole_pressure=__list_downhole_pressure,
                n_wells=__list_n_wells,
                ukpg_pressure=__list_ukpg_pressure,
                cs_power=__list_cs_power))



    while current_pressure > data['abandon_pressure']:

        def func(x):
            return [data['init_reservoir_pressure'] / data['init_overcompress_coef']
                        * (1 - x[2] / data['geo_gas_reserves']) * x[1] - x[0],
                    count_overcomp_coef(x[0], data, data['reservoir_temp']) - x[1],
                    sum_current_annual_production + 365 * n_wells * data['operations_ratio']
                        * (current_daily_production + count_daily_production(x[0], data))
                        / (2 * 10**6 * data['reserve_ratio']) *1e3 - x[2]
                    ]

        res = so.fsolve(func,
                        [current_pressure, overcompress_coef, sum_current_annual_production],
                        xtol=1e-3,
                        full_output=True)
        
        root = res[0]
        current_pressure, overcompress_coef, _ = root[0], root[1], root[2]
        
        if res[2] != 1:
            return RESULT.EVALUATION_ERROR, pd.DataFrame(dict(
                kig = __list_kig,
                annual_production = __list_annual_production,
                current_pressure = __list_current_pressure,
                wellhead_pressure = __list_wellhead_pressure,
                downhole_pressure = __list_downhole_pressure,
                n_wells = __list_n_wells,
                ukpg_pressure = __list_ukpg_pressure,
                cs_power = __list_cs_power))
        
        new_current_daily_production = count_daily_production(current_pressure, data)


        wellhead_pressure, downhole_pressure, data = __count_wellhead_and_downhole_pressures(wellhead_pressure,
                                                                                             downhole_pressure,
                                                                                             data,
                                                                                             current_pressure,
                                                                                             new_current_daily_production,
                                                                                             overcompress_coef)

        current_annual_production = (
                365 * n_wells * data['operations_ratio']
                / (2 * 10**6 * data['reserve_ratio'])
                * (new_current_daily_production + current_daily_production) * 1e3)

        if current_annual_production > data['annual_production']:
            current_annual_production = data['annual_production']

        current_daily_production = new_current_daily_production

        ukpg_pressure = __count_ukpg_pressure(data,
                                              wellhead_pressure,
                                              downhole_pressure,
                                              current_daily_production,
                                              n_wells)

        power = __count_bcs_power(data, ukpg_pressure, current_daily_production, n_wells)

        sum_current_annual_production += current_annual_production
        kig = sum_current_annual_production / data['geo_gas_reserves']


        __list_kig.append(kig)
        __list_annual_production.append(current_annual_production)
        __list_current_pressure.append(current_pressure)
        __list_n_wells.append(n_wells)
        __list_wellhead_pressure.append(wellhead_pressure)
        __list_downhole_pressure.append(downhole_pressure)
        __list_ukpg_pressure.append(ukpg_pressure)
        __list_cs_power.append(power)

        if len(__list_kig) > MAX_ITERATIONS:
            return RESULT.PASSED_LIMIT, pd.DataFrame(dict(
                kig=__list_kig,
                annual_production=__list_annual_production,
                current_pressure=__list_current_pressure,
                wellhead_pressure=__list_wellhead_pressure,
                downhole_pressure=__list_downhole_pressure,
                n_wells=__list_n_wells,
                ukpg_pressure=__list_ukpg_pressure,
                cs_power=__list_cs_power))
    
    return RESULT.SUCCESS, pd.DataFrame(dict(
        kig = __list_kig,
        annual_production = __list_annual_production,
        current_pressure = __list_current_pressure,
        wellhead_pressure = __list_wellhead_pressure,
        downhole_pressure = __list_downhole_pressure,
        n_wells = __list_n_wells,
        ukpg_pressure = __list_ukpg_pressure,
        cs_power = __list_cs_power))
