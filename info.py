# --------------------------------------------------  PACKAGES
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
from main import app    
import wikipedia
import flask
import glob
import os

# -------------------------------------------------- LOADING DATAFRAMES
from data import df_results_t
from data import dfr_new

# --------------------------------------------------  PLOTLY MAPBOX ACCESS TOKEN
px.set_mapbox_access_token(
    "pk.eyJ1IjoibWlndWVsLW92YSIsImEiOiJjbDFmNGlqZ2wwMWNyM2VtamFmcnMxY2twIn0.hSSsFzP_FRfrILsBmgc1gQ"
)

# --------------------------------------------------  COMPONENTS RANGE
# list of Years
years = [i for i in range(1950, 2022, 1)]
years = list(reversed(years))

# List of tracks
tracks_options = [dict(label=name_t, value=name_t) for name_t in df_results_t['name_t'].unique()]

# List of countries
countries = [dict(label=country, value=country) for country in df_results_t['country'].unique()]

# List of drivers
driver_options = [dict(label=name_d, value=name_d) for name_d in df_results_t['name_d'].unique()]

# List of constructors
constructors_options = [dict(label=name_c, value=name_c) for name_c in df_results_t['name_c'].unique()]

# List of DNF Status Reasons
df_dnf = dfr_new[(dfr_new['position'] == 'DNF') & (~dfr_new['status'].str.contains(r'^(?=.*Lap)'))]
status_options = [dict(label=status, value=status) for status in df_dnf['status'].unique()]


# --------------------------------------------------  LOADING CIRCUITS IMAGES
image_directory_circuits = 'tracks_png/'
list_of_images_c = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory_circuits))]
static_image_route_c = '/tracks_png/'


# --------------------------------------------------  LOADING CHAMP IMAGES

image_directory_d = 'champions_png/'
list_of_images_champ = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory_d))]
static_image_route_d = '/champions_png/'


# --------------------------------------------------  INFO LAYOUT
# --------------------------------------------------  INFO LAYOUT

info_layout = html.Div([
                    html.H1('Circuits Overhead Layouts: 2021 - 2022',
                            style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dbc.Row(children=[
    dbc.Col(
        dbc.Card([
            dbc.CardHeader("Select Circuit"),
            dbc.CardBody(children=[
                dcc.Dropdown(
                    id="circuit-dropdown",
                    options=[{'label': i, 'value': i} for i in list_of_images_c],
                    clearable=True,
                    searchable=True,
                    value=list_of_images_c[0],
                    style={"width": "300px"}),
                dcc.Loading(children=[
                    html.P(id="circuit-about-card",
                           style={"margin": "5 10px", 'margin-top': '15px'}),
                    html.Br()]),
                        ]),
                ]), width=4),
    dbc.Col(dbc.Card([
        dbc.CardHeader("Circuit Layout"),
        dbc.CardBody(children=[
            html.Img(id="circuit-image",
                     style={"height": "400px", "width": "700px"})
                    ]),
                    ]),width=8),
            ]),
html.Br(),
html.Br(),
    html.H1('Formula 1 Hall of Fame - Bio',
            style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),
    dbc.Row(children=[
    dbc.Col(
        dbc.Card([
            dbc.CardHeader("Select Champion"),
            dbc.CardBody(children=[
                dcc.Dropdown(
                    id="champ-dropdown",
                    options=[{'label': i, 'value': i} for i in list_of_images_champ],
                    clearable=True,
                    searchable=True,
                    value=list_of_images_champ[0],
                    style={"width": "300px"}),
                dcc.Loading(children=[
                    html.P(id="champ-about-card",
                           style={"margin": "5 10px", 'margin-top': '15px'}),
                    html.Br()]),
                        ]),
                ]), width=4),
    dbc.Col(dbc.Card([
        dbc.CardHeader("Champion Bio"),
        dbc.CardBody(children=[
            html.Img(id="champ-img",
                     style={"height": "400px", "width": "690px"})
                    ]),
                    ]),width=8),
            ]),
    ])


# ------------------------------------------------------CALLBACKS-------------------------------------------------------
# ------------------------------------------------------CIRCUITS--------------------------------------------------------
# ------------------------------------------------------CALLBACKS-------------------------------------------------------

@app.callback(dash.dependencies.Output('circuit-image', 'src'),
            [dash.dependencies.Input('circuit-dropdown', 'value')])

def update_image_src_circuit(value):
    return static_image_route_c + value

@app.callback(Output("circuit-about-card", "children"),
              [Input("circuit-dropdown", "value")])

def get_circuit_about_card(name):

    if name is not None:
        name = name.split(".")[0]
        return wikipedia.summary(name, sentences=3)
    else:
        raise PreventUpdate

@app.server.route('{}<image_path>.png'.format(static_image_route_c))
def serve_image_circuit(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images_c:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))

    return flask.send_from_directory(image_directory_circuits, image_name)


# ------------------------------------------------------CALLBACKS-------------------------------------------------------
# -------------------------------------------------------DRIVERS--------------------------------------------------------
# ------------------------------------------------------CALLBACKS-------------------------------------------------------

image_directory_d = 'champions_png/'
list_of_images_champ = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory_d))]
static_image_route_d = '/champions_png/'

@app.callback(dash.dependencies.Output('champ-img', 'src'),
            [dash.dependencies.Input('champ-dropdown', 'value')])

def update_image_src_driver(value):
    return static_image_route_d + value

@app.callback(Output("champ-about-card", "children"),
              [Input("champ-dropdown", "value")])

def get_champ_about_card(name):

    if name is not None:
        name = name.split(".")[0]
        return wikipedia.summary(name, sentences=3)
    else:
        raise PreventUpdate

@app.server.route('{}<image_path>.png'.format(static_image_route_d))
def serve_image_driver(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images_champ:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))

    return flask.send_from_directory(image_directory_d, image_name)
