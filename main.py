from dash import Dash, html, dcc, callback, Input, Output, State
from layout import *
from callbacks import *

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], 
           suppress_callback_exceptions=True)

app.layout = Layout


@callback(Output('tabs-content', 'children'),
          Input('tabs-calcs', 'value'))
def render_content(tab):
    if tab == 'tab-reserves-calcs':
        return render_reserves_calcs()
    elif tab == 'tab-production-indicators':
        return render_production_indicators()
    




def render_reserves_calcs():
    return html.Div([
        dbc.Row([
            ReservesInputGroup,
            ReservesMainOutputs,
        ]),
        dbc.Row([
            ReservesOutputTable,
            TornadoDiagram,
            
        ]),
        dbc.Row([
            IndicatorsDiagram
        ])])

def render_production_indicators():
    return html.Div(html.H1('Определение показателей разработки здесь<--'))



if __name__ == '__main__':
    app.run(debug=True)