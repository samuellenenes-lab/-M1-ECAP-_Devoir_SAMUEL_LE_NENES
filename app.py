## Import libraries ##

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc



## Chargement des données ##

df = pd.read_csv("C:/Users/samue/OneDrive/Documents/Cours/M1 ECAP/Python avancée/projet/supermarket_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.to_period("W").apply(lambda x: x.start_time)

cities = sorted(df["City"].unique())
genders = sorted(df["Gender"].unique())


## Création de l'application Dash ##

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Styles
BG = "#F0F4F8"
CARD = "#FFFFFF"
PRIMARY = "#4A6FA5"
ACCENT = "#6B9AC4"
DARK = "#2D3748"
MUTED = "#8899A6"
PASTEL = ["#A8D8EA", "#AA96DA", "#FCBAD3", "#FFD3B6", "#B5EAD7", "#C7CEEA"]

app.layout = html.Div(style={"fontFamily": "'Segoe UI', sans-serif", "backgroundColor": BG,
                              "minHeight": "100vh", "padding": "0", "margin": "0"}, children=[

    html.Div(style={
        "backgroundColor": CARD, "padding": "20px 40px", "display": "flex",
        "justifyContent": "space-between", "alignItems": "center",
        "borderBottom": f"3px solid {PRIMARY}", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)",
    }, children=[
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "12px"}, children=[
            html.Span("Tableaux de bord interactif", style={"fontSize": "30px"}),
            html.H2("(Vente de supermarche)", style={"margin": "0", "color": DARK,
                                                "fontWeight": "600", "letterSpacing": "1px"}),
        ]),
        html.Div(style={
            "backgroundColor": BG, "borderRadius": "20px", "padding": "8px 20px",
            "fontSize": "13px", "color": MUTED, "border": "1px solid #D8DEE6",
        }, children="Supermarket Sales - Analyse interactive"),
    ]),

    html.Div(style={"padding": "24px 40px"}, children=[

        html.Div(style={
            "display": "flex", "gap": "20px", "marginBottom": "22px", "alignItems": "flex-end",
        }, children=[
            html.Div(style={"width": "220px"}, children=[
                html.Label("VILLE", style={"fontSize": "11px", "fontWeight": "700",
                                            "color": MUTED, "letterSpacing": "1px",
                                            "marginBottom": "4px", "display": "block"}),
                dcc.Dropdown(id="dd-city",
                             options=[{"label": "Toutes", "value": "Toutes"}] +
                                     [{"label": c, "value": c} for c in cities],
                             value="Toutes", clearable=False),
            ]),
            html.Div(style={"width": "200px"}, children=[
                html.Label("SEXE", style={"fontSize": "11px", "fontWeight": "700",
                                           "color": MUTED, "letterSpacing": "1px",
                                           "marginBottom": "4px", "display": "block"}),
                dcc.Dropdown(id="dd-gender",
                             options=[{"label": "Tous", "value": "Tous"}] +
                                     [{"label": g, "value": g} for g in genders],
                             value="Tous", clearable=False),
            ]),
        ]),

        html.Div(id="kpi-cards", style={"display": "flex", "gap": "20px", "marginBottom": "22px"}),

        html.Div(style={"display": "flex", "gap": "20px", "marginBottom": "20px"}, children=[
            html.Div(style={"flex": "1", "backgroundColor": CARD, "borderRadius": "12px",
                            "padding": "14px", "boxShadow": "0 1px 6px rgba(0,0,0,0.05)"}, children=[
                dcc.Graph(id="graph-hist", config={"displayModeBar": False}),
            ]),
            html.Div(style={"flex": "1", "backgroundColor": CARD, "borderRadius": "12px",
                            "padding": "14px", "boxShadow": "0 1px 6px rgba(0,0,0,0.05)"}, children=[
                dcc.Graph(id="graph-pie", config={"displayModeBar": False}),
            ]),
        ]),

        html.Div(style={"backgroundColor": CARD, "borderRadius": "12px", "padding": "14px",
                         "boxShadow": "0 1px 6px rgba(0,0,0,0.05)"}, children=[
            dcc.Graph(id="graph-weekly", config={"displayModeBar": False}),
        ]),
    ]),
])


def make_kpi(label, value, border_color):
    return html.Div(style={
        "flex": "1", "backgroundColor": CARD, "borderRadius": "12px",
        "padding": "20px 24px", "textAlign": "center",
        "boxShadow": "0 1px 6px rgba(0,0,0,0.05)",
        "borderLeft": f"5px solid {border_color}",
    }, children=[
        html.P(label, style={"margin": "0", "fontSize": "12px", "color": MUTED,
                              "fontWeight": "600", "textTransform": "uppercase",
                              "letterSpacing": "0.5px"}),
        html.H3(value, style={"margin": "10px 0 0", "fontSize": "26px",
                                "fontWeight": "700", "color": DARK}),
    ])


LAYOUT = dict(
    plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Segoe UI, sans-serif", color=DARK, size=12),
    margin=dict(t=45, b=35, l=45, r=20),
    title_font=dict(size=14, color=DARK),
)


@app.callback(
    Output("kpi-cards", "children"),
    Output("graph-hist", "figure"),
    Output("graph-pie", "figure"),
    Output("graph-weekly", "figure"),
    Input("dd-city", "value"),
    Input("dd-gender", "value"),
)
def update(city, gender):
    dff = df.copy()
    if city != "Toutes":
        dff = dff[dff["City"] == city]
    if gender != "Tous":
        dff = dff[dff["Gender"] == gender]

    cards = [
        make_kpi("Montant total des achats", f"{dff['Total'].sum():,.0f}", "#A8D8EA"),
        make_kpi("Nombre total d'achats", f"{dff['Invoice ID'].nunique()}", "#AA96DA"),
    ]

    fig_hist = px.histogram(dff, x="Total", nbins=20, color_discrete_sequence=["#A8D8EA"],
                            title="Répartition des montants totaux")
    fig_hist.update_layout(**LAYOUT, xaxis_title="Montant", yaxis_title="Frequence")
    fig_hist.update_traces(marker_line_width=0.8, marker_line_color="white")

    pie_data = dff.groupby("Product line")["Invoice ID"].count().reset_index(name="Count")
    fig_pie = px.pie(pie_data, names="Product line", values="Count",
                     title="Répartition par catégorie de produit", hole=0.4,
                     color_discrete_sequence=PASTEL)
    fig_pie.update_layout(**LAYOUT, legend=dict(font=dict(size=11)))

    weekly = dff.groupby("Week")["Total"].sum().reset_index()
    fig_week = px.bar(weekly, x="Week", y="Total",
                      title="Evolution hebdomadaire du montant total",
                      color_discrete_sequence=["#B5EAD7"])
    fig_week.update_layout(**LAYOUT, xaxis_title="Semaine", yaxis_title="Montant total")
    fig_week.update_traces(marker_line_width=0.5, marker_line_color="white")

    return cards, fig_hist, fig_pie, fig_week


if __name__ == "__main__":
    app.run_server(debug=True)
