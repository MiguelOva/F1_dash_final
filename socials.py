# --------------------------------------------------  PACKAGES
from dash import html
import plotly.express as px

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


# --------------------------------------------------  SOCIAL LAYOUT
# --------------------------------------------------  SOCIAL LAYOUT

social_layout = html.Div(children=[
    html.H1('F1 Social Networks',
            style={'textAlign': 'left', 'color': '#503D36', 'font-size': 28, 'margin-top': '15px'}),

    html.Div([
        html.Div([
            html.Iframe(
                srcDoc='''
                        <a class="twitter-timeline" data-theme="light" href="https://twitter.com/F1?s=20&t=Fc_K8_Xj2oFx58ihSXA9rQ">
                            Tweets by F1 Official Account
                        </a> 
                        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        ''',
                height=800,
                width=400
            )
        ]),
        html.Div([
            html.Iframe(
                srcDoc='''
                       <iframe 
                        src="https://widget.taggbox.com/91613" style="width:685px;height:1770px;overflow: auto; border:none">
                        </iframe>
                        ''',
                height=800,
                width=717
            )
        ])
    ], style={'display': 'flex'})
])
