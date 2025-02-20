import os.path

from dash import Dash

from src.callbacks.production_profiles import *
from src.callbacks.reserves_calcs import *
from src.callbacks.menu import *
from src.callbacks.single_page import *
from src.callbacks.risks import *

from src.layouts.single_page import *

app = Dash(# external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           # assets_folder='assets',
           suppress_callback_exceptions=True)

app.layout = Layout

if __name__ == '__main__':
    if not os.path.exists(TEMP_PATH):
        os.mkdir(TEMP_PATH)

    app.run(debug=True)