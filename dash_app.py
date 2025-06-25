from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

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
    get_ordres
)


# TODO : nombre d'espèce total observé
# répartition par groupe des espèces
# rajouter l'ordre et la classe sur les tableaux ?


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

new_species = get_new_species()
new_species_chart = px.pie(
    pd.DataFrame.from_dict(new_species),
    names="group2_inpn",
    title="Nouvelle espèces",
    hole=0.3,
)

new_species_commune = get_new_species_commune()

new_species_commune_chart = px.pie(
    pd.DataFrame.from_dict(new_species_commune),
    names="group2_inpn",
    hole=0.3,
)

species_in_event = get_species_in_event()

species_event_chart = px.pie(
    pd.DataFrame.from_dict(species_in_event),
    names="group2_inpn",
    hole=0.3,
)
species_event_chart.update_traces(textinfo="value")



# observations
obs_df = pd.DataFrame.from_dict(get_all_data_geo())
map = px.density_map(
    lat=obs_df.latitude,
    lon=obs_df.longitude,
    z=obs_df.nb,
    radius=10,
    map_style="satellite",
    height=800,
)


# GLOBAL DATAFRAMES 

g_species_in_event = get_species_in_event()
species_in_event_df = pd.DataFrame.from_dict(g_species_in_event)



# print(new_species_chart)
app.layout = dbc.Container(
    [
        html.H1(children="Explor'Nature 2025", style={"textAlign": "center"}),
        html.Div([
            dcc.Dropdown(get_group2_inpn(), id='group2-dropdown', clearable=True, placeholder="Filtrer par groupe INPN", className="mb-3"),
            dcc.Dropdown(get_ordres(), id='ordre-dropdown', clearable=True, placeholder="Filtrer par ordre"),
        ],
        className="mb-3"
        ),

        # CARD
        html.Div(
            className="d-flex justify-content-center mb-5",
            children=[
                card("Nombre de données", "", id="nb_data"),
                card("Nombre d'espèces", "", "nb_species"),
                card("Nouvelles espèces pour le PNE", len(new_species), "nb_new_species_pne"),
                card("Nouvelles espèces pour la commune", len(new_species_commune), "nb_new_species_pne_commune"),
            ],
        ),
        # SPECIES IN EVENT
        html.Div(
            children=[
                html.H2(
                    children="Taxons observés pendant l'évenement"
                ),
                html.Div(id='my-output'),
                html.Div(
                    className="row mt-3",
                    children=[
                        html.Div(
                            dash_table.DataTable(data=[], page_size=20, sort_action='native', id="datable_species"),
                            className="col-6",
                        ),
                        html.Div(
                            dcc.Graph(
                                figure=species_event_chart,
                                style={"width": "70vh", "height": "50vh"},
                            ),
                            className="col-6",
                        ),
                    ],
                ),
            ]
        ),

        # NOUVELLE ESPECE COMMUNE
        html.H2(children=f" {len(new_species_commune)} Nouvelles espèces sur la commune"),
        html.Div(
            className="row mt-3",
            children=[
                html.Div(
                    dash_table.DataTable(data=new_species_commune, page_size=20, sort_action='native'),
                    className="col-6",
                ),
                html.Div(
                    dcc.Graph(
                        figure=new_species_commune_chart,
                        style={"width": "70vh", "height": "50vh"},
                    ),
                    className="col-6",
                ),
            ],
        ),
        # NOUVELLE ESPECE PNE
        html.H2(children=f" {len(new_species)} nouvelles espèces pour le PNE"),
        html.Div(
            className="row mt-3",
            children=[
                html.Div(
                    dash_table.DataTable(data=new_species, page_size=20, sort_action='native'),
                    className="col-6",
                ),
                html.Div(
                    dcc.Graph(
                        figure=new_species_chart,
                        style={"width": "70vh", "height": "50vh"},
                    ),
                    className="col-6",
                ),
            ],
        ),
        # MAP
        dcc.Graph(figure=map),
    ],
    fluid=True,
)

def filter_df(df, column, value):
    filter_df = df[df[column] == value]
    return filter_df.to_dict("records")

@callback(
    Output(component_id='nb_data', component_property='children'),
    Output(component_id='nb_species', component_property='children'),
    Output('datable_species', "data"),
    Input('group2-dropdown', 'value'),
)
def update_output_div(value):
    if value:
        # species_in_event = get_species_in_event(column="group2_inpn", filter=value)
        filter_species_in_event = filter_df(species_in_event_df, "group2_inpn", value)
        return get_total_obs(column="group2_inpn", filter=value), len(filter_species_in_event), filter_species_in_event
    else:
        
        
        return get_total_obs(), len(species_in_event_df), g_species_in_event
    





if __name__ == "__main__":
    app.run(debug=True)
