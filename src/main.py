from dash import Dash, html, dcc, callback, Input, Output, State
from layout import *
from callbacks import *
import json

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], 
           suppress_callback_exceptions=True)

app.layout = Layout


@callback(Output('tabs-content', 'children'),
          Input('tabs-calcs', 'value'),
          State('calcs_storage', 'data'),
          State('indics_storage', 'data'))
def render_content(tab, data, indics_data):
    if tab == 'tab-reserves-calcs':
        return render_reserves_calcs(data)
    elif tab == 'tab-production-indicators':
        return render_production_indicators(data, indics_data)
    



def render_reserves_calcs(data):
    values = {}
    if data is not None:
        values = json.loads(data)
    return html.Div([
        dbc.Row([
            get_reserves_input_group(values),
            get_reserves_main_outputs(values),
        ]),
        dbc.Row([
            ReservesOutputTable,
            TornadoDiagram,
            
        ]),
        dbc.Row([
            ECDFDiagram,
            PDFDiagram
        ])])

def render_production_indicators(data, indics_data):
    values = {}
    indics_values = {}
    if data is not None:
        values = json.loads(data)
    if indics_data is not None:
        indics_values = json.loads(indics_data)
    return html.Div([
        dbc.Row([
            dbc.Col(get_production_indicators_inputs(values, indics_values)),
            dbc.Col(make_prod_calcs_table())
        ]),
        dbc.Row([
            PressureOnStages,
            ProdKig,
        ])
    ])



if __name__ == '__main__':
    app.run(debug=True)