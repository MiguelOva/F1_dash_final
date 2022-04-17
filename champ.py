# --------------------------------------------------  PACKAGES
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from main import app

# -------------------------------------------------- LOADING DATAFRAMES
from data import df_results_t
from data import dfr_new
from data import df_cc
from data import df_dc
from data import df_drivers
from data import df_constructors

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


# --------------------------------------------------  REQUIRED DF Champ
# Filter standings by only LAST ROUND OF EACH YEAR
a = (df_cc.sort_values(['year', 'round'], ascending=[True, False]).drop_duplicates(['year']).reset_index(drop=True))
a = a[['raceId', 'year', 'round']]
b = pd.merge(a, df_cc, how='inner', on=['raceId'])
b = pd.merge(b, df_constructors, how='inner', on=['name_c'])
b = b[['raceId', 'name_t', 'year_y', 'round_y', 'name_c','nationality_c','champ_pts', 'champ_pos', 'wins']]

df_champ = b
df_champ = df_champ[df_champ['year_y'] >= 2000]
df_champ = df_champ[df_champ['year_y'] != 2022]

# --------------------------------------------------  REQUIRED DF Drivers
# Filter standings by only LAST ROUND OF EACH YEAR
c = (df_dc.sort_values(['year', 'round'], ascending=[True, False]).drop_duplicates(['year']).reset_index(drop=True))
c = c[['raceId', 'year', 'round']]
d = pd.merge(c, df_dc, how='inner', on=['raceId'])
d = pd.merge(d, df_drivers, how='inner', on=['name_d'])
d = d[['raceId', 'name_t', 'year_y', 'round_y', 'name_d','nationality_d', 'champ_pts', 'champ_pos', 'wins']]

df_champ_d = d
df_champ_d = df_champ_d[df_champ_d['year_y'] >= 2000]
df_champ_d = df_champ_d[df_champ_d['year_y'] != 2022]

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


# -------------------------------------------------- SUB TABS CALLBACK
champ_layout = html.Div([
    html.H4('Interactive Championship Tables: 2000 - 2021', style={'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dcc.Tabs(id="int_bars", value='int_bars', children=[

        dcc.Tab(label='Constructors Int Table', value='cons_tab', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Drivers Int Table', value='drivers_tab', style=tab_style, selected_style=tab_selected_style)

    ], style=tabs_styles),
    html.Br(),
    html.Div(id='int_content')
])
# -------------------------------------------------- SUB TABS CALLBACK

@app.callback(
    Output("int_content", "children"),
    [Input("int_bars", "value")]
)
def seperator_switch(tab):
    if tab == "cons_tab":
        return cons_tab_layout
    elif tab == "drivers_tab":
        return drivers_tab_layout
    else:
        print("I hate my life")

# ------------------------------------------------------LAYOUT------------------------------------------------------
# -----------------------------------------------------DNF CONST------------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------

cons_tab_layout = html.Div([
                    html.H1('Interactive Constructors Table: 2000 - 2021',
                    style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dash_table.DataTable(
        id='datatable-interactivity-champ',
        columns=[
            {"name": i, "id": i, "hideable": True, "selectable": True} for i in df_champ.columns
        ],
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        data=df_champ.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-interactivity-champ-container')
])

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(
    Output('datatable-interactivity-champ', 'style_data_conditional'),
    Input('datatable-interactivity-champ', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(
    Output('datatable-interactivity-champ-container', "children"),
    Input('datatable-interactivity-champ', "derived_virtual_data"),
    Input('datatable-interactivity-champ', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df_champ if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["name_c"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 350,
                    "margin": {"t": 25, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["champ_pts", "wins"] if column in dff
    ]


# ------------------------------------------------------LAYOUT------------------------------------------------------
# -----------------------------------------------------DNF CONST------------------------------------------------------
# ------------------------------------------------------LAYOUT------------------------------------------------------

drivers_tab_layout = html.Div([
                    html.H1('Interactive Drivers Table: 2000 - 2021',
                    style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dash_table.DataTable(
        id='datatable-interactivity-driver',
        columns=[
            {"name": i, "id": i, "hideable": True, "selectable": True} for i in df_champ_d.columns
        ],
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        data=df_champ_d.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-interactivity-driver-container')
])

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(
    Output('datatable-interactivity-driver', 'style_data_conditional'),
    Input('datatable-interactivity-driver', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(
    Output('datatable-interactivity-driver-container', "children"),
    Input('datatable-interactivity-driver', "derived_virtual_data"),
    Input('datatable-interactivity-driver', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):


    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df_champ_d if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["name_d"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 350,
                    "margin": {"t": 25, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["champ_pts", "wins"] if column in dff
    ]





















