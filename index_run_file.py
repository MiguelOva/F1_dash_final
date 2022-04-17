# --------------------------------------------------  PACKAGES
from dash import html
from dash.dependencies import Input, Output, State
from main import app
import dash_bootstrap_components as dbc

# --------------------------------------------------  Connect to separators
from current import hall_of_fame_layout
from champ import champ_layout
from geo import geo_layout
from socials import social_layout
from tables import tables_layout
from sunburst import sun_layout
from dnf import dnf_layout
from speed import line_layout
from info import info_layout

# -------------------------------------------------- CREATING DIFFERENT SEPARATORS
app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Hall Of Fame", tab_id="current_sep", labelClassName="text-success font-weight-bold", activeLabelClassName ="text-danger"),
                dbc.Tab(label="Championship", tab_id="champ_sep", labelClassName="text-success font-weight-bold",activeLabelClassName="text-danger"),
                dbc.Tab(label="Tables Comparison", tab_id="tables_sep", labelClassName="text-success font-weight-bold", activeLabelClassName ="text-danger"),
                dbc.Tab(label="Line Comparison", tab_id="line_sep", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Sunburst", tab_id="sun_sep", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="DNF", tab_id="dnf_sep", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Track & Champs - Info", tab_id="info_sep", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Geolocation", tab_id="geo_sep", labelClassName="text-success font-weight-bold",activeLabelClassName ="text-danger"),
                dbc.Tab(label="Socials", tab_id="social_sep", labelClassName="text-success font-weight-bold",activeLabelClassName ="text-danger"),

                dbc.Row(dbc.Col(width=12)),

            ],
            id="seps",
            active_tab="current_sep",
        ),
    ], className="mt-3"
)


# -------------------------------------------------- APP LAYOUT
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("Formula 1 - Statistical Data Analysis",
                            style={"textAlign": "left", "margin-top": '20px'}), width=12)),
    html.Hr(),
    dbc.Row(
        dbc.Col(
            app_tabs, width=12), className="fr-1"),
    html.Div(id='data_1', children=[])

])

# -------------------------------------------------- CALLBACK FOR SEPARATORS
@app.callback(
    Output("data_1", "children"),
    [Input("seps", "active_tab")]
)

def seperator_switch(choice):
    if choice == "current_sep":
        return hall_of_fame_layout
    elif choice == "champ_sep":
        return champ_layout
    elif choice == "tables_sep":
        return tables_layout
    elif choice == "sun_sep":
        return sun_layout
    elif choice == "line_sep":
        return line_layout
    elif choice == "dnf_sep":
        return dnf_layout
    elif choice == "info_sep":
        return info_layout
    elif choice == "geo_sep":
        return geo_layout
    elif choice == "social_sep":
        return social_layout
    else:
        html.P("I hate my Life")

if __name__ == '__main__':
    app.run_server(debug=True)
