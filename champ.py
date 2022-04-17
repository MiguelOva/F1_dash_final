# --------------------------------------------------  PACKAGES
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from app import app

# -------------------------------------------------- LOADING DATAFRAMES
from data import df_results_t
from data import dfr_new
from data import df_cc

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


# --------------------------------------------------  REQUIRED DF
# Filter standings by only LAST ROUND OF EACH YEAR
a = (df_cc.sort_values(['year', 'round'], ascending=[True, False]).drop_duplicates(['year']).reset_index(drop=True))
a = a[['raceId', 'year', 'round']]
b = pd.merge(a, df_cc, how='inner', on=['raceId'])
b = b[['raceId', 'name_t', 'year_y', 'round_y', 'name_c', 'champ_pts', 'champ_pos', 'wins']]

df_champ = b
df_champ = df_champ[df_champ['year_y'] >= 2000]
df_champ = df_champ[df_champ['year_y'] != 2022]


# --------------------------------------------------  CHAMP LAYOUT
# Sorting operators (https://dash.plotly.com/datatable/filtering)
champ_layout = html.Div([
                    html.H1('Interactive Championship Table: 2004 - 2021',
                    style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 20}),

    dash_table.DataTable(
        id='datatable-interactivity',
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
    html.Div(id='datatable-interactivity-container')
])

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# ------------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):

    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.

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
        for column in ["champ_pts", "wins", 'champ_pos'] if column in dff
    ]



















