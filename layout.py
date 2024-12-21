from dash import Dash, html, Input, Output, State, dcc


Layout = html.Div(
    [
        dcc.Tabs(id="tabs-calcs", value="tab-reserves-calcs", children=[
            dcc.Tab(label="Подсчёт запасов", value="tab-reserves-calcs"),
            dcc.Tab(label="Показатели разработки", value="tab-production-indicators")
        ]),
        html.Div(id="tabs-content")
    ])


