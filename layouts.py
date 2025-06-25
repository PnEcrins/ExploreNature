from dash import html
import dash_bootstrap_components as dbc


def card(title, nb, id):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(title, className="card-title"),
                    html.H2(
                        nb,
                        className="card-text",
                        id=id
                    ),
                ],
                className="text-center",
            ),
        ],
        style={"width": "18rem"},
        className="me-2",
    )
