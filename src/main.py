from dash import Dash, html, dcc, callback, Input, Output, State
from layout import *
from callbacks import *
import json

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], 
           suppress_callback_exceptions=True)

app.layout = Layout


@callback(Output('tabs-content', 'children'),
          Input('tabs-calcs', 'value'),
          State('persistence_storage', 'data'),
          )
def render_content(tab, data):
    if tab == 'tab-reserves-calcs':
        values = get_tab(data, 'Месторождение1', tab)
        return render_reserves_calcs(values)
    elif tab == 'tab-production-indicators':
        values = get_tab(data, 'Месторождение1', tab)
        return render_production_indicators(values)
    



def render_reserves_calcs(data):
    return html.Div([
        dbc.Row([
            make_reserves_input_group(data),
            make_reserves_main_outputs(data),
        ]),
        *make_output(data)
    ])

def render_production_indicators(data):
    return html.Div([
        dbc.Row([
            dbc.Col(get_production_indicators_inputs(data)),
            dbc.Col(make_prod_calcs_table(data))
        ]),
        dbc.Row([
            make_prod_indics_plots(data)
        ])
    ])



if __name__ == '__main__':
    app.run(debug=True)