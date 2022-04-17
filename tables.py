# --------------------------------------------------  PACKAGES
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
from app import app
from dash import dash_table as dt

# -------------------------------------------------- LOADING DATAFRAMES
from data import df_results_t
from data import dfr_new
from data import df_cc
from data import df_dc

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

# --------------------------------------------------  DROPDOWNS
drop_const = dcc.Dropdown(id='dropdown_constructors',
                          placeholder="Select the Constructor",
                          options=constructors_options,
                          value='Mercedes',
                          multi=True,
                          )

drop_drivers = dcc.Dropdown(id='dropdown_drivers',
                            placeholder="Select the Driver",
                            options=driver_options,
                            value='Lewis Hamilton',
                            multi=True,
                            )

drop_years = dcc.Dropdown(id='dropdown_years',
                          placeholder="Select the Championship Year",
                          options=years,
                          value=2021)

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

tables_layout = html.Div([
    html.H4('Championship Standings Comparison: 1950 - 2021',
            style={'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dcc.Tabs(id="champ_tables", value='champ_tables', children=[

        dcc.Tab(label='Constructors Standings', value='cons_tables', style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(label='Drivers Standings', value='drivers_tables', style=tab_style, selected_style=tab_selected_style)

    ], style=tabs_styles),
    html.Br(),
    html.Div(id='tables_content')
])


# -------------------------------------------------- SUB TABS CALLBACK
# -------------------------------------------------- SUB TABS CALLBACK

@app.callback(
    Output("tables_content", "children"),
    [Input("champ_tables", "value")]
)
def seperator_switch(tab):
    if tab == "cons_tables":
        return cons_layout
    elif tab == "drivers_tables":
        return drivers_layout
    else:
        print("I hate my life")


# ------------------------------------------------------LAYOUT------------------------------------------------------
# ----------------------------------------------------CONSTRUCTORS------------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------

cons_layout = html.Div([

    html.Div([
        html.H1('Constructors Standings Comparison:',
                style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),
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
                            html.P(id="const_table",
                                   style={"margin": "5 10px", 'margin-top': '15px'}),
                            html.Br()]),
                    ]),
                ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Constructor Table Standings"),
                dbc.CardBody(id='const_table', children=[
                    dt.DataTable(
                        columns=[{"name": i, "id": i} for i in df_cc.columns],
                        data=df_cc.to_dict("records"),
                        page_current=0,
                        style_header={"backgroundColor": "white", "fontWeight": "bold", },
                        style_cell={"textAlign": "center", "font-size": "12px", },
                        style_cell_conditional=[{"if": {"column_id": "Finished"}, "textAlign": "center", }]
                    ),
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
    Output(component_id="const_table", component_property="children"),
    Input(component_id="dropdown_constructors", component_property="value"),
    Input(component_id="dropdown_years", component_property="value")
)
def constructor_comparison(teams, year):
    standings_t = df_cc.loc[[x in teams for x in df_cc['name_c'].tolist()] & (df_cc['year'] == year)]
    standings_t = standings_t.groupby(['name_c', 'year', 'round', 'name_t', 'wins'])['champ_pts'].max(
    ).sort_values(ascending=False).reset_index()
    standings_t = standings_t.sort_values(by='round')
    standings_t = dt.DataTable(standings_t.to_dict('records'), [{"name": i, "id": i} for i in standings_t.columns])

    return standings_t


# ------------------------------------------------------LAYOUT------------------------------------------------------
# ------------------------------------------------------DRIVERS------------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------
drivers_layout = html.Div([

    html.Div([
        html.H1('Drivers Standings Comparison:',
                style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),
    ], id='1st row', className='pretty_box'),

    html.Div([
        dbc.Row(children=[
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Optional Filters"),
                    dbc.CardBody(children=[
                        html.Label('Please select Drivers'),
                        drop_drivers,
                        html.Br(),
                        html.Label('Please select Year'),
                        drop_years,
                        html.Br(),
                        dcc.Loading(children=[
                            html.P(id="drivers_table",
                                   style={"margin": "5 10px", 'margin-top': '15px'}),
                            html.Br()]),
                    ]),
                ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Drivers Table Standings"),
                dbc.CardBody(id='drivers_table', children=[
                    dt.DataTable(
                        columns=[{"name": i, "id": i} for i in df_cc.columns],
                        data=df_cc.to_dict("records"),
                        page_current=0,
                        style_header={"backgroundColor": "white", "fontWeight": "bold", },
                        style_cell={"textAlign": "center", "font-size": "12px", },
                        style_cell_conditional=[{"if": {"column_id": "Finished"}, "textAlign": "center", }]
                    ),
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
    Output(component_id="drivers_table", component_property="children"),
    Input(component_id="dropdown_drivers", component_property="value"),
    Input(component_id="dropdown_years", component_property="value")
)
def drivers_comparison(drivers, year):
    standings_t = df_dc.loc[[x in drivers for x in df_dc['name_d'].tolist()] & (df_dc['year'] == year)]
    standings_t = standings_t.groupby(['name_d', 'year', 'round', 'name_t', 'wins'])['champ_pts'].max(
    ).sort_values(ascending=False).reset_index()
    standings_t = standings_t.sort_values(by='round')
    standings_t = dt.DataTable(standings_t.to_dict('records'), [{"name": i, "id": i} for i in standings_t.columns])

    return standings_t
