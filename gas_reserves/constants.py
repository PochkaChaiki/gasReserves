import scipy.stats as st


amount_of_vars = 3000
zero_c_to_k = 273
norm_temp_c = 20
pres_std_cond = 0.101325 * 1e6

distributions = {
    "norm": st.norm,
    "uniform": st.uniform,
    "triang": st.triang,
    "truncnorm": st.truncnorm,
}

varnames = {
    "area":'Площадь, тыс. м2',
    "effective_thickness":'Эффективная газонасыщенная толщина, м',
    "porosity_coef":'Коэффициент пористости, д.е',
    "gas_saturation_coef":'Коэффициент газонасыщенности, д.е.',
    "init_reservoir_pressure":'Начальное пластовое давление, МПа',
    "relative_density":'Относительная плотность газа',
    "reservoir_temp":'Пластовая температура, К',
    "permeability":'Проницаемость, мД',
    "area_volume":'Объем площади, тыс. м3',
    "pore_volume":'Поровый объем, тыс. м3',
    "temp_correction":'Поправка на температуру',
    "fin_reservoir_pressure":'Конечное пластовое давление, МПа',
    "critical_pressure":'Критическое давление, МПа',
    "critical_temp":'Критическая температура, К',
    "init_overcompress_coef":'Коэффициент сверхсжимаемости начальный',
    "fin_overcompress_coef":'Коэффициент сверхсжимаемости конечный',
    "geo_gas_reserves":'Геологические запасы газа, млн. м3',
    "reserves":'Геологические запасы газа, млн. м3',
    "dry_gas_init_reserves":'Начальные запасы "сухого" газа, млн м3',
}