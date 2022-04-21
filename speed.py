# --------------------------------------------------  PACKAGES
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from main import app

# -------------------------------------------------- LOADING DATAFRAMES
from data import dfr_new
from data import df_results_t
from data import total_points
from data import total_points_team

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

# ------------------------------------------------------DROPDOWNS-------------------------------------------------------

drop_const = dcc.Dropdown(id='dropdown_constructors',
                          placeholder="Select the Constructor",
                          options=constructors_options,
                          value=['Mercedes', 'Red Bull', 'Ferrari'],
                          multi=True,
                          )

drop_driver = dcc.Dropdown(id='driver_drop',
                           options=driver_options,
                           placeholder="Select the Driver",
                           value=['Lewis Hamilton', 'Max Verstappen','Sebastian Vettel'],
                           multi=True,
                           )

drop_tracks = dcc.Dropdown(id='track_drop',
                           options=tracks_options,
                           placeholder="Select the Track",
                           value=['Australian Grand Prix'],
                           )

drop_years = dcc.Dropdown(id='dropdown_years',
                          placeholder="Select the Championship Year",
                          options=years,
                          value=2021,
                          )

# -------------------------------------------------- SUB TABS LAYOUT
# -------------------------------------------------- SUB TABS LAYOUT
# -------------------------------------------------- SUB TABS LAYOUT

tabs_styles = {
    'height': '33px'}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'}

line_layout = html.Div([
    html.H4('Points Evolution per Driver & Constructor  2000 - 2021',
            style={'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dcc.Tabs(id="points_line", value='points_line', children=[

        dcc.Tab(label='Constructors Points Evolution', value='cons_line', style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(label='Drivers Points Evolution', value='drivers_line', style=tab_style,
                selected_style=tab_selected_style)

    ], style=tabs_styles),
    html.Br(),
    html.Div(id='points_content')
])


# -------------------------------------------------- SUB TABS CALLBACK
# -------------------------------------------------- SUB TABS CALLBACK

@app.callback(
    Output("points_content", "children"),
    [Input("points_line", "value")]
)
def seperator_switch(tab):
    if tab == "cons_line":
        return cons_line_p
    elif tab == "drivers_line":
        return drivers_line_p
    else:
        print("I hate my life")


# ------------------------------------------------------LAYOUT------------------------------------------------------
# -----------------------------------------------------LINE CONST------------------------------------------------------
# ------------------------------------------------------LAYOUT-------------------------------------------------


cons_line_p = html.Div([

    html.H1('Points per Constructor: 2000 - 2021',
            style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),
    html.Div([
        dbc.Row(children=[
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Optional Filters"),
                    dbc.CardBody(children=[
                        html.Label('Please select Constructors'),
                        drop_const,
                        html.Br(),
                        html.Label('Please select Year'),
                        drop_years,
                        html.Br(),
                        dcc.Loading(children=[
                            html.P(id="drivers_line",
                                   style={"margin": "5 10px", 'margin-top': '15px'}),
                            html.Br()]),
                    ]),
                ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Drivers Points per Round"),
                dbc.CardBody(children=[
                    dcc.Graph(id="line_c")
                ]),
            ]), width=9),
        ]),
    ]),
    html.Br(),
    html.Br(),
]),

# -----------------------------------------------------CALLBACKS-------------------------------------------------------
# ----------------------------------------------------CONSTRUCTORS------------------------------------------------------
# -----------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(
    Output("line_c", "figure"),
    Input("dropdown_constructors", "value"))
def update_line_chart_c(constructors):
    df = px.data.gapminder()  # replace with your own data source
    mask = total_points_team.Team.isin(constructors)
    fig = px.line(total_points_team[mask],
                  x="Year", y="Points", color='Team')
    return fig

# ------------------------------------------------------LAYOUT------------------------------------------------------
# -----------------------------------------------------LINE DRIVER------------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------

drivers_line_p = html.Div([

    html.H1('Points per Driver: 2000 - 2021',
            style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),
    html.Div([
        dbc.Row(children=[
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Optional Filters"),
                    dbc.CardBody(children=[
                        html.Label('Please select Drivers'),
                        drop_driver,
                        html.Br(),
                        html.Label('Please select Year'),
                        drop_years,
                        html.Br(),
                        dcc.Loading(children=[
                            html.P(id="drivers_line",
                                   style={"margin": "5 10px", 'margin-top': '15px'}),
                            html.Br()]),
                    ]),
                ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Drivers Points per Round"),
                dbc.CardBody(children=[
                    dcc.Graph(id="line_d")
                ]),
            ]), width=9),
        ]),
    ]),
    html.Br(),
    html.Br(),
]),


# -----------------------------------------------------CALLBACKS-------------------------------------------------------
# ----------------------------------------------------CONSTRUCTORS------------------------------------------------------
# -----------------------------------------------------CALLBACKS-------------------------------------------------------


@app.callback(
    Output("line_d", "figure"),
    Input("driver_drop", "value"))
def update_line_chart_d(drivers):
    df = px.data.gapminder()  # replace with your own data source
    mask = total_points.Driver.isin(drivers)
    fig = px.line(total_points[mask],
                  x="Year", y="Points", color='Driver')
    return fig











