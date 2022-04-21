# --------------------------------------------------  PACKAGES
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
from main import app
from dash.dependencies import Input, Output

# -------------------------------------------------- LOADING DATAFRAMES
from data import df_results_t
from data import dfr_new

# --------------------------------------------------  PLOTLY MAPBOX ACCESS TOKEN
px.set_mapbox_access_token(
    "pk.eyJ1IjoibWlndWVsLW92YSIsImEiOiJjbDFmNGlqZ2wwMWNyM2VtamFmcnMxY2twIn0.hSSsFzP_FRfrILsBmgc1gQ"
)

# --------------------------------------------------  COMPONENTS RANGE
# list of Years
years = [dict(label=year, value=year) for year in df_results_t['year'].unique()]
years

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



df_dnf_c = df_results_t[df_results_t['position'] == 'DNF']
df_dnf_c = df_dnf_c.groupby(['name_c', 'year','status']).status.agg(['count']).reset_index()

df_dnf_d = df_results_t[df_results_t['position'] == 'DNF']
df_dnf_d = df_dnf_d.groupby(['name_d', 'year','status']).status.agg(['count']).reset_index()

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
                           value=['Lewis Hamilton', 'Max Verstappen'],
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

dnf_layout = html.Div([
    html.H4('DNF Status per Driver & Constructor  1950 - 2021', style={'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dcc.Tabs(id="dnf_bars", value='dnf_bars', children=[

        dcc.Tab(label='Constructors DNF', value='cons_bar', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Drivers DNF', value='drivers_bar', style=tab_style, selected_style=tab_selected_style)

    ], style=tabs_styles),
    html.Br(),
    html.Div(id='dnf_content')
])

# -------------------------------------------------- SUB TABS CALLBACK
# -------------------------------------------------- SUB TABS CALLBACK

@app.callback(
    Output("dnf_content", "children"),
    [Input("dnf_bars", "value")]
)
def seperator_switch(tab):
    if tab == "cons_bar":
        return cons_layout
    elif tab == "drivers_bar":
        return drivers_layout
    else:
        print("I hate my life")


# ------------------------------------------------------LAYOUT------------------------------------------------------
# -----------------------------------------------------DNF CONST------------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------
cons_layout = html.Div([

html.Div([
    html.H1('Constructors DNF Status:',
            style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),
], id='1st row', className='pretty_box'),

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
                    html.P(id="const_dnf",
                           style={"margin": "5 10px", 'margin-top': '15px'}),
                    html.Br()]),
                        ]),
                ]), width=3),
    dbc.Col(dbc.Card([
        dbc.CardHeader("Constructor DNF status & count"),
        dbc.CardBody(children=[
            dcc.Graph(id="bar_plot_c")
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
    Output(component_id="bar_plot_c", component_property="figure"),
    Input(component_id="dropdown_constructors", component_property="value"),
    Input(component_id="dropdown_years", component_property="value")
)

def update_bar_chart(constructors, year):

    data_c = df_dnf_c.loc[[x in constructors for x in df_dnf_c['name_c'].tolist()] & (df_dnf_c['year'] == year)]
    # df = px.total_dnf.Constructor() # replace with your own data source
    fig = px.bar(data_c, x="status", y="count", color="name_c", title="Drivers DNF count", text_auto=True, height=650)
    # color="smoker", barmode="group"))
    return fig

# ------------------------------------------------------LAYOUT------------------------------------------------------
# -----------------------------------------------------DNF DRIVER------------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------

drivers_layout = html.Div([

html.Div([
    html.H1('Drivers DNF Status:',
            style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),
], id='1st row', className='pretty_box'),

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
                        html.P(id="driver_dnf",
                               style={"margin": "5 10px", 'margin-top': '15px'}),
                        html.Br()]),
                            ]),
                    ]), width=3),
    dbc.Col(dbc.Card([
        dbc.CardHeader("Drivers DNF status & count"),
        dbc.CardBody(children=[
            dcc.Graph(id="bar_plot_d")
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
    Output(component_id="bar_plot_d", component_property="figure"),
    Input(component_id="driver_drop", component_property="value"),
    Input(component_id="dropdown_years", component_property="value")
)

def update_bar_chart(drivers, year):

    data_d = df_dnf_d.loc[[x in drivers for x in df_dnf_d['name_d'].tolist()] & (df_dnf_d['year'] == year)]
    # df = px.total_dnf.Constructor() # replace with your own data source
    fig = px.bar(data_d, x="status", y="count", color="name_d", title="Drivers DNF count", text_auto=True, height=650)
    # color="smoker", barmode="group"))
    return fig

