import scipy.stats as st


zero_c_to_k = 273
norm_temp_c = 20
pres_std_cond = 0.101325 * 1e6

coef_K = 3326400
init_num_wells = 1
adiabatic_index = 1.3
pipe_roughness = 0.0001


distributions = {
    "norm": st.norm,
    "uniform": st.uniform,
    "triang": st.triang,
    "truncnorm": st.truncnorm,
}

varnames = {
    'area': 'Площадь, тыс. м2',
    'effective_thickness': 'Эффективная газонасыщенная толщина, м',
    'porosity_coef': 'Коэффициент пористости, д.е',
    'gas_saturation_coef': 'Коэффициент газонасыщенности, д.е.',
    'init_reservoir_pressure': 'Начальное пластовое давление, МПа',
    'relative_density': 'Относительная плотность газа, д.е.',
    'reservoir_temp': 'Пластовая температура, К',
    'area_volume': 'Объем площади, тыс. м3',
    'pore_volume': 'Поровый объем, тыс. м3',
    'temp_correction': 'Поправка на температуру, К',
    'fin_reservoir_pressure': 'Конечное пластовое давление, МПа',
    'critical_pressure': 'Критическое давление, МПа',
    'critical_temp': 'Критическая температура, К',
    'init_overcompress_coef': 'Коэффициент сверхсжимаемости начальный, д.е.',
    'fin_overcompress_coef': 'Коэффициент сверхсжимаемости конечный, д.е.',
    'geo_gas_reserves': 'Геологические запасы газа, млн. м3',
    'reserves': 'Геологические запасы газа, млн. м3',
    'dry_gas_init_reserves': 'Начальные запасы "сухого" газа, млн м3',
}

varnamesIndicators = {
    'permeability':'Проницаемость, мД',
    'init_reservoir_pressure': 'Начальное пластовое давление, МПа',
    'reservoir_temp': 'Пластовая температура, К',
    'relative_density': 'Относительная плотность газа, д.е.',
    'init_overcompress_coef': 'Коэффициент сверхсжимаемости начальный, д.е.',
    'max_depression': 'Максимальная депрессия, МПа',
    'reserve_ratio': 'Коэффициент резерва, д.е.',
    'operations_ratio': 'Коэффициент эксплуатации, д.е.',
    'porosity_coef': 'Коэффициент пористости, д.е.',
    'gas_saturation_coef': 'Коэффициент газонасыщенности, д.е.',
    'avg_well_temp': 'Средняя температура скважины, К',
    'pipe_diameter': 'Диаметр трубы, м',
    'well_height': 'Высота скважины, м',
    # 'pipe_roughness': 'Шероховатость',
    # 'init_num_wells': 'Начальное количество скважин, шт.',
    'trail_length': 'Длина шлейфа, м',
    'trail_diameter': 'Диаметр трубы шлейфа, м',
    'trail_roughness': 'Шероховатость трубы шлейфа',
    'avg_trail_temp': 'Средняя температура шлейфа, К',
    'main_gas_pipeline_pressure': 'Давление в магистральной трубе, МПа',
    'input_cs_temp': 'Входная температура на компрессорную станцию, К',
    # 'coef_K': 'Коэффициент К',
    'efficiency_cs': 'КПД, д.е.',
    # 'adiabatic_index': 'Показатель адиабаты',
    'density_athmospheric': 'Плотность атмосферного воздуха, д.е.',
    'viscosity': 'Вязкость',
    'machines_num': 'Количество установок, шт.',
    'time_to_build': 'Время на разработку одной скважины, мес',
    'annual_production': 'Годовые отборы, млн. м3',
    'effective_thickness':'Эффективная газонасыщенная толщина, м',
    "geo_gas_reserves":'Геологические запасы газа, млн. м3',
    'lambda_trail': 'Лямбда шлейфа',
    'lambda_fontain': 'Лямбда скважины',

    'macro_roughness_l':'Коэффициент макрошероховатости, д.е.',
    'filtr_resistance_A': 'Коэффициент фильтрационного сопротивления A, МПа2/(тыс.м3/сут)',
    'filtr_resistance_B': 'Коэффициент фильтрационного сопротивления B, МПа2/(тыс.м3/сут)2',


    'critical_temp': 'Критическая температура, К',
    'critical_pressure': 'Критическое давление, МПа',
}