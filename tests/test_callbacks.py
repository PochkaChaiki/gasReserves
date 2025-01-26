from src import callback as c
from src import callbacks as cs
import pytest
from src.gas_reserves.constants import *


import pandas as pd
import plotly.graph_objects as go

# def test_calculate_reserves_callback():
#     p_a = [{'parameter': 'Площадь, тыс. м2', 'distribution': "Нормальное", 'mean': 38860, 'std_dev': 3650}]
#     p_et = [{'parameter': 'Эффективная газонасыщенная толщина, м', 'distribution': "Нормальное", 'mean': 11.1, 'std_dev': 0.87}]
#     p_pc = [{'parameter': 'Коэффициент пористости, д.е', 'distribution': "Нормальное", 'mean': 0.09, 'std_dev': 0.01}]
#     p_gsc = [{'parameter': 'Коэффициент газонасыщенности, д.е.', 'distribution': "Нормальное", 'mean': 0.7, 'std_dev': 0.01}]
#     params = [
#         {'parameter': 'Начальное пластовое давление, МПа', 'value': 32.3},
#         {'parameter': 'Относительная плотность газа, д.е.', 'value': 0.63},
#         {'parameter': 'Пластовая температура, К', 'value': 320.49},
#         {'parameter': 'Количество реализаций, шт.', 'value': 3000},
#     ]

#     # add_params = [
#     #     {'parameter': 'Объем площади, тыс. м3', 'value': 32.3},
#     #     {'parameter': 'Поровый объем, тыс. м3', 'value': 0.63},
#     #     {'parameter': 'Поправка на температуру, К', 'value': 0.93},
#     # ]
#     add_params = []

#     output = c.calculate_gas_reserves(1, p_a, p_et, p_pc, p_gsc, params, add_params)
#     assert output


class TestCallbackReservesCalcs:
    p_area = [
        ([{'parameter': varnames['area'], 'distribution': "Нормальное", 'mean': 38860, 'std_dev': 3650}]),
    ]
    p_effective_thickness = [
        ([{'parameter': varnames['effective_thickness'], 'distribution': "Нормальное", 'mean': 11.1, 'std_dev': 0.87}])
    ]
    p_porosity_coef = [
        ([{'parameter': varnames['porosity_coef'], 'distribution': "Нормальное", 'mean': 0.09, 'std_dev': 0.01}])
    ]
    p_gas_saturation_coef = [
        ([{'parameter': varnames['gas_saturation_coef'], 'distribution': "Нормальное", 'mean': 0.7, 'std_dev': 0.01}])
    ]
    params = [
        ([
            {'parameter': varnames['init_reservoir_pressure'], 'value': 32.3},
            {'parameter': varnames['relative_density'], 'value': 0.63},
            {'parameter': varnames['reservoir_temp'], 'value': 320.49},
            {'parameter': varnames['num_of_vars'], 'value': 3000},
        ])
    ]
    add_params = [
        ([
            {'parameter': varnames['area_volume'], 'value': 32.3},
            {'parameter': varnames['pore_volume'], 'value': 0.63},
            {'parameter': varnames['temp_correction'], 'value': 0.93},
            {'parameter': varnames['fin_reservoir_pressure'], 'value': None},
            {'parameter': varnames['critical_pressure'], 'value': None},
            {'parameter': varnames['critical_temp'], 'value': None},
            {'parameter': varnames['init_overcompress_coef'], 'value': None},
            {'parameter': varnames['fin_overcompress_coef'], 'value': None},
            {'parameter': varnames['geo_gas_reserves'], 'value': None},
            {'parameter': varnames['dry_gas_init_reserves'], 'value': None},    
        ]), 
        ([
            {'parameter': varnames['area_volume'], 'value': None},
            {'parameter': varnames['pore_volume'], 'value': None},
            {'parameter': varnames['temp_correction'], 'value': 0.93},
            {'parameter': varnames['fin_reservoir_pressure'], 'value': None},
            {'parameter': varnames['critical_pressure'], 'value': None},
            {'parameter': varnames['critical_temp'], 'value': None},
            {'parameter': varnames['init_overcompress_coef'], 'value': None},
            {'parameter': varnames['fin_overcompress_coef'], 'value': None},
            {'parameter': varnames['geo_gas_reserves'], 'value': None},
            {'parameter': varnames['dry_gas_init_reserves'], 'value': None},    
        ])
    ]

    storage_data = [
        ({
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
                }
            }
        })
    ]

    @pytest.mark.parametrize('add_params', add_params)
    @pytest.mark.parametrize('p_area', p_area)
    @pytest.mark.parametrize('p_effective_thickness', p_effective_thickness)
    @pytest.mark.parametrize('p_porosity_coef', p_porosity_coef)
    @pytest.mark.parametrize('p_gas_saturation_coef', p_gas_saturation_coef)
    @pytest.mark.parametrize('params', params)
    def test_prepare_inputs(self,
                            p_area,
                            p_effective_thickness,
                            p_porosity_coef,
                            p_gas_saturation_coef,
                            params,
                            add_params):
        input_data, stat_data = cs.callback_reserves_calcs.prepare_inputs(p_area, 
                                                                          p_effective_thickness, 
                                                                          p_porosity_coef, 
                                                                          p_gas_saturation_coef, 
                                                                          params, 
                                                                          add_params)

        assert isinstance(input_data, pd.DataFrame)
        assert isinstance(stat_data, pd.DataFrame)

        expected_columns = [
            'area', 
            'effective_thickness', 
            'porosity_coef', 
            'gas_saturation_coef', 
            'init_reservoir_pressure', 
            'relative_density', 
            'reservoir_temp', 
            'num_of_vars', 
            'area_volume',
            'pore_volume',
            'temp_correction',
            'fin_reservoir_pressure',
            'critical_pressure',
            'critical_temp',
            'init_overcompress_coef',
            'fin_overcompress_coef',
            'geo_gas_reserves',
            'dry_gas_init_reserves',]
        assert all(col in input_data.columns for col in expected_columns)

        expected_stat_columns = ['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef']
        assert all(col in stat_data.columns for col in expected_stat_columns)

    @pytest.fixture
    def fixt_prepare_inputs(self):
        input_data, stat_data = cs.callback_reserves_calcs.prepare_inputs(self.p_area[0], 
                                                                          self.p_effective_thickness[0], 
                                                                          self.p_porosity_coef[0], 
                                                                          self.p_gas_saturation_coef[0], 
                                                                          self.params[0], 
                                                                          self.add_params[0])
        return input_data, stat_data

    
    def test_calculate(self, fixt_prepare_inputs):
        input_data, stat_data = fixt_prepare_inputs

        result_df, tornado_fig, ecdf_fig, pdf_fig = cs.callback_reserves_calcs.calculate(input_data, stat_data)
        assert isinstance(result_df, pd.DataFrame)
        assert isinstance(tornado_fig, go.Figure)
        assert isinstance(ecdf_fig, go.Figure)
        assert isinstance(pdf_fig, go.Figure)

        expected_columns = ['P90', 'P50', 'P10']
        assert all(col in result_df.columns for col in expected_columns)

        expected_index = [
            varnames['geo_gas_reserves'],
            varnames['area'],
            varnames['effective_thickness'],
            varnames['porosity_coef'],
            varnames['gas_saturation_coef']
        ]
        assert all(idx in result_df.index for idx in expected_index)

        for ind in expected_index:
            for col in expected_columns: 
                assert result_df.loc[ind, col] is not None

    @pytest.fixture
    def fixt_prepare_inputs_and_calculate(self, fixt_prepare_inputs):
        
        input_data, stat_data = fixt_prepare_inputs
        result_df, _, _, _ = cs.callback_reserves_calcs.calculate(input_data, stat_data)

        return result_df, input_data

    @pytest.mark.parametrize('storage_data', storage_data)
    def test_save_data_to_profiles_tab(self, storage_data, fixt_prepare_inputs_and_calculate):
        result_df, input_data = fixt_prepare_inputs_and_calculate
        save_data = cs.callback_reserves_calcs.save_data_to_profiles_tab(storage_data, 'field_name', result_df, input_data)
        print(save_data)
        for prop in ('parameter_table_stat_indics', 
                     'parameter_table_indics', 
                     'parameter_table_indics_collapse',
                     ):
            val = save_data['field_name']['tab-production-indicators'][prop]
            assert val is not None and val != {}