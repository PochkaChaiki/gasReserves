from dash import Dash
import dash_bootstrap_components as dbc

from src.callbacks.production_profiles import *
from src.callbacks.reserves_calcs import *
from src.callbacks.menu import *
from src.callbacks.single_page import *
from src.callbacks.risks import *

from src.layouts.single_page import *

import webbrowser
import requests as r
import os

APP_TITLE = 'Оценка перспективности'
DEBUG = False

app: Dash

try:
    resp = r.get(dbc.themes.BOOTSTRAP)

    resp.raise_for_status()
    app = Dash(
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
        serve_locally=True,
        include_assets_files=False,
        suppress_callback_exceptions=True,
        title=APP_TITLE,
    )

except r.exceptions.RequestException:
    app = Dash(
        serve_locally=True,
        include_assets_files=True,
        suppress_callback_exceptions=True,
        title=APP_TITLE,
    )

app.layout = Layout

if __name__ == '__main__':
    if not os.path.exists(TEMP_PATH):
        os.mkdir(TEMP_PATH)

    webbrowser.open('http://localhost:8050', new=2)
    app.run(debug=DEBUG)
