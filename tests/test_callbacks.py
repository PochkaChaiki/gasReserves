from src import callbacks as c


def test_calculate_reserves_callback():
    p_a = [{'parameter': 'Площадь, тыс. м2', 'distribution': "Нормальное", 'mean': 38860000, 'std_dev': 3650000}]
    p_et = [{'parameter': 'Эффективная газонасыщенная толщина, м', 'distribution': "Нормальное", 'mean': 11.1, 'std_dev': 0.87}]
    p_pc = [{'parameter': 'Коэффициент пористости, д.е', 'distribution': "Нормальное", 'mean': 0.09, 'std_dev': 0.01}]
    p_gsc = [{'parameter': 'Коэффициент газонасыщенности, д.е.', 'distribution': "Нормальное", 'mean': 0.7, 'std_dev': 0.01}]
    params = [
        {'parameter': 'Начальное пластовое давление, МПа', 'value': 32.3},
        {'parameter': 'Относительная плотность газа, д.е.', 'value': 0.63},
        {'parameter': 'Пластовая температура, К', 'value': 320.49},
        {'parameter': 'Количество реализаций, шт.', 'value': 3000},
    ]

    # add_params = [
    #     {'parameter': 'Объем площади, тыс. м3', 'value': 32.3},
    #     {'parameter': 'Поровый объем, тыс. м3', 'value': 0.63},
    #     {'parameter': 'Поправка на температуру, К', 'value': 0.93},
    # ]
    add_params = []

    output = c.calculate_gas_reserves(1, p_a, p_et, p_pc, p_gsc, params, add_params)
    assert output