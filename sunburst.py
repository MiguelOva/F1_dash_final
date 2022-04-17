# --------------------------------------------------  PACKAGES
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app

# -------------------------------------------------- LOADING DATAFRAMES
from data import df_results_t
from data import dfr_new

# -------------------------------------------------- CREATING DATAFRAMES
sunburst_df = df_results_t.loc[df_results_t['position'] == '1']


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
                          value=['Mercedes'],
                          multi=True,
                          )

drop_driver = dcc.Dropdown(id='driver_drop',
                           options=driver_options,
                           placeholder="Select the Driver",
                           value=['Lewis Hamilton'],
                           multi=True,
                           )

drop_tracks = dcc.Dropdown(id='track_drop',
                           options=tracks_options,
                           placeholder="Select the Track",
                           value=['Australian Grand Prix']
                           )

drop_years = dcc.Dropdown(id='dropdown_years',
                          placeholder="Select the Championship Year",
                          options=years,
                          value=2021,
                          )



# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
# ------------------------------------------------------DROPDOWNS-------------------------------------------------------
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

# -------------------------------------------------- APP LAYOUT
sun_layout = html.Div([
    html.H4('Sunburst Graphical Analysis', style={'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dcc.Tabs(id="sun-graph", value='sun_graphs', children=[

        dcc.Tab(label='Sunburst Wins', value='sun_wins', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Sunburst Points', value='sun_points', style=tab_style, selected_style=tab_selected_style)

    ], style=tabs_styles),
    html.Br(),
    html.Div(id='sun_content')
])


# -------------------------------------------------- APP LAYOUT

@app.callback(
    Output("sun_content", "children"),
    [Input("sun-graph", "value")]
)
def seperator_switch(tab):
    if tab == "sun_wins":
        return sun_layout_wins
    elif tab == "sun_points":
        return sun_layout_points
    else:
        print("I hate my life")

# --------------------------------------------------  SUN LAYOUT WINS
# --------------------------------------------------  SUN LAYOUT WINS
# --------------------------------------------------  SUN LAYOUT WINS
# --------------------------------------------------  SUN LAYOUT WINS
# --------------------------------------------------  SUN LAYOUT WINS
# --------------------------------------------------  SUN LAYOUT WINS

sun_layout_wins = html.Div([
    html.H1('Sunburst per Wins',
            style={'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),

    html.Div([
        html.Div([
            drop_years,
        ]),
        html.Br(),
    ]),

    dbc.Row(children=[
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Per Driver"),
                dbc.CardBody(children=[
                    dcc.Loading(children=[
                        dcc.Graph(id="sun_dri", style={"height": "550px", "width": "500px"}),
                        html.Br(),
                    ],
                        type="circle",
                    ),
                ]),
            ]), width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Per Constructor"),
                dbc.CardBody(children=[
                    dcc.Loading(children=[
                        dcc.Graph(id="sun_cons", style={"height": "550px", "width": "500px"}),
                        html.Br(),
                    ],
                        type="circle",
                    ),
                ]),
            ]), width=6,
        ),
    ]),
html.Br(),
html.Br(),
    dbc.Row(children=[
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Complete -- Per Driver & Per Constructor"),
                dbc.CardBody(children=[
                    dcc.Loading(children=[
                        dcc.Graph(id="sun_complete", style={"height": "621px", "width": "1068px"}),
                        html.Br(),
                    ]),
                    ]),
                ]),
        ),
    ]),
html.Br(),
html.Br(),
])

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
# ------------------------------------------------------- WINS -------------------------------------------------------
# ------------------------------------------------------CALLBACKS-------------------------------------------------------


@app.callback(
    Output("sun_dri", "figure"),
    Input("dropdown_years", "value"))
def update_sun_w(option_slctd):
    fig1 = px.sunburst(sunburst_df.loc[sunburst_df['year'] == option_slctd], path=['name_d', 'name_t'], values='position')

    return fig1


@app.callback(
    Output("sun_cons", "figure"),
    Input("dropdown_years", "value"))
def update_sun_w2(option_slctd):
    fig2 = px.sunburst(sunburst_df.loc[sunburst_df['year'] == option_slctd], path=['name_c', 'name_t'], values='position')

    return fig2

@app.callback(
    Output("sun_complete", "figure"),
    Input("dropdown_years", "value"))
def update_sun_w3(option_slctd):
    fig3 = px.sunburst(sunburst_df.loc[sunburst_df['year'] == option_slctd], path=['name_c', 'name_d', 'name_t'], values='position')

    return fig3


# --------------------------------------------------  SUN LAYOUT POINTS
# --------------------------------------------------  SUN LAYOUT POINTS
# --------------------------------------------------  SUN LAYOUT POINTS
# --------------------------------------------------  SUN LAYOUT POINTS
# --------------------------------------------------  SUN LAYOUT POINTS
# --------------------------------------------------  SUN LAYOUT POINTS
sunburst_df_p = df_results_t.copy()


sun_layout_points = html.Div([
    html.H1('Sunburst per Points',
            style={'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),

    html.Div([
        html.Div([
            drop_years,
        ]),
        html.Br(),
    ]),

    dbc.Row(children=[
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Per Driver"),
                dbc.CardBody(children=[
                    dcc.Loading(children=[
                        dcc.Graph(id="sun_dri_p", style={"height": "550px", "width": "500px"}),
                        html.Br(),
                    ],
                        type="circle",
                    ),
                ]),
            ]), width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Per Constructor"),
                dbc.CardBody(children=[
                    dcc.Loading(children=[
                        dcc.Graph(id="sun_cons_p", style={"height": "550px", "width": "500px"}),
                        html.Br(),
                    ],
                        type="circle",
                    ),
                ]),
            ]), width=6,
        ),
    ]),
html.Br(),
html.Br(),
    dbc.Row(children=[
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Complete -- Per Driver & Per Constructor"),
                dbc.CardBody(children=[
                    dcc.Loading(children=[
                        dcc.Graph(id="sun_complete_p", style={"height": "621px", "width": "1068px"}),
                        html.Br(),
                    ]),
                    ]),
                ]),
        ),
    ]),
html.Br(),
html.Br(),
])

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
# ------------------------------------------------------ POINTS -------------------------------------------------------
# ------------------------------------------------------CALLBACKS-------------------------------------------------------


@app.callback(
    Output("sun_dri_p", "figure"),
    Input("dropdown_years", "value"))
def update_sun_p(option_slctd):
    fig4 = px.sunburst(sunburst_df_p.loc[sunburst_df_p['year'] == option_slctd], path=['name_d', 'name_t'], values='points')

    return fig4


@app.callback(
    Output("sun_cons_p", "figure"),
    Input("dropdown_years", "value"))
def update_sun_p1(option_slctd):
    fig5 = px.sunburst(sunburst_df_p.loc[sunburst_df_p['year'] == option_slctd], path=['name_c', 'name_t'], values='points')

    return fig5

@app.callback(
    Output("sun_complete_p", "figure"),
    Input("dropdown_years", "value"))
def update_sun_p3(option_slctd):
    fig6 = px.sunburst(sunburst_df_p.loc[sunburst_df_p['year'] == option_slctd], path=['name_c', 'name_d', 'name_t'], values='points')

    return fig6







