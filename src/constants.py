
DISABLE_CELL_COLOR = '#EEEEEE'

CHART_COLORS = [
    '#2FB4E9',
    '#F38B00',
    '#3FBFAD',
    '#9193E9',
    '#004077',
    '#FF5733',
    '#FFC300',
    '#B3DEE2',
    '#B4B4DC',
    '#A63B36',
    '#A6703A',
]


DIST_DICT={
    "Нормальное": "norm",
    "Равномерное": "uniform",
    "Треугольное": "triang",
    "Усечённое нормальное": "truncnorm",
}

VARNAMES = {
    'area': 'Площадь залежи, тыс. м2',
    'effective_thickness': 'Эффективная газонасыщенная толщина, м',
    'porosity_coef': 'Коэффициент пористости, д.е.',
    'gas_saturation_coef': 'Коэффициент газонасыщенности, д.е.',
    'init_reservoir_pressure': 'Начальное пластовое давление, МПа',
    'relative_density': 'Относительная плотность газа, д.е.',
    'reservoir_temp': 'Пластовая температура, К',
    'area_volume': 'Объем газонасыщенной породы, тыс. м3',
    'pore_volume': 'Поровый объем, тыс. м3',
    'temp_correction': 'Поправка на температуру, К',
    'fin_reservoir_pressure': 'Конечное пластовое давление, МПа',
    'critical_pressure': 'Критическое давление, МПа',
    'critical_temp': 'Критическая температура, К',
    'init_overcompress_coef': 'Коэффициент сверхсжимаемости начальный, д.е.',
    'fin_overcompress_coef': 'Коэффициент сверхсжимаемости конечный, д.е.',
    'geo_gas_reserves': 'Геологические запасы газа, млн. м3',
    'dry_gas_init_reserves': 'Начальные запасы "сухого" газа, млн м3',
    'num_of_vars': 'Количество реализаций, шт.',
}

REVERSED_VARNAMES = { val: key for key, val in VARNAMES.items()}


DISPLAY_VARNAMES_INDICATORS = {
    'year': 'Год',
    'avg_production': 'Средний дебит скважины, млн. м3',
    'annual_production': 'Годовые отборы, млн. м3',
    'kig': 'Коэффициент извлечения газа, д.е.',
    'current_pressure': 'Пластовое давление, МПа',
    'wellhead_pressure': 'Устьевое давление, МПа',
    'downhole_pressure': 'Забойное давление, МПа',
    'ukpg_pressure': 'Давление на УКПГ, МПа',
    'cs_power': 'Мощность ДКС, КВт',
    'n_wells': 'Количество скважин, шт.',
}

SHORTNAMES_VARNAMES_INDICATORS = {
    'year': 'Год',
    'avg_production': 'Qскв, млн. м3',
    'annual_production': 'Qгод, млн. м3',
    'kig': 'КИГ, д.е.',
    'current_pressure': 'Pпл, МПа',
    'wellhead_pressure': 'Pуст, МПа',
    'downhole_pressure': 'Pзаб, МПа',
    'ukpg_pressure': 'Pукпг, МПа',
    'cs_power': 'N, КВт',
    'n_wells': 'Nскв, шт.',
}

VARNAMES_INDICATORS = {
    'permeability':'Проницаемость, 1e(-3) мкм^2',
    'init_reservoir_pressure': 'Начальное пластовое давление, МПа',
    'reservoir_temp': 'Пластовая температура, К',
    'relative_density': 'Относительная плотность газа, д.е.',
    'init_overcompress_coef': 'Коэффициент сверхсжимаемости начальный, д.е.',
    'porosity_coef': 'Коэффициент пористости, д.е.',
    'gas_saturation_coef': 'Коэффициент газонасыщенности, д.е.',
    'max_depression': 'Максимальная депрессия, МПа',
    'reserve_ratio': 'Коэффициент резерва, д.е.',
    'operations_ratio': 'Коэффициент эксплуатации, д.е.',
    'avg_well_temp': 'Средняя температура по стволу скважины, К',
    'pipe_diameter': 'Диаметр трубы, м',
    'well_height': 'Глубина скважины, м',
    'PIPE_ROUGHNESS': 'Шероховатость',
    'init_num_wells': 'Начальное количество скважин, шт.',
    'trail_length': 'Длина шлейфа, м',
    'trail_diameter': 'Диаметр трубы шлейфа, м',
    'trail_roughness': 'Шероховатость трубы шлейфа',
    'avg_trail_temp': 'Средняя температура шлейфа, К',
    'main_gas_pipeline_pressure': 'Давление на УКПГ, МПа',
    'input_cs_temp': 'Входная температура на компрессорную станцию, К',
    'COEF_K': 'Коэффициент К',
    'efficiency_cs': 'КПД, д.е.',
    'ADIABATIC_INDEX': 'Показатель адиабаты',
    'density_athmospheric': 'Плотность атмосферного воздуха, д.е.',
    'viscosity': 'Вязкость, мПа*с',
    'machines_num': 'Количество буровых установок, шт.',
    'time_to_build': 'Время строительства одной скважины, мес',
    'annual_production': 'Годовые отборы, млн. м3',
    'effective_thickness':'Эффективная газонасыщенная толщина, м',
    "geo_gas_reserves":'Геологические запасы газа, млн. м3',
    'lambda_trail': 'Лямбда шлейфа',
    'lambda_fontain': 'Лямбда скважины',
    'prod_rate': 'Темп годовых отборов на период постоянной добычи, д.е.',
    'abandon_pressure': 'Давление забрасывания, МПа',
    'min_necessary_wellhead_pressure': 'Минимальное устьевое давление, МПа',

    'macro_roughness_l':'Коэффициент макрошероховатости, д.е.',
    'filtr_resistance_A': 'Коэффициент фильтрационного сопротивления A, МПа2/(тыс.м3/сут)',
    'filtr_resistance_B': 'Коэффициент фильтрационного сопротивления B, МПа2/(тыс.м3/сут)2',


    'critical_temp': 'Критическая температура, К',
    'critical_pressure': 'Критическое давление, МПа',
}

REVERSED_VARNAMES_INDICATORS = {VARNAMES_INDICATORS[key]: key for key in VARNAMES_INDICATORS}


LOCALE = """d3.formatLocale({
  "decimal": ".",
  "thousands": "\u00a0",
  "grouping": [3],
  "percent": "\u202f%",
  "nan": ""
})"""


VARNAMES_RISKS = {
    'seismic_exploration_work': 'Сейсморазведочные работы',
    'grid_density': 'Плотность сетки разведочного бурения',
    'core_research': 'Керновые исследования',
    'c1_reserves': 'Доля запасов категории С1',
    'HYDROCARBON_PROPERTIES': 'Физико-химические свойства углеводородов',
    'exploration_wells_amount': 'Количество разведочных скважин с проведением ГИС',
    'distance_from_infra': 'Удаленность от существующей инфраструктуры, км',
    'study_coef': 'Коэффициент изученности, д.е.',
}




VARNAMES_ANALYSIS = {
    'area': VARNAMES['area'],
    'study_coef': VARNAMES_RISKS['study_coef'],
    'uncertainty_coef': 'Коэффициент неопределённости, д.е.',
    'annual_production': 'Годовые отборы на период постоянной добычи, млн. м3',
    'distance_from_infra': VARNAMES_RISKS['distance_from_infra'],
    'accumulated_production': 'Накопленная добыча газа, млн. м3',
}

