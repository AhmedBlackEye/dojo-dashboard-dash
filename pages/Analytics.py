import dash
from dash import html, dcc, Input, Output, callback, dash_table
import pandas as pd
import plotly.express as px
from components.graph_card import graph_card

dash.register_page(__name__)


def load_data():
    data = pd.read_csv("./data/customer_a.csv")
    data["transaction_timestamp"] = pd.to_datetime(data["transaction_timestamp"])
    return data


def get_sales_over_time(data):
    sales_over_time = (
        data.groupby("transaction_timestamp")["amount"].sum().cumsum().reset_index()
    )

    return px.line(
        sales_over_time,
        x="transaction_timestamp",
        y="amount",
        title="Sales Over Time",
        # width=800,
        # height=500,
        labels={"transaction_timestamp": "Time", "amount": "Sales"},
    )


data = load_data()
layout = html.Div(
    className="grid gap-4",
    children=[
        graph_card(
            "Test",
            "so good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so far",
            get_sales_over_time(data),
        ),
        graph_card(
            "Test",
            "so good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so far",
            get_sales_over_time(data),
        ),
        graph_card(
            "Test",
            "so good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so faro good so far",
            get_sales_over_time(data),
        ),
    ],
)
