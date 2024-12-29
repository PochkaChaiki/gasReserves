import gas_reserves as gr
from pytest import *
import pytest

import pandas as pd
from pandas.testing import assert_frame_equal
import scipy.stats as st



class TestStats: 
    def test_generate_stats(self):
        stat_params = {
            'area': {
                'distribution': 'norm',
                'params': {
                    'loc': 10,
                    'scale': 5,
                },
                'adds': {}
            },
            'effective_thickness': {
                'distribution': 'uniform',
                'params': {
                    'loc': 10,
                    'scale': 5,
                },
                'adds': {}
            },
            'porosity_coef': {
                'distribution': 'triang',
                'params': {
                    'loc': 10,
                    'scale': 5,
                },
                'adds': {
                    'c': 0.7
                }
            },
            'gas_saturation_coef': {
                'distribution': 'truncnorm',
                'params': {
                    'loc': 10,
                    'scale': 5,
                },
                'adds': {
                    'a': 4,
                    'b': 16,
                }
            },
        }


        stats_data = gr.stats.generate_stats(stat_params, 200)

        assert set(stats_data.columns) == set(['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef']) and len(stats_data) == 200


class TestProcessInput:
    initdata = [
        ({
            'area': 38_556 * 1e3,
            'effective_thickness': 11.10,
            'porosity_coef': 0.091,
            'gas_saturation_coef': 0.7,
            'init_reservoir_pressure': 32.30 * 1e6,
            'relative_density': 0.6348,
            'reservoir_temp': 320.49,
        }),
        ({
            'area': 38_556 * 1e3,
            'effective_thickness': 11.10,
            'porosity_coef': 0.091,
            'gas_saturation_coef': 0.7,
            'init_reservoir_pressure': 32.30 * 1e6,
            'relative_density': 0.6348,
            'reservoir_temp': 320.49,
            'area_volume': 99*1e6,
            'fin_reservoir_pressure': 0
        }),
    ]

    @pytest.mark.parametrize('init_data', initdata)
    def test_make_input_data(self, init_data):
        df_init_data = pd.DataFrame(init_data, index=['value'])
        pr_df = gr.process_input.make_input_data(df_init_data) 
        res_cols = ['area_volume', 'pore_volume', 'temp_correction', 'fin_reservoir_pressure', 'critical_pressure', 'critical_temp', 'init_overcompress_coef',
                    'fin_overcompress_coef', 'geo_gas_reserves', 'dry_gas_init_reserves', 'area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef',
                    'init_reservoir_pressure', 'relative_density', 'reservoir_temp']
        assert len(pr_df.columns) == len(res_cols) and set(pr_df.columns) == set(res_cols) and len(df_init_data) == len(pr_df)

    init_indics_data = [dict(
        init_reservoir_pressure=32.5, 
        reservoir_temp=320,
        relative_density=0.63,
        init_overcompress_coef=0.94,
        max_depression=2,
        reserve_ratio=1.05,
        operations_ratio=0.94,
        porosity_coef=0.09,
        gas_saturation_coef=0.7,
        avg_well_temp=320,
        pipe_diameter=0.114,
        well_height=2700,
        trail_length=2300,
        trail_diameter=0.168,
        trail_roughness=0.0001,
        avg_trail_temp=310,
        main_gas_pipeline_pressure=4,
        input_cs_temp=310,
        efficiency_cs=0.87,
        viscosity=0.012,
        machines_num=1,
        time_to_build=6,
        annual_production=360.47,
        # filtr_resistance_A=,
        # filtr_resistance_B=,
        # critical_temp=,
        # critical_pressure=,
        effective_thickness=11.1,
        geo_gas_reserves=8800,
        permeability=9.57,
    )]

    @pytest.mark.parametrize('init_data', init_indics_data)
    def test_make_init_data_for_prod_indics(self, init_data):
        df_init_data = pd.DataFrame(init_data, index=['value'])
        pr_df = gr.process_input.make_init_data_for_prod_indics(df_init_data) 
        res_cols = ['init_reservoir_pressure', 'reservoir_temp', 'relative_density', 'init_overcompress_coef', 'max_depression', 'reserve_ratio', 'operations_ratio',
                    'porosity_coef', 'gas_saturation_coef', 'avg_well_temp', 'pipe_diameter', 'well_height', 'trail_length', 'trail_diameter', 'avg_trail_temp',
                    'main_gas_pipeline_pressure', 'input_cs_temp', 'efficiency_cs', 'viscosity', 'machines_num', 'time_to_build', 'annual_production', 'effective_thickness', 
                    'geo_gas_reserves', 'permeability', 'trail_roughness',
                    'density_athmospheric', 'lambda_trail', 'lambda_fontain', 'macro_roughness_l', 'filtr_resistance_A',
                    'filtr_resistance_B', 'critical_pressure', 'critical_temp']
        assert len(pr_df.columns) == len(res_cols) and set(pr_df.columns) == set(res_cols) and len(df_init_data) == len(pr_df)


def test_calculate_reserves():
    pass