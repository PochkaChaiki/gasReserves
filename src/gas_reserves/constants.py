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

dist_dict={
    "Нормальное": "norm", 
    "Равномерное": "uniform",
    "Треугольное": "triang",
    "Усечённое нормальное": "truncnorm",
}

back_dist_dict = {
    "norm": "Нормальное", 
    "uniform": "Равномерное",
    "triang": "Треугольное",
    "truncnorm": "Усечённое нормальное",
}

varnames = {
    'area': 'Площадь, млн. м2',
    'effective_thickness': 'Эффективная газонасыщенная толщина, м',
    'porosity_coef': 'Коэффициент пористости, д.е',
    'gas_saturation_coef': 'Коэффициент газонасыщенности, д.е.',
    'init_reservoir_pressure': 'Начальное пластовое давление, МПа',
    'relative_density': 'Относительная плотность газа, д.е.',
    'reservoir_temp': 'Пластовая температура, К',
    'area_volume': 'Объем площади, млн. м3',
    'pore_volume': 'Поровый объем, млн. м3',
    'temp_correction': 'Поправка на температуру, К',
    'fin_reservoir_pressure': 'Конечное пластовое давление, МПа',
    'critical_pressure': 'Критическое давление, МПа',
    'critical_temp': 'Критическая температура, К',
    'init_overcompress_coef': 'Коэффициент сверхсжимаемости начальный, д.е.',
    'fin_overcompress_coef': 'Коэффициент сверхсжимаемости конечный, д.е.',
    'geo_gas_reserves': 'Геологические запасы газа, млн. м3',
    'reserves': 'Геологические запасы газа, млн. м3',
    'dry_gas_init_reserves': 'Начальные запасы "сухого" газа, млн м3',
    'num_of_vars': 'Количество реализаций, шт.',
}

reversed_varnames = {
    'Площадь, млн. м2': 'area',
    'Эффективная газонасыщенная толщина, м': 'effective_thickness',
    'Коэффициент пористости, д.е': 'porosity_coef',
    'Коэффициент газонасыщенности, д.е.': 'gas_saturation_coef',
    'Начальное пластовое давление, МПа': 'init_reservoir_pressure',
    'Относительная плотность газа, д.е.': 'relative_density',
    'Пластовая температура, К': 'reservoir_temp',
    'Объем площади, млн. м3': 'area_volume',
    'Поровый объем, млн. м3': 'pore_volume',
    'Поправка на температуру, К': 'temp_correction',
    'Конечное пластовое давление, МПа': 'fin_reservoir_pressure',
    'Критическое давление, МПа': 'critical_pressure',
    'Критическая температура, К': 'critical_temp',
    'Коэффициент сверхсжимаемости начальный, д.е.': 'init_overcompress_coef',
    'Коэффициент сверхсжимаемости конечный, д.е.': 'fin_overcompress_coef',
    'Геологические запасы газа, млн. м3': 'geo_gas_reserves',  #[ 'reserves'],
    'Начальные запасы "сухого" газа, млн м3': 'dry_gas_init_reserves',
    'Количество реализаций, шт.': 'num_of_vars'
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
    'pipe_roughness': 'Шероховатость',
    'init_num_wells': 'Начальное количество скважин, шт.',
    'trail_length': 'Длина шлейфа, м',
    'trail_diameter': 'Диаметр трубы шлейфа, м',
    'trail_roughness': 'Шероховатость трубы шлейфа',
    'avg_trail_temp': 'Средняя температура шлейфа, К',
    'main_gas_pipeline_pressure': 'Давление в магистральной трубе, МПа',
    'input_cs_temp': 'Входная температура на компрессорную станцию, К',
    'coef_K': 'Коэффициент К',
    'efficiency_cs': 'КПД, д.е.',
    'adiabatic_index': 'Показатель адиабаты',
    'density_athmospheric': 'Плотность атмосферного воздуха, д.е.',
    'viscosity': 'Вязкость',
    'machines_num': 'Количество буровых установок, шт.',
    'time_to_build': 'Время на разработку одной скважины, мес',
    'annual_production': 'Годовые отборы, млн. м3',
    'effective_thickness':'Эффективная газонасыщенная толщина, м',
    "geo_gas_reserves":'Геологические запасы газа, млн. м3',
    'lambda_trail': 'Лямбда шлейфа',
    'lambda_fontain': 'Лямбда скважины',
    'prod_rate': 'Темп годовых отбор на период постоянной добычи, %',
    'abandon_pressure_rate': 'Давление забрасывания, %',

    'macro_roughness_l':'Коэффициент макрошероховатости, д.е.',
    'filtr_resistance_A': 'Коэффициент фильтрационного сопротивления A, МПа2/(тыс.м3/сут)',
    'filtr_resistance_B': 'Коэффициент фильтрационного сопротивления B, МПа2/(тыс.м3/сут)2',


    'critical_temp': 'Критическая температура, К',
    'critical_pressure': 'Критическое давление, МПа',
}

reversed_varnamesIndicators = {
    'Проницаемость, мД': 'permeability',
    'Начальное пластовое давление, МПа': 'init_reservoir_pressure',
    'Пластовая температура, К': 'reservoir_temp',
    'Относительная плотность газа, д.е.': 'relative_density',
    'Коэффициент сверхсжимаемости начальный, д.е.': 'init_overcompress_coef',
    'Максимальная депрессия, МПа': 'max_depression',
    'Коэффициент резерва, д.е.': 'reserve_ratio',
    'Коэффициент эксплуатации, д.е.': 'operations_ratio',
    'Коэффициент пористости, д.е.': 'porosity_coef',
    'Коэффициент газонасыщенности, д.е.': 'gas_saturation_coef',
    'Средняя температура скважины, К': 'avg_well_temp',
    'Диаметр трубы, м': 'pipe_diameter',
    'Высота скважины, м': 'well_height',
    'Шероховатость': 'pipe_roughness',
    'Начальное количество скважин, шт.': 'init_num_wells',
    'Длина шлейфа, м': 'trail_length',
    'Диаметр трубы шлейфа, м': 'trail_diameter',
    'Шероховатость трубы шлейфа': 'trail_roughness',
    'Средняя температура шлейфа, К': 'avg_trail_temp',
    'Давление в магистральной трубе, МПа': 'main_gas_pipeline_pressure',
    'Входная температура на компрессорную станцию, К': 'input_cs_temp',
    'Коэффициент К': 'coef_K',
    'КПД, д.е.': 'efficiency_cs',
    'Показатель адиабаты': 'adiabatic_index',
    'Плотность атмосферного воздуха, д.е.': 'density_athmospheric',
    'Вязкость': 'viscosity',
    'Количество буровых установок, шт.': 'machines_num',
    'Время на разработку одной скважины, мес': 'time_to_build',
    'Годовые отборы, млн. м3': 'annual_production',
    'Эффективная газонасыщенная толщина, м': 'effective_thickness',
    'Геологические запасы газа, млн. м3': 'geo_gas_reserves',
    'Лямбда шлейфа': 'lambda_trail',
    'Лямбда скважины': 'lambda_fontain',
    'Темп годовых отбор на период постоянной добычи, %': 'prod_rate',
    'Давление забрасывания, %': 'abandon_pressure_rate',
    'Коэффициент макрошероховатости, д.е.': 'macro_roughness_l',
    'Коэффициент фильтрационного сопротивления A, МПа2/(тыс.м3/сут)': 'filtr_resistance_A',
    'Коэффициент фильтрационного сопротивления B, МПа2/(тыс.м3/сут)2': 'filtr_resistance_B',
    'Критическая температура, К': 'critical_temp',
    'Критическое давление, МПа': 'critical_pressure'
}


locale = """d3.formatLocale({
  "decimal": ".",
  "thousands": "\u00a0",
  "grouping": [3],
  "percent": "\u202f%",
  "nan": ""
})"""