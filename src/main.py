from dash import Dash
from src.layouts import *
from src.callback import *
from src.utils import *

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
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
    


if __name__ == '__main__':
    app.run(debug=True)