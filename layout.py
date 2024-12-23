from dash import html, dcc
import dash_bootstrap_components as dbc
from gas_reserves.constants import *

Layout = html.Div(
    [
        html.Header(
        dcc.Tabs(id="tabs-calcs", value="tab-reserves-calcs", children=[
            dcc.Tab(label="Подсчёт запасов", value="tab-reserves-calcs"),
            dcc.Tab(label="Показатели разработки", value="tab-production-indicators")
        ])),
        html.Div(id="tabs-content")
    ])

distribution_options=[
    {"label": "Нормальное", "value": "norm"}, 
    {"label": "Равномерное", "value": "uniform"},
    {"label": "Треугольное", "value": "triang"},
    {"label": "Усечённое нормальное", "value": "truncnorm"},
]

def distribution_input(name, id, placeholder):
    return html.Div([
        dbc.Label(name, id=id, html_for=id+"-select"),
        dbc.Select(distribution_options, id=id+"-select", placeholder=placeholder),
        html.Div(id=id+"-input-div")
    ])

ReservesInputGroup = dbc.Col(
    [
        distribution_input("Площадь, м2", "area", "Площадь"),

        distribution_input("Эффективная газонасыщенная толщина, м", "effective_thickness", "Толщина"),

        distribution_input("Коэффициент пористости, д.е", "porosity_coef", "Пористость"),

        distribution_input("Коэффициент газонасыщенности, д.е.", "gas_saturation_coef", "Газонасыщенность"),

        dbc.Label("Начальное пластовое давление, МПа", id="init_reservoir_pressure", html_for="init_reservoir_pressure-input"),
        dbc.Input(type="number", id="init_reservoir_pressure-input", placeholder="Начальное пластовое давление"),
        
        dbc.Label("Относительная плотность газа", id="relative_density", html_for="relative_density-input"),
        dbc.Input(type="number", id="relative_density-input", placeholder="Относительная плотность газа"),
        
        dbc.Label("Пластовая температура, К", id="reservoir_temp", html_for="reservoir_temp-input"),
        dbc.Input(type="number", id="reservoir_temp-input", placeholder="Пластовая температура"),
        
        # dbc.Label("Проницаемость, мД", id="permeability", html_for="permeability-input"),
        # dbc.Input(type="number", id="permeability-input", placeholder="Проницаемость"),
        
        dbc.Button("Расчитать", id="calculate_reserves_button", n_clicks=0)
    ]
)


ReservesMainOutputs = dbc.Col(
    [
        dbc.Label("Объем площади, м3", id="area_volume", html_for="area_volume-input"),
        dbc.Input(type="number", id="area_volume-input", placeholder='Объём площади', readonly=True),

        dbc.Label("Поровый объем, м3", id="pore_volume", html_for="pore_volume-input"),
        dbc.Input(type="number", id="pore_volume-input", placeholder="Поровый объем", readonly=True),
        
        dbc.Label("Поправка на температуру", id="temp_correction", html_for="temp_correction-input"),
        dbc.Input(type="number", id="temp_correction-input", placeholder="Поправка на температуру"),
        
        dbc.Label("Конечное пластовое давление, МПа", id="fin_reservoir_pressure", html_for="fin_reservoir_pressure-input"),
        dbc.Input(type="number", id="fin_reservoir_pressure-input", placeholder="Конечное пластовое давление", readonly=True),
        
        dbc.Label("Критическое давление, МПа.", id="critical_pressure", html_for="critical_pressure-input"),
        dbc.Input(type="number", id="critical_pressure-input", placeholder="Критическое давление"),
        
        dbc.Label("Критическая температура, К", id="critical_temp", html_for="critical_temp-input"),
        dbc.Input(type="number", id="critical_temp-input", placeholder="Критическая температура"),
        
        dbc.Label("Коэффициент сверхсжимаемости начальный", id="init_overcompress_coef", html_for="init_overcompress_coef-input"),
        dbc.Input(type="number", id="init_overcompress_coef-input", placeholder="Коэффициент сверхсжимаемости начальный"),
        
        dbc.Label("Коэффициент сверхсжимаемости конечный", id="fin_overcompress_coef", html_for="fin_overcompress_coef-input"),
        dbc.Input(type="number", id="fin_overcompress_coef-input", placeholder="Коэффициент сверхсжимаемости конечный", readonly=True),
        
        dbc.Label("Геологические запасы газа, млн. м3", id="geo_gas_reserves", html_for="geo_gas_reserves-input"),
        dbc.Input(type="number", id="geo_gas_reserves-input", placeholder="Геологические запасы газа", readonly=True),

        dbc.Label("Начальные запасы сухого газа, млн. м3", id="dry_gas_init_reserves", html_for="dry_gas_init_reserves-input"),
        dbc.Input(type="number", id="dry_gas_init_reserves-input", placeholder="Начальные запасы сухого газа", readonly=True),
    ]
)

ReservesOutputTable = html.Div(id="output_table")

TornadoDiagram = html.Div(id="tornado-diagram", )

IndicatorsDiagram = html.Div(id="indicators-diagram")
