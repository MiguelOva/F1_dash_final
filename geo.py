# --------------------------------------------------  PACKAGES
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app

# -------------------------------------------------- LOADING DATAFRAMES
from data import df_races
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


# --------------------------------------------------  GEO LAYOUT
geo_layout = html.Div(children=[
    html.H1('Races Location 1950 to 2021',
            style={'textAlign': 'left', 'color': '#503D36', 'margin-top': '15px', 'font-size': 28}),

    html.Div([
        html.Div([
            dcc.Dropdown(id='input-year',
                         options=[{'label': i, 'value': i} for i in years],
                         placeholder="Select the year",
                         value=2021,
                         style={'width': '50%', 'height': '5%',
                                'font-size': '15px', 'margin-top': '15px', 'text-align-last': 'center'}),
        ])
    ]),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='map', figure={})
])


# ------------------------------------------------------CALLBACKS-------------------------------------------------------
@app.callback(Output(component_id='output_container', component_property='children'),
              Output(component_id='map', component_property='figure'),
              [Input(component_id='input-year', component_property='value')])

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    container = "The default year presented: {}".format(option_slctd)

    fig = px.scatter_mapbox(
        df_races[df_races["year"] == option_slctd],
        hover_name="name_t",
        hover_data=["year", "round", "location_t"],
        color="country",
        zoom=3,
        height=600,
        lat="lat", lon="lng", )
    fig.update_layout(mapbox_style="dark")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return container, fig


