import pandas as pd
import plotly.express as px
from dash import html
from .get_data import data, current_end_date

# from lifetimes import (
#     GammaGammaFitter,
#     ModifiedBetaGeoFitter,
#     BetaGeoBetaBinomFitter,
#     BetaGeoFitter,
# )

# from .model import get_change_points

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_sales_over_time(data):
    sales_over_time = (
        data.groupby("transaction_timestamp")["amount"].sum().cumsum().reset_index()
    )
    fig = px.line(
        sales_over_time,
        x="transaction_timestamp",
        y="amount",
        title="Sales Over Time",
        labels={"transaction_timestamp": "Time", "amount": "Sales"},
    )

    return fig


def get_sales_over_time_info(data):
    daily_sales = (
        data.groupby(data["transaction_timestamp"].dt.date)["amount"]
        .sum()
        .reset_index()
    )

    if daily_sales.empty:
        return [
            html.Li("No sales data available"),
        ]

    average_sale = daily_sales["amount"].mean()
    highest_sale = daily_sales["amount"].max()

    most_transaction_day = (
        data["transaction_timestamp"]
        .dt.date.value_counts()
        .idxmax()
        .strftime("%b %dth, %y")
    )

    most_profitable_day = daily_sales.loc[
        daily_sales["amount"].idxmax(), "transaction_timestamp"
    ].strftime("%b %dth, %y")

    return [
        html.Li(f"Average Sales Value: £{round(average_sale, 2)}"),
        html.Li(
            f"Most Transaction day: {most_transaction_day}", className="text-green-400"
        ),
        html.Li(
            f"Most Profitable Day: {most_profitable_day}", className="text-green-400"
        ),
        html.Li(f"Highest Sale: £{round(highest_sale, 2)}", className="text-green-400"),
    ]


def get_sales_per_weekday(data):
    sales_per_weekday = (
        data.groupby(data["transaction_timestamp"].dt.day_name())["amount"]
        .sum()
        .reset_index()
    )
    sales_per_weekday["transaction_timestamp"] = pd.Categorical(
        sales_per_weekday["transaction_timestamp"],
        categories=weekday_order,
        ordered=True,
    )

    sales_per_weekday = sales_per_weekday.sort_values("transaction_timestamp")
    return px.bar(
        sales_per_weekday,
        x="transaction_timestamp",
        y="amount",
        title="Sales Per Day",
        labels={"transaction_timestamp": "Day", "Sales": "Amount"},
    )


def get_sales_per_weekday_info(data):
    sales_per_weekday = (
        data.groupby(data["transaction_timestamp"].dt.day_name())["amount"]
        .sum()
        .reset_index()
    )
    if sales_per_weekday.empty:
        return [
            html.Li("No sales data available"),
        ]

    highest_sale_day = sales_per_weekday.loc[
        sales_per_weekday["amount"].idxmax(), "transaction_timestamp"
    ]
    highest_sale_amount = sales_per_weekday.loc[
        sales_per_weekday["amount"].idxmax(), "amount"
    ]

    lowest_sale_day = sales_per_weekday.loc[
        sales_per_weekday["amount"].idxmin(), "transaction_timestamp"
    ]
    lowest_sale_amount = sales_per_weekday.loc[
        sales_per_weekday["amount"].idxmin(), "amount"
    ]

    return [
        html.Li(
            f"Day with Highest Sale: {highest_sale_day}", className="text-green-400"
        ),
        html.Li(
            f"Revenue On That Day: £{highest_sale_amount}", className="text-green-400"
        ),
        html.Li(f"Day with Lowest Sale: {lowest_sale_day}", className="text-red-400"),
        html.Li(
            f"Revenue On That Day: £{lowest_sale_amount}", className="text-red-400"
        ),
    ]


################## Sales Per Location Graph ##################
def get_sales_per_location(data, chart_type="pie"):
    locations_sales = data.groupby("postcode_area")["amount"].sum().reset_index()
    if chart_type == "pie":
        return px.pie(
            locations_sales,
            values="amount",
            names="postcode_area",
            title="Sales by Location",
            hole=0.4,
            labels={"amount": "Sales Amount", "postcode_area": "Location"},
        )
    else:
        return px.bar(
            locations_sales,
            x="postcode_area",
            y="amount",
            title="Sales by Location",
            labels={"amount": "Sales Amount", "postcode_area": "Location"},
        )


######################### Sales Per Location #####################
def get_sales_per_location_info(data):
    locations_sales = data.groupby("postcode_area")["amount"].sum().reset_index()

    if locations_sales.empty:
        return [
            html.Li("No sales data available"),
        ]
    highest_sales_area = locations_sales.loc[
        locations_sales["amount"].idxmax(), "postcode_area"
    ]
    highest_sales_value = locations_sales.loc[
        locations_sales["amount"].idxmax(), "amount"
    ]
    lowest_sales_area = locations_sales.loc[
        locations_sales["amount"].idxmin(), "postcode_area"
    ]
    lowest_sales_value = locations_sales.loc[
        locations_sales["amount"].idxmin(), "amount"
    ]

    return [
        html.Li(
            f"Area with Highest Sales: {highest_sales_area}", className="text-green-400"
        ),
        html.Li(
            f"Revenue From This Area: £{highest_sales_value}",
            className="text-green-400",
        ),
        html.Li(
            f"Area with Lowest Sales: {lowest_sales_area}", className="text-red-400"
        ),
        html.Li(
            f"Revenue From This Area: £{lowest_sales_value}", className="text-red-400"
        ),
    ]


############################# Sales Per Hour ###############################
def get_sales_per_hour(data):
    data["hour"] = data["transaction_timestamp"].dt.hour
    sales_per_hour = data.groupby("hour")["amount"].sum().reset_index()

    return px.bar(
        sales_per_hour,
        x="hour",
        y="amount",
        title="Sales Per Hour",
        labels={"hour": "Hour", "amount": "Sales Amount"},
    )


def get_sales_per_hour_info(data):
    data["hour"] = data["transaction_timestamp"].dt.hour
    sales_per_hour = data.groupby("hour")["amount"].sum().reset_index()

    most_sales_hour = sales_per_hour.loc[sales_per_hour["amount"].idxmax(), "hour"]
    most_sales_avg = data[data["hour"] == most_sales_hour]["amount"].mean()

    lowest_sales_hour = sales_per_hour.loc[sales_per_hour["amount"].idxmin(), "hour"]
    lowest_sales_avg = data[data["hour"] == lowest_sales_hour]["amount"].mean()

    return [
        html.Li(f"Most Sales Hour: {most_sales_hour}", className="text-green-400"),
        html.Li(f"Avg: £{round(most_sales_avg, 2)}", className="text-green-400"),
        html.Li(f"Lowest Sales Hour: {lowest_sales_hour}", className="text-red-400"),
        html.Li(f"Avg: £{round(lowest_sales_avg, 2)}", className="text-red-400"),
    ]


##### Sales per Card Type #####
def get_sales_per_card_type(data):
    card_type_sales = data.groupby("card_type")["amount"].sum().reset_index()
    return px.pie(
        card_type_sales,
        values="amount",
        names="card_type",
        title="Sales by Card Type",
        labels={"amount": "Sales Amount", "card_type": "Card Type"},
    )


def get_sales_per_card_entry(data):
    card_entry_sales = data.groupby("entry_type")["amount"].sum().reset_index()
    return px.pie(
        card_entry_sales,
        values="amount",
        names="entry_type",
        title="Sales by Card Entry",
        labels={"amount": "Sales Amount", "entry_type": "Card Entry"},
    )


# def get_customer_lifetime_value_graph(data):
#     # Calculate recency and T values
#     max_purchase_date = (
#         data.groupby("customer_id")["transaction_timestamp"].max().reset_index()
#     )
#     max_purchase_date.columns = ["customer_id", "last_purchase_date"]
#     data = pd.merge(data, max_purchase_date, on="customer_id")
#     data["recency"] = (
#         data["last_purchase_date"].max() - data["last_purchase_date"]
#     ).dt.days
#     data["T"] = (
#         data["last_purchase_date"].max() - data["transaction_timestamp"]
#     ).dt.days

#     # Calculate frequency
#     summary = data.groupby("customer_id").agg(
#         {"transaction_timestamp": ["count", "min"], "amount": "sum"}
#     )
#     summary.columns = ["frequency", "first_purchase_date", "monetary_value"]
#     summary["first_purchase_date"] = (
#         summary["first_purchase_date"].max() - summary["first_purchase_date"]
#     ).dt.days
#     summary.reset_index(inplace=True)

#     # Filter out non-positive values in monetary_value
#     summary = summary[summary["monetary_value"] > 0]

#     # Fit the Gamma-Gamma model
#     ggf = GammaGammaFitter(penalizer_coef=0.4)
#     ggf.fit(summary["frequency"], summary["monetary_value"])

#     # Fit the BG/NBD model
#     bgf = BetaGeoFitter(penalizer_coef=0.4)
#     bgf.fit(summary["frequency"], summary["recency"], summary["T"])

#     # Calculate customer lifetime value
#     summary["clv"] = ggf.customer_lifetime_value(
#         bgf,
#         summary["frequency"],
#         summary["recency"],
#         summary["T"],
#         summary["monetary_value"],
#     )

#     # Plot the number of transactions per customer
#     fig = px.bar(
#         summary,
#         x="customer_id",
#         y="frequency",
#         title="Number of Transactions per Customer",
#     )
#     return fig


# # Example usage:
