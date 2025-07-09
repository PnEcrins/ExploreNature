from typing import List
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign


import plotly.express as px

import pandas as pd

from layouts import card

from queries import (
    get_total_obs,
    get_new_species,
    get_new_species_commune,
    get_all_data_geo,
    get_species_in_event,
    get_group2_inpn,
    get_ordres,
    get_familles,
    get_observers,
    get_communal_limit,
)
from utils import format_columns, pointToLayer
from config import *


# TODO : nombre d'espèce total observé
# répartition par groupe des espèces
# rajouter l'ordre et la classe sur les tableaux ?


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# observations
observation_geom = get_all_data_geo()
limit_commune = get_communal_limit()


######################
##### GLOBAL vars ####
######################

# Species in event
g_species_in_event = get_species_in_event()
species_in_event_df = pd.DataFrame.from_dict(g_species_in_event)
species_event_chart = px.pie(
    species_in_event_df,
    names="group2_inpn",
    hole=0.3,
)
species_event_chart.update_traces(textinfo="value")

# new species in town

g_new_species_commune = get_new_species_commune()
new_species_commune_df = pd.DataFrame.from_dict(g_new_species_commune)

new_species_commune_chart = px.pie(
    pd.DataFrame.from_dict(g_new_species_commune),
    names="group2_inpn",
    hole=0.3,
)

# new species in structure

g_new_species = get_new_species()
new_species_df = pd.DataFrame.from_dict(g_new_species)

new_species_chart = px.pie(
    new_species_df,
    names="group2_inpn",
    title="Nouvelle espèces",
    hole=0.3,
)

# observer in dataset
observers = get_observers()


app.layout = dbc.Container(
    [
        html.H1(children=EVENT_TITLE, style={"textAlign": "center"}),
        html.Div(
            [
                dcc.Dropdown(
                    get_group2_inpn(),
                    id="group2-dropdown",
                    clearable=True,
                    placeholder="Filtrer par groupe INPN",
                    className="mb-3",
                ),
                dcc.Dropdown(
                    get_ordres(),
                    id="ordre-dropdown",
                    clearable=True,
                    placeholder="Filtrer par ordre",
                    className="mb-3",
                ),
                dcc.Dropdown(
                    get_familles(),
                    id="famille-dropdown",
                    clearable=True,
                    placeholder="Filtrer par famille",
                ),
            ],
            className="mb-3",
        ),
        # CARD
        html.Div(
            className="d-flex justify-content-center mb-5",
            children=[
                card("Nombre de données", "", id="nb_data"),
                card("Nombre d'espèces", "", id="nb_species"),
                card(
                    "Nouvelles espèces pour la commune",
                    "",
                    id="nb_new_species_commune",
                ),
                card(
                    "Nouvelles espèces pour le Parc",
                    "",
                    id="nb_new_species_pne",
                ),
            ],
        ),
        # SPECIES IN EVENT
        html.Div(
            children=[
                html.H2(children="Taxons observés pendant l'évenement"),
                html.Div(id="my-output"),
                html.Div(
            className="d-flex justify-content-center",
                    children=[
                        html.Div(
                            dash_table.DataTable(
                                data=[],
                                columns=format_columns(g_species_in_event),
                                page_size=15,
                                sort_action="native",
                                id="datable_species",
                                markdown_options={"html": True},
                                style_cell={"textAlign": "left"},
                            ),
                        ),
                    ],
                ),
                html.Div(
                    className="d-flex justify-content-center",
                    children=[
                        html.Div(
                            dcc.Graph(
                                figure=species_event_chart,
                                style={"width": "70vh", "height": "50vh"},
                            ),
                        ),
                    ],
                ),
            ]
        ),
        # NOUVELLE ESPECE COMMUNE
        html.H2(children="Nouveaux taxons sur la commune"),
        html.Div(
            className="d-flex justify-content-center",
            children=[
                html.Div(
                    dash_table.DataTable(
                        data=[],
                        columns=format_columns(g_new_species_commune),
                        page_size=15,
                        sort_action="native",
                        id="datable_new_species_commune",
                        markdown_options={"html": True},
                        style_cell={"textAlign": "left"},
                    ),
                ),
            ],
        ),
        html.Div(
            className="d-flex justify-content-center",
            children=[
                html.Div(
                    dcc.Graph(
                        figure=new_species_commune_chart,
                        style={"width": "70vh", "height": "50vh"},
                    ),
                ),
            ],
        ),
        # NOUVELLE ESPECE Parc
        html.H2(children="Nouveaux taxons pour le Parc"),
        html.Div(
            className="d-flex justify-content-center",
            children=[
                html.Div(
                    dash_table.DataTable(
                        data=[],
                        columns=format_columns(g_new_species),
                        page_size=15,
                        sort_action="native",
                        id="new_species_in_structure",
                        markdown_options={"html": True},
                        style_cell={"textAlign": "left"},
                    ),
                ),
            ],
        ),
        html.Div(
            className="d-flex justify-content-center",
            children=[
                html.Div(
                    dcc.Graph(
                        figure=new_species_chart,
                        style={"width": "70vh", "height": "50vh"},
                    ),
                ),
            ],
        ),
        dbc.Container(
            [
                html.H2(children=f"Observations durant l'évenement"),
                dl.Map(
                    children=[
                        dl.TileLayer(
                            url="https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&LAYER=GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2&FORMAT=image/png",
                            attribution="&copy; IGN ",
                        ),
                        dl.GeoJSON(data=limit_commune),
                        dl.GeoJSON(
                            data=observation_geom, pointToLayer=assign(pointToLayer)
                        ),
                    ],
                    center=[45.04, 5.95],
                    zoom=13,
                    style={"height": "80vh"},
                    className="mb-4",
                ),
            ]
        ),
        html.H2(children=f"{len(observers)} observateurs au total pendant l'évenement"),
        html.Div(
            dash_table.DataTable(
                data=observers,
                page_size=15,
                sort_action="native",
                id="observers",
                style_cell={"textAlign": "left"},
            ),
            className="col-6 mb-4",
        ),
        # MAP
        # dcc.Graph(figure=map),
    ],
    fluid=True,
)


def filter_df(df: pd.DataFrame, column: str, value: str) -> List:
    """
    Filter the dataframe in parameter according to column and value
    return a list of dict for Dash Datatable and plots
    """
    filter_df = df[df[column] == value]
    return filter_df.to_dict("records")


def on_update(column, value):
    if value:
        filter_species_in_event = filter_df(species_in_event_df, column, value)
        filter_new_species_commune = filter_df(new_species_df, column, value)
        filter_new_species_struct = filter_df(new_species_df, column, value)
        return (
            get_total_obs(column=column, filter=value),
            len(filter_species_in_event),
            filter_species_in_event,
            len(filter_new_species_commune),
            filter_new_species_commune,
            len(filter_new_species_struct),
            filter_new_species_struct,
        )
    else:
        return (
            get_total_obs(),
            len(species_in_event_df),
            g_species_in_event,
            len(new_species_commune_df),
            g_new_species_commune,
            len(g_new_species),
            g_new_species,
        )


@callback(
    [
        Output(component_id="nb_data", component_property="children"),
        Output(component_id="nb_species", component_property="children"),
        Output("datable_species", "data"),
        Output("nb_new_species_commune", "children"),
        Output("datable_new_species_commune", "data"),
        Output("nb_new_species_pne", "children"),
        Output("new_species_in_structure", "data"),
    ],
    [
        Input("group2-dropdown", "value"),
        Input("ordre-dropdown", "value"),
        Input("famille-dropdown", "value"),
    ],
)
def update_output_div(group2, ordre, famille):
    if famille:
        return on_update("famille", famille)
    elif ordre:
        return on_update("ordre", ordre)
    elif group2:
        return on_update("group2_inpn", group2)
    else:
        return on_update(None, None)


if __name__ == "__main__":
    app.run(debug=True)
