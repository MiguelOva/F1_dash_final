# --------------------------------------------------  PACKAGES
from main import app
import pandas as pd
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dash_table as dt

# -------------------------------------------------- LOADING DATAFRAMES
from data import dfr_new
from data import df_results_t
from data import total_points
from data import total_points_team
from data import hall_of_fame


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

# Select Desired Number
number = [i for i in range(1, 50, 1)]

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
                          multi=True
                          )

drop_num = dcc.Dropdown(id='dropdown_number',
                        placeholder="Select the desired value",
                        options=number,
                        value=10,
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

hall_of_fame_layout = html.Div([
    html.H4('HALL OF FAME 1950-2021',
            style={'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dcc.Tabs(id="hof_tables", value='hof_tables', children=[

        dcc.Tab(label='Constructors Hall of Fame', value='cons_hof', style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(label='Drivers Hall of Fame', value='drivers_hof', style=tab_style, selected_style=tab_selected_style)

    ], style=tabs_styles),
    html.Br(),
    html.Div(id='tables_hof')
])


# -------------------------------------------------- SUB TABS CALLBACK
# -------------------------------------------------- SUB TABS CALLBACK

@app.callback(
    Output("tables_hof", "children"),
    [Input("hof_tables", "value")]
)
def seperator_switch(tab):
    if tab == "cons_hof":
        return cons_hof_layout
    elif tab == "drivers_hof":
        return drivers_hof_layout


# ------------------------------------------------------LAYOUT------------------------------------------------------
# ------------------------------------------------CONS HALL OF FAME--------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------

cons_hof_layout = html.Div([
    html.H1('Hall of Fame - Cosntructors',
            style={'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),

    html.Div([
        html.Div([
            drop_num,
                ]),
            html.Br(),
            ]),

    dbc.Row(children=[
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Constructors Per Total Points"),
                dbc.CardBody(id='cons_hof_p', children=[
                    dt.DataTable(
                        columns=[{"name": i, "id": i} for i in hall_of_fame.columns],
                        data=hall_of_fame.to_dict("records"),
                        page_current=0,
                        style_header={"backgroundColor": "white", "fontWeight": "bold", },
                        style_cell={"textAlign": "center", "font-size": "12px", },
                        style_cell_conditional=[{"if": {"column_id": "Finished"}, "textAlign": "center", }],
                            ),
                            ]),
                    ]),
                    ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Constructors Per Total Wins"),
                dbc.CardBody(id='cons_hof_w', children=[
                    dt.DataTable(
                        columns=[{"name": i, "id": i} for i in hall_of_fame.columns],
                        data=hall_of_fame.to_dict("records"),
                        page_current=0,
                        style_header={"backgroundColor": "white", "fontWeight": "bold", },
                        style_cell={"textAlign": "center", "font-size": "12px", },
                        style_cell_conditional=[{"if": {"column_id": "Finished"}, "textAlign": "center", }],
                                ),
                            ]),
                    ]),
                    ),
                ]),
html.Br(),
html.Br(),
            ])


# -----------------------------------------------------CALLBACKS-------------------------------------------------------
# ----------------------------------------------------CONSTRUCTORS------------------------------------------------------
# -----------------------------------------------------CALLBACKS-------------------------------------------------------

@app.callback(
    Output(component_id="cons_hof_p", component_property="children"),
    Output(component_id="cons_hof_w", component_property="children"),
    Input(component_id="dropdown_number", component_property="value")
)
def constructor_hall_of_fame(number):
    fame_points = hall_of_fame.groupby(['name_c'])['points'].sum().reset_index().sort_values(by='points',
                                                                                             ascending=False)
    top_c = fame_points.head(number)
    top_c = dt.DataTable(top_c.to_dict('records'), [{"name": i, "id": i} for i in top_c.columns])

    st_position_c = hall_of_fame[hall_of_fame['position'] == '1']
    st_position_c = st_position_c['name_c'].value_counts()
    list3 = list(st_position_c.index)
    list4 = list(st_position_c.values)
    df_st_position_c = pd.DataFrame(list(zip(list3, list4)), columns=['Constructor', 'Nr of 1st places'])
    top_c_wins = df_st_position_c.head(number)
    top_c_wins = dt.DataTable(top_c_wins.to_dict('records'), [{"name": i, "id": i} for i in top_c_wins.columns])

    return top_c, top_c_wins


# ------------------------------------------------------LAYOUT------------------------------------------------------
# ------------------------------------------------DRIVERS HALL OF FAME--------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------
drivers_hof_layout = html.Div([
    html.H1('Hall of Fame - Drivers',
            style={'color': '#503D36', 'margin-top': '15px', 'font-size': 15}),

    html.Div([
        html.Div([
            drop_num,
                ]),
            html.Br(),
            ]),

    dbc.Row(children=[
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Drivers Per Total Points"),
                dbc.CardBody(id='drivers_hof_p', children=[
                    dt.DataTable(
                        columns=[{"name": i, "id": i} for i in hall_of_fame.columns],
                        data=hall_of_fame.to_dict("records"),
                        page_current=0,
                        style_header={"backgroundColor": "white", "fontWeight": "bold", },
                        style_cell={"textAlign": "center", "font-size": "12px", },
                        style_cell_conditional=[{"if": {"column_id": "Finished"}, "textAlign": "center", }],
                            ),
                            ]),
                    ]),
                    ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Drivers Per Total Wins"),
                dbc.CardBody(id='drivers_hof_w', children=[
                    dt.DataTable(
                        columns=[{"name": i, "id": i} for i in hall_of_fame.columns],
                        data=hall_of_fame.to_dict("records"),
                        page_current=0,
                        style_header={"backgroundColor": "white", "fontWeight": "bold", },
                        style_cell={"textAlign": "center", "font-size": "12px", },
                        style_cell_conditional=[{"if": {"column_id": "Finished"}, "textAlign": "center", }],
                                ),
                            ]),
                    ]),
                    ),
                ]),
html.Br(),
html.Br(),
            ])


# -----------------------------------------------------CALLBACKS-------------------------------------------------------
# ----------------------------------------------------CONSTRUCTORS------------------------------------------------------
# -----------------------------------------------------CALLBACKS-------------------------------------------------------

@app.callback(
    Output(component_id="drivers_hof_p", component_property="children"),
    Output(component_id="drivers_hof_w", component_property="children"),
    Input(component_id="dropdown_number", component_property="value")
)
def drivers_hall_of_fame(number):
    fame_points = hall_of_fame.groupby(['name_d'])['points'].sum().reset_index().sort_values(by='points',
                                                                                             ascending=False)
    top_d = fame_points.head(number)
    top_d = dt.DataTable(top_d.to_dict('records'), [{"name": i, "id": i} for i in top_d.columns])

    st_position = hall_of_fame[hall_of_fame['position'] == '1']
    st_position1 = st_position['name_d'].value_counts()
    list1 = list(st_position1.index)
    list2 = list(st_position1.values)
    df_st_position = pd.DataFrame(list(zip(list1, list2)), columns=['Driver', 'Nr of 1st places'])
    top_d_wins = df_st_position.head(number)

    top_d_wins = dt.DataTable(top_d_wins.to_dict('records'), [{"name": i, "id": i} for i in top_d_wins.columns])

    return top_d, top_d_wins
