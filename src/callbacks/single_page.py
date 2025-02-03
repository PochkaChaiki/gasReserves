from dash import callback, Output, Input, State, ALL, ctx, no_update

from src.layouts.single_page import *
from src.layouts.reserves_calcs import render_reserves_calcs
from src.layouts.production_profiles import render_production_indicators
from src.utils import *


@callback(
    Output('main-contents', 'children'),
    Output('current_field', 'children', allow_duplicate=True),

    Input({'type': 'open_field', 'index': ALL}, 'n_clicks'),
    State('menu_nav', 'children'),
    Input('current_field', 'children'),
    prevent_initial_call=True
)
def show_main_contents(n_clicks, field_items, current_field):
    if len(ctx.triggered) == 1 and ctx.triggered_id and ctx.triggered[0]['value']:
        field_name = ''
        hashed_id = ctx.triggered_id['index'][len('open_'):]
        for field in field_items:
            if field['props']['id'] == hashed_id:
                field_name = field['props']['children'][0]['props']['children'][1]['props']['children']
                break

        return make_main_contents(), field_name
    elif current_field and len(current_field) > 0:
            return no_update, no_update
    else:
        return make_front_page(), ''


@callback(
    Output('tabs-content', 'children'),

    Input('tabs-calcs', 'value'),
    State('persistence_storage', 'data'),
    State('current_field', 'children'),
)
def render_content(tab, data, field_name):
    if tab == 'tab-reserves-calcs':
        values = get_tab(data, field_name, tab)
        return render_reserves_calcs(values)
    elif tab == 'tab-production-indicators':
        values = get_tab(data, field_name, tab)
        return render_production_indicators(values)