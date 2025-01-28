import pytest
import json
from excel_report import *


class TestExcelReportService:
    storage_data = None
    
    @pytest.fixture
    def load_storage(self):
        if self.storage_data is None: 
            with open('./tests/storage_data.json', 'r', encoding='utf8') as file:
                storage_data = json.load(file)
        return storage_data, 'Месторождение1'
    
    def test_collect_stat_params(self, load_storage):
        storage_data, field_name = load_storage
        stat_params = collect_stat_params(storage_data=storage_data,
                                          field_name=field_name)
        
        expected_keys = {'area', 'effective_thickness', 'porosity_coef', 
                         'gas_saturation_coef', 'permeability'}
        for key in expected_keys:
            assert stat_params.get(key, None)
            assert stat_params[key]['distribution'] != ''
    

    def test_collect_init_data(self, load_storage):
        storage_data, field_name = load_storage
        init_data = collect_init_data(storage_data=storage_data, 
                                      field_name=field_name)
        
        init_data_params = {'relative_density', 'reservoir_temp', 
                            'init_reservoir_pressure', 'temp_correction', 
                            'init_overcompress_coef', 'num_of_vars'}
        for key in init_data_params: 
            assert init_data.get(key, None)


    def test_collect_prod_profile_init_data(self, load_storage):
        storage_data, field_name = load_storage
        prod_profile_init_data = collect_prod_profile_init_data(
            storage_data=storage_data,
            field_name=field_name
        )

        prod_init_data_params = {'prod_rate', 'operations_ratio', 
            'reserve_ratio', 'machines_num','time_to_build', 'well_height', 
            'pipe_diameter', 'main_gas_pipeline_pressure',
            'abandon_pressure', 'filtr_resistance_A', 
            'filtr_resistance_B', 'trail_length', 
            'input_cs_temp'}
        
        for key in prod_init_data_params:
            assert prod_profile_init_data.get(key, None)


    def test_collect_profiles_report(self, load_storage):
        storage_data, field_name = load_storage
        profiles_report = collect_profiles_report(
            storage_data=storage_data,
            field_name=field_name
        )
        assert all(key in profiles_report.keys() for key in {'P10', 'P50', 'P90'})
        
        for profile in profiles_report.keys():
            assert profiles_report[profile].get('geo_gas_reserves', None)
            assert profiles_report[profile].get('effective_thickness', None)
            assert profiles_report[profile].get('porosity_coef', None)
            assert profiles_report[profile].get('gas_saturation_coef', None)
            assert profiles_report[profile].get('relative_density', None)
            assert profiles_report[profile].get('reservoir_temp', None)
            assert profiles_report[profile].get('init_reservoir_pressure', None)
            assert profiles_report[profile].get('temp_correction', None)
            assert profiles_report[profile].get('init_overcompress_coef', None)
            assert profiles_report[profile].get('annual_production', None)
            assert profiles_report[profile].get('accumulated_production', None)
            assert profiles_report[profile].get('kig', None)
            assert profiles_report[profile].get('num_of_wells', None)
            assert profiles_report[profile].get('years', None)
        
    def test_collect_images(self, load_storage):
        storage_data, field_name = load_storage

        images = collect_images(storage_data=storage_data,
                                field_name=field_name)
        
        assert images.get('hist', None)
        assert images.get('tornado', None)
        assert images.get('profile', None)
