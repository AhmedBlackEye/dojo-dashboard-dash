import dash
from dash import html, dcc, Input, Output, callback, dash_table
import pandas as pd
import plotly.express as px
from components.graph_card import graph_card
from utils.get_data import *
from utils.graphs import *

# from utils.model import visualize_forecast

dash.register_page(__name__, path="/")


def sidebar():
    locations = list(data["postcode_area"].unique())
    card_types = list(data["card_type"].unique())
    card_country_types = list(data["card_country_type"].unique())
    entry_types = list(data["entry_type"].unique())
    return html.Div(
        className="grid grid-cols-2 gap-2 p-6 rounded-lg bg-base-100 mb-8",
        children=[
            html.Span("Date", className="text-xl font-semibold"),
            dcc.DatePickerRange(
                id="date-range",
                start_date=pd.Timestamp(year=2023, month=5, day=1),
                end_date=pd.Timestamp(year=2023, month=5, day=31),
                display_format="MMM Do, YY",
                start_date_placeholder_text="Start Date",
                end_date_placeholder_text="End Date",
                min_date_allowed=data["transaction_timestamp"].min(),
                max_date_allowed=data["transaction_timestamp"].max(),
            ),
            html.Span("Locations", className="text-xl font-semibold"),
            dcc.Dropdown(
                id="locations",
                className="",
                options=locations,
                value=locations,
                multi=True,
            ),
            html.Span("Card Type", className="text-xl font-semibold"),
            dcc.Checklist(
                id="card_types",
                className="flex flex-wrap gap-4",
                options=card_types,
                value=card_types,
            ),
            html.Span("Card Country Type", className="text-xl font-semibold"),
            dcc.Checklist(
                id="card_country_types",
                className="flex flex-wrap gap-4",
                options=card_country_types,
                value=card_country_types,
            ),
            html.Span("Purchase Type", className="text-xl font-semibold"),
            dcc.Checklist(
                id="entry_types",
                className="flex flex-wrap gap-4",
                options=entry_types,
                value=entry_types,
            ),
        ],
    )


def analytics(data):
    return html.Div(
        id="analytics-container",
        className="grid gap-7",
        children=[
            # dcc.Graph(visualize_forecast()),
            graph_card(
                "Sales Over Time",
                get_sales_over_time_info(data),
                get_sales_over_time(data),
            ),
            graph_card(
                "Sales Per Weekdays",
                get_sales_per_weekday_info(data),
                get_sales_per_weekday(data),
            ),
            graph_card(
                "Sales Per Location",
                get_sales_per_location_info(data),
                get_sales_per_location(data, "bar"),
            ),
        ],
    )


@callback(
    Output("analytics-container", "children"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("locations", "value"),
        Input("card_types", "value"),
        Input("card_country_types", "value"),
        Input("entry_types", "value"),
    ],
)
def update_analytics(
    start_date,
    end_date,
    selected_locations,
    selected_card_types,
    selected_card_country_types,
    selected_entry_types,
):
    start_date = pd.Timestamp(start_date).tz_localize("UTC")
    end_date = pd.Timestamp(end_date).tz_localize("UTC")

    if isinstance(selected_locations, str):
        selected_locations = [selected_locations]

    filtered_data = data[
        (data["transaction_timestamp"] >= start_date)
        & (data["transaction_timestamp"] <= end_date)
        & (data["postcode_area"].isin(selected_locations))
        & (data["card_type"].isin(selected_card_types))
        & (data["card_country_type"].isin(selected_card_country_types))
        & (data["entry_type"].isin(selected_entry_types))
    ]

    return analytics(filtered_data)


layout = html.Div(children=[sidebar(), analytics(data)])
